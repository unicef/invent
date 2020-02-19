<template>
  <div class="NewProjectForm">
    <el-form
      ref="projectForm"
      label-position="top"
      @submit.native.prevent
    >
      <el-row type="flex">
        <el-col :span="18">
          <general-overview
            ref="generalOverview"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
          />
          <implementation-overview
            ref="implementationOverview"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
          />
          <donor-custom
            ref="donorCustom"
            :use-publish-rules="usePublishRules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
          />
        </el-col>
        <el-col :span="6">
          <project-navigation
            @saveDraft="doSaveDraft"
            @discardDraft="doDiscardDraft"
            @publishProject="doPublishProject"
          />
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { publishRules, draftRules } from '@/utilities/projects';
import ProjectNavigation from './ProjectNavigation';
import GeneralOverview from './sections/GeneralOverview';
import ImplementationOverview from './sections/ImplementationOverview';
import DonorCustom from './sections/DonorCustom';
import { mapGetters, mapActions } from 'vuex';

export default {
  components: {
    ProjectNavigation,
    GeneralOverview,
    ImplementationOverview,
    DonorCustom
  },
  $_veeValidate: {
    validator: 'new'
  },
  data () {
    return {
      readyElements: 0,
      createdElements: 0,
      usePublishRules: false,
      apiErrors: {}
    };
  },
  computed: {
    ...mapGetters({
      project: 'project/getProjectData',
      countryAnswers: 'project/getCountryAnswers',
      donorAnswers: 'project/getDonorsAnswers'
    }),
    isDraft () {
      return this.$route.name.includes('organisation-projects-id-edit');
    },
    isNewProject () {
      return this.$route.name.includes('organisation-projects-create');
    },
    draftRules: draftRules,
    publishRules: publishRules,
    rules () {
      return this.usePublishRules ? this.publishRules : this.draftRules;
    }
  },
  mounted () {
    if (this.$route.query.reloadDataFromStorage) {
      this.$nextTick(() => {
        this.$nuxt.$loading.start();
        try {
          const stored = JSON.parse(window.localStorage.getItem('rescuedProject'));
          this.initProjectState(stored);
        } catch (e) {
          this.$alert(this.$gettext('Failed to restore auto-saved project'), this.$gettext('Warning'), {
            confirmButtonText: this.$gettext('OK')
          });
        }
        window.localStorage.removeItem('rescuedProject');
        this.$router.replace({ ...this.$route, query: undefined });
        this.$nuxt.$loading.finish();
      });
    }
  },
  methods: {
    ...mapActions({
      createProject: 'project/createProject',
      saveDraft: 'project/saveDraft',
      discardDraft: 'project/discardDraft',
      publishProject: 'project/publishProject',
      setLoading: 'project/setLoading',
      initProjectState: 'project/initProjectState'
    }),
    digitalHealthInterventionsValidator (rule, value, callback) {
      const ownDhi = this.project.digitalHealthInterventions.filter(dhi => dhi.platform === value && dhi.id);
      if (ownDhi.length === 0) {
        const error = {
          message: this.$gettext('Please select one or more Digital Health Intervetions for this Software'),
          field: rule.fullField
        };
        callback(error);
      } else {
        callback();
      }
    },
    async unCaughtErrorHandler (errors) {
      if (this.$sentry) {
        this.$sentry.captureMessage('Un-caught validation error in project page', {
          level: 'error',
          extra: {
            apiErrors: this.apiErrors,
            errors
          }
        });
      }

      try {
        await this.$confirm(this.$gettext('There was an un-caught validation error an automatic report has been submitted'),
          this.$gettext('Warning'), {
            confirmButtonText: this.$gettext('Recover & Reload'),
            cancelButtonText: this.$gettext('Discard changes')
          });
        const project = {
          ...this.project,
          country_custom_answers: this.countryAnswers,
          donor_custom_answers: this.donorAnswers
        };
        const toStore = JSON.stringify(project);
        window.localStorage.setItem('rescuedProject', toStore);
        const newUrl = window.location.origin + this.$route.path + `?reloadDataFromStorage=true`;
        window.location.href = newUrl;
      } catch (e) {
        console.log('User declined the option to save, just reloading');
        window.location.reload(true);
      }
    },
    handleErrorMessages () {
      this.$nextTick(() => {
        const errors = [...this.$el.querySelectorAll('.is-error')];
        const visibleErrors = errors.filter(e => e.offsetParent !== null);
        if (visibleErrors && visibleErrors.length > 0) {
          visibleErrors[0].scrollIntoView();
        } else {
          this.unCaughtErrorHandler(errors);
        }
      });
    },
    async validate () {
      const validations = await Promise.all([
        this.$refs.generalOverview.validate(),
        this.$refs.implementationOverview.validate(),
        this.$refs.donorCustom.validate()
      ]);
      console.log('root validations', validations);
      return validations.reduce((a, c) => a && c, true);
    },
    clearValidation () {
      this.apiErrors = {};
      this.$refs.generalOverview.clear();
      this.$refs.implementationOverview.clear();
      this.$refs.donorCustom.clear();
    },
    async doSaveDraft () {
      this.clearValidation();
      this.usePublishRules = false;
      this.$nextTick(async () => {
        const valid = await this.$refs.generalOverview.validateDraft();
        if (valid) {
          try {
            if (this.isNewProject) {
              const id = await this.createProject();
              const localised = this.localePath({ name: 'organisation-projects-id-edit', params: { ...this.$route.params, id } });
              this.$router.push(localised);
            } else if (this.isDraft) {
              await this.saveDraft(this.$route.params.id);
            }
            this.$alert(this.$gettext('Your draft has been saved successfully'), this.$gettext('Congratulation'), {
              confirmButtonText: this.$gettext('Close')
            });
            return;
          } catch (e) {
            if (e.response) {
              this.apiErrors = e.response.data;
            } else {
              console.error(e);
            }
            this.setLoading(false);
          }
        }
        this.handleErrorMessages();
      });
    },
    async doDiscardDraft () {
      try {
        await this.$confirm(this.$gettext('The current draft will be overwritten by the published version'), this.$gettext('Attention'), {
          confirmButtonText: this.$gettext('Ok'),
          cancelButtonText: this.$gettext('Cancel'),
          type: 'warning'
        });
        await this.discardDraft(this.$route.params.id);
        this.$message({
          type: 'success',
          message: this.$gettext('Draft overriden with published version')
        });
      } catch (e) {
        this.setLoading(false);
        this.$message({
          type: 'info',
          message: this.$gettext('Action cancelled')
        });
      }
    },
    async doPublishProject () {
      this.clearValidation();
      this.usePublishRules = true;
      this.$nextTick(async () => {
        const valid = await this.validate();
        if (valid) {
          try {
            await this.publishProject(this.$route.params.id);
            const localised = this.localePath({ name: 'organisation-projects-id-published', params: { ...this.$route.params } });
            this.$router.push(localised);
            this.$alert(this.$gettext('Your draft has been published successfully'), this.$gettext('Congratulation'), {
              confirmButtonText: this.$gettext('Close')
            });
            return;
          } catch (e) {
            console.log(e);
            this.setLoading(false);
            this.apiErrors = e.response.data;
          }
        }
        this.handleErrorMessages();
      });
    }
  }

};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .NewProjectForm {
    .limitPageWidth();

    .Loader {
      display: block;
      margin: 0 auto 80px;
       span {
         margin: 0 auto;
       }
    }

    > .el-form {
      > .el-row > .el-col {
        // form fieldsets
        &:first-child {
          width: calc(100% - @projectAsideNavWidth - 20px);
          margin-right: 20px;
        }

        // aside navigation
        &:last-child {
          width: @projectAsideNavWidth;
        }
      }
    }
  }
</style>
