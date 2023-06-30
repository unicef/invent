<template>
  <div class="NewProjectForm">
    <div v-show="!showForm" class="Loader">
      <div />
      <span>Loading</span>
    </div>
    <el-form ref="projectForm" label-position="top" @submit.native.prevent>
      <el-row v-show="showForm" type="flex">
        <el-col :span="18">
          <GeneralOverview
            key="generalOverview"
            ref="generalOverview"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <Categorization
            key="categorization"
            ref="categorization"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <ImplementationOverview
            ref="implementationOverview"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <StageOverview
            ref="stageOverview"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <Partners
            ref="partners"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <Technology
            ref="technology"
            :rules="rules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <DonorCustom
            ref="donorCustom"
            :use-publish-rules="usePublishRules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <CountryCustom
            ref="countryCustom"
            :use-publish-rules="usePublishRules"
            :draft-rules="draftRules"
            :publish-rules="publishRules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
        </el-col>
        <el-col :span="6">
          <ProjectNavigation
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
import { publishRules, draftRules } from '@/utilities/projects'
import { mapGetters, mapActions } from 'vuex'
import GeneralOverview from '@/components/project/sections/GeneralOverview'
import Categorization from '@/components/project/sections/Categorization'
import ImplementationOverview from '@/components/project/sections/ImplementationOverview'
import StageOverview from '@/components/project/sections/StageOverview'
import Partners from '@/components/project/sections/Partners'
import Technology from '@/components/project/sections/Technology'
import DonorCustom from '@/components/project/sections/DonorCustom'
import CountryCustom from '@/components/project/sections/CountryCustom'
import ProjectNavigation from '@/components/project/ProjectNavigation'

export default {
  components: {
    GeneralOverview,
    Categorization,
    ImplementationOverview,
    StageOverview,
    Partners,
    Technology,
    DonorCustom,
    ProjectNavigation,
    CountryCustom,
  },
  $_veeValidate: {
    validator: 'new',
  },
  data() {
    return {
      readyElements: 0,
      createdElements: 0,
      usePublishRules: false,
      apiErrors: {},
      coverImage: null,
    }
  },
  computed: {
    ...mapGetters({
      project: 'project/getProjectData',
      countryAnswers: 'project/getCountryAnswers',
      donorAnswers: 'project/getDonorsAnswers',
    }),
    isDraft() {
      return this.$route.name.includes('organisation-initiatives-id-edit')
    },
    isNewProject() {
      return this.$route.name.includes('organisation-initiatives-create')
    },
    showForm() {
      return this.readyElements >= this.createdElements
    },
    draftRules,
    publishRules,
    rules() {
      return this.usePublishRules ? this.publishRules : this.draftRules
    },
  },
  mounted() {
    if (this.$route.query.reloadAfterImport) {
      window.location.href = window.location.origin + this.$route.path
      return
    }
    if (this.$route.query.reloadDataFromStorage) {
      this.$nextTick(() => {
        this.$nuxt.$loading.start()
        try {
          const stored = JSON.parse(window.localStorage.getItem('rescuedProject'))
          this.initProjectState(stored)
        } catch (e) {
          this.$alert(this.$gettext('Failed to restore auto-saved project'), this.$gettext('Warning'), {
            confirmButtonText: this.$gettext('OK'),
          })
        }
        window.localStorage.removeItem('rescuedProject')
        this.$router.replace({ ...this.$route, query: undefined })
        this.$nuxt.$loading.finish()
      })
    }
  },
  methods: {
    ...mapActions({
      createProject: 'project/createProject',
      saveDraft: 'project/saveDraft',
      discardDraft: 'project/discardDraft',
      publishProject: 'project/publishProject',
      setLoading: 'project/setLoading',
      initProjectState: 'project/initProjectState',
    }),
    digitalHealthInterventionsValidator(rule, value, callback) {
      const ownDhi = this.project.digitalHealthInterventions.filter((dhi) => dhi.platform === value && dhi.id)
      if (ownDhi.length === 0) {
        const error = {
          message: this.$gettext('Please select one or more Digital Health Intervetions for this Software'),
          field: rule.fullField,
        }
        callback(error)
      } else {
        callback()
      }
    },
    async unCaughtErrorHandler(errors) {
      try {
        await this.$confirm(
          this.$gettext('There was an un-caught validation error an automatic report has been submitted'),
          this.$gettext('Warning'),
          {
            confirmButtonText: this.$gettext('Recover & Reload'),
            cancelButtonText: this.$gettext('Discard changes'),
          }
        )
        const project = {
          ...this.project,
          country_custom_answers: this.countryAnswers,
          donor_custom_answers: this.donorAnswers,
        }
        const toStore = JSON.stringify(project)
        window.localStorage.setItem('rescuedProject', toStore)
        const newUrl = window.location.origin + this.$route.path + `?reloadDataFromStorage=true`
        window.location.href = newUrl
      } catch (e) {
        console.log('User declined the option to save, just reloading')
        window.location.reload(true)
      }
    },
    handleErrorMessages() {
      this.$nextTick(() => {
        const errors = [...this.$el.querySelectorAll('.is-error')]
        const visibleErrors = errors.filter((e) => e.offsetParent !== null)
        if (visibleErrors && visibleErrors.length > 0) {
          visibleErrors[0].scrollIntoView()
        } else {
          this.unCaughtErrorHandler(errors)
        }
      })
    },
    async validate() {
      const validations = await Promise.all([
        this.$refs.generalOverview.validate(),
        this.$refs.categorization.validate(),
        this.$refs.implementationOverview.validate(),
        this.$refs.stageOverview.validate(),
        this.$refs.partners.validate(),
        this.$refs.technology.validate(),
        this.$refs.donorCustom.validate(),
        this.$refs.countryCustom.validate(),
      ])
      console.log('root validations', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    clearValidation() {
      this.apiErrors = {}
      this.$refs.generalOverview.clear()
      this.$refs.categorization.clear()
      this.$refs.implementationOverview.clear()
      this.$refs.stageOverview.clear()
      this.$refs.partners.clear()
      this.$refs.technology.clear()
      this.$refs.donorCustom.clear()
      this.$refs.countryCustom.clear()
    },
    async doSaveDraft() {
      this.clearValidation()
      this.usePublishRules = false
      await this.$nextTick(async () => {
        const valid = await this.$refs.generalOverview.validateDraft()
        const categorization = await this.$refs.categorization.validateDraft()
        const technology = await this.$refs.technology.validateDraft()
        const stages = await this.$refs.stageOverview.validateDraft()
        const partners = await this.$refs.partners.validateDraft()
        if (valid && categorization && technology && stages && partners) {
          try {
            if (this.isNewProject) {
              const id = await this.createProject()
              const localised = this.localePath({
                name: 'organisation-initiatives-id-edit',
                params: { ...this.$route.params, id },
              })
              this.$router.push(localised)
            } else if (this.isDraft) {
              await this.saveDraft(this.$route.params.id)
              location.reload()
            }
            this.$alert(this.$gettext('Your draft has been saved successfully'), this.$gettext('Congratulation'), {
              confirmButtonText: this.$gettext('Close'),
            })
            return
          } catch (e) {
            if (e.response) {
              this.apiErrors = e.response.data
            } else {
              console.error(e)
              this.setLoading(false)
            }
          }
        }
        this.handleErrorMessages()
        this.setLoading(false)
      })
    },
    async doDiscardDraft() {
      try {
        await this.$confirm(
          this.$gettext('The current draft will be overwritten by the published version'),
          this.$gettext('Attention'),
          {
            confirmButtonText: this.$gettext('Ok'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning',
          }
        )
        await this.discardDraft(this.$route.params.id)
        this.$message({
          type: 'success',
          message: this.$gettext('Draft overriden with published version'),
        })
      } catch (e) {
        this.setLoading(false)
        this.$message({
          type: 'info',
          message: this.$gettext('Action cancelled'),
        })
      }
    },
    async doPublishProject() {
      this.clearValidation()
      this.usePublishRules = true
      await this.$nextTick(async () => {
        const valid = await this.validate()
        if (valid) {
          try {
            await this.publishProject(this.$route.params.id)
            const localised = this.localePath({
              name: 'organisation-initiatives-id-published',
              params: { ...this.$route.params },
            })
            this.$router.push(localised)
            this.$alert(this.$gettext('Your draft has been published successfully'), this.$gettext('Congratulation'), {
              confirmButtonText: this.$gettext('Close'),
            })
            return
          } catch (e) {
            console.log(e)
            this.setLoading(false)
            this.apiErrors = e.response.data ? e.response.data : 'error'
          }
        }
        this.handleErrorMessages()
        this.setLoading(false)
      })
    },
    createdHandler() {
      this.createdElements += 1
    },
    mountedHandler() {
      setTimeout(() => {
        this.readyElements += 1
      }, 300)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

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
