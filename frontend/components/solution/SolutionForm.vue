<template>
  <div class="NewProjectForm">
    <div v-show="!showForm" class="Loader">
      <div></div>
      <span>Loading</span>
    </div>
    <el-form ref="projectForm" label-position="top" @submit.native.prevent>
      <el-row v-show="showForm" type="flex">
        <el-col :span="18">
          <GeneralOverview
            key="solutionGeneral"
            ref="solutionGeneral"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
          <ActivityAndReach
            key="solutionActivityAndReach"
            ref="solutionActivityAndReach"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
          />
        </el-col>
        <el-col :span="6">
          <FormActionsAside @save="doSaveDraft" @cancel="doDiscardDraft" @delete="doPublishProject" />
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { rules } from '@/utilities/solutions'
import { mapGetters, mapActions } from 'vuex'
import GeneralOverview from './sections/GeneralOverview'
import ActivityAndReach from './sections/ActivityAndReach'
import FormActionsAside from './FormActionsAside.vue'

export default {
  components: {
    GeneralOverview,
    ActivityAndReach,
    FormActionsAside,
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
      countriesTable: [],
    }
  },
  computed: {
    ...mapGetters({
      solution: 'solution/getSolutionData',
      countryAnswers: 'project/getCountryAnswers',
      donorAnswers: 'project/getDonorsAnswers',
    }),
    isDraft() {
      return this.$route.name.includes('organisation-portfolio-innovation-solutions-edit')
    },
    isNewSolution() {
      return this.$route.name.includes('organisation-portfolio-innovation-solutions-create')
    },
    showForm() {
      return this.readyElements >= this.createdElements
    },
    rules,
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
          const stored = JSON.parse(window.localStorage.getItem('rescuedSoluton'))
          this.initProjectState(stored)
        } catch (e) {
          this.$alert(this.$gettext('Failed to restore auto-saved solution'), this.$gettext('Warning'), {
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
      createSolution: 'solution/createSolution',
      setSolution: 'solution/setSolution',
      discardDraft: 'project/discardDraft',
      publishProject: 'project/publishProject',
      setLoading: 'project/setLoading',
      initProjectState: 'project/initProjectState',
    }),
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
        const solution = {
          ...this.solution,
          country_custom_answers: this.countryAnswers,
          donor_custom_answers: this.donorAnswers,
        }
        const toStore = JSON.stringify(solution)
        window.localStorage.setItem('rescuedSolution', toStore)
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
        this.$refs.solutionGeneral.validate(),
        this.$refs.solutionActivityAndReach.validate(),
      ])
      console.log('root validations', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    clearValidation() {
      this.apiErrors = {}
      this.$refs.solutionGeneral.clear()
      this.$refs.solutionActivityAndReach.clear()
    },
    async doSaveDraft() {
      this.clearValidation()
      this.usePublishRules = false
      await this.$nextTick(async () => {
        const general = await this.$refs.solutionGeneral.validateDraft()
        const solutionActivityAndReach = await this.$refs.solutionActivityAndReach.validateDraft()

        if (general && solutionActivityAndReach) {
          try {
            if (this.isNewSolution) {
              const id = await this.createSolution()
              const localised = this.localePath({
                name: 'organisation-portfolio-innovation-solutions-id-edit',
                params: { ...this.$route.params, id },
              })
              this.$router.push(localised)
            } else if (this.isDraft) {
              await this.setSolution(this.$route.params.id)
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
    async deleteSolution() {
      this.clearValidation()
      this.dispatch()
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
