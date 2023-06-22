<template>
  <div class="NewProjectForm">
    <div v-show="!showForm" class="Loader">
      <div></div>
      <span><translate>Loading</translate></span>
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
            v-model="solution.general_overview"
          />
          <InnovationPortfolios
            key="innovationPortfolios"
            ref="innovationPortfolios"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
            v-model="solution.innovation_portfolios"
          />
          <ActivityAndReach
            key="solutionActivityAndReach"
            ref="solutionActivityAndReach"
            :use-publish-rules="usePublishRules"
            :rules="rules"
            :api-errors="apiErrors"
            @hook:mounted="mountedHandler"
            @hook:created="createdHandler"
            v-model="solution.activity_reach"
          />
        </el-col>
        <el-col :span="6">
          <FormActionsAside @save="handleSave" @cancel="handleCancel" :canDelete="false" />
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
import InnovationPortfolios from './sections/InnovationPortfolios.vue'
import FormActionsAside from './FormActionsAside.vue'

export default {
  components: {
    GeneralOverview,
    ActivityAndReach,
    FormActionsAside,
    InnovationPortfolios,
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
      solution: {
        general_overview: {
          name: '',
        },
        innovation_portfolios: {
          phase: 0,
          open_source_frontier_tech: false,
          learning_investment: false,
          portfolio_problem_statements: [],
        },
        activity_reach: {
          override_reach: null,
          people_reached: 0,
          country_solutions: [],
        },
      },
    }
  },
  computed: {
    ...mapGetters({
      getSolution: 'solution/getSolutionData',
    }),

    showForm() {
      return this.readyElements >= this.createdElements
    },
    rules,
  },

  methods: {
    ...mapActions({
      // createSolution: 'solution/createSolution',
      createNewSolution: 'solution/createNewSolution',
      deleteSolution: 'solution/deleteSolution',
      cancelSolution: 'solution/cancelSolution',
      setLoading: 'solution/setLoading',
    }),

    handleErrorMessages() {},
    async validate() {
      const validations = await Promise.all([
        this.$refs.solutionGeneral.validate(),
        this.$refs.solutionActivityAndReach.validate(),
        this.$refs.innovationPortfolios.validate(),
      ])
      console.log('root validations', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    clearValidation() {
      this.apiErrors = {}
      this.$refs.solutionGeneral.clear()
      this.$refs.solutionActivityAndReach.clear()
      this.$refs.innovationPortfolios.clear()
    },
    peopleReached(people_reached) {
      if (people_reached === undefined || people_reached === null) {
        return null
      } else {
        return people_reached
      }
    },
    goToViewSolution(id) {
      if (id) {
        const localised = this.localePath({
          name: 'organisation-portfolio-innovation-solutions-id',
          params: { ...this.$route.params, id },
        })
        this.$router.push(localised)
      } else {
        const localised = this.localePath({
          name: 'organisation-portfolio-innovation-solutions',
        })
        this.$router.push(localised)
      }
    },
    async handleSave() {
      // this.trimEmptyRows()

      // this.setLoading(true)
      // this.clearValidation()
      this.usePublishRules = true
      await this.$nextTick(async () => {
        const general = await this.$refs.solutionGeneral.validate()
        const solutionActivityAndReach = await this.$refs.solutionActivityAndReach.validate()
        const innovationPortfolios = await this.$refs.innovationPortfolios.validate()
        if (general && solutionActivityAndReach && innovationPortfolios) {
          const s = this.solution
          try {
            const response = await this.createNewSolution({
              name: s.general_overview.name,
              phase: s.innovation_portfolios.phase,
              open_source_frontier_tech: s.innovation_portfolios.open_source_frontier_tech,
              learning_investment: s.innovation_portfolios.learning_investment,
              portfolio_problem_statements: s.innovation_portfolios.portfolio_problem_statements,
              country_solutions: s.activity_reach.country_solutions,
              people_reached: this.peopleReached(s.activity_reach.override_reach),
            })
            this.goToViewSolution(response.data.id)

            this.$alert(this.$gettext('Your Solution has been created successfully'), this.$gettext('Congratulation'), {
              confirmButtonText: this.$gettext('Close'),
            })
            this.usePublishRules = false
            return
          } catch (e) {
            this.$alert(
              `${this.$gettext('Request failed, please retry, or contact support with code: ')} ${e.message}`,
              this.$gettext('Error'),
              {
                confirmButtonText: this.$gettext('Close'),
              }
            )
            if (e.response) {
              this.apiErrors = e.response.data
            } else {
              console.error(e)
              this.setLoading(false)
            }
          }
        } else {
          this.$alert(
            this.$gettext('Please correct all errors in required fields before save.'),
            this.$gettext('Error'),
            {
              confirmButtonText: this.$gettext('Close'),
            }
          )
        }
        this.handleErrorMessages()
        this.setLoading(false)
      })
    },
    async handleCancel() {
      try {
        await this.$confirm(
          this.$gettext('Any changes will be lost and you will be navigated to All Solutions page'),
          this.$gettext('Attention'),
          {
            confirmButtonText: this.$gettext('Ok'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning',
          }
        )
        await this.cancelSolution()
        const localised = this.localePath({
          name: 'organisation-portfolio-innovation-solutions',
          params: { ...this.$route.params },
        })
        this.$router.push(localised)
        this.$message({
          type: 'success',
          message: this.$gettext('Action canceled'),
        })
      } catch (e) {
        // this.setLoading(false)
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
            // await this.publishProject(this.$route.params.id)
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
            //this.setLoading(false)
            this.apiErrors = e.response.data ? e.response.data : 'error'
          }
        }
        this.handleErrorMessages()
        this.$nextTick(() => {
          const errors = [...this.$el.querySelectorAll('.is-error')]
          const visibleErrors = errors.filter((e) => e.offsetParent !== null)
          if (visibleErrors && visibleErrors.length > 0) {
            visibleErrors[0].scrollIntoView()
          } else {
            this.unCaughtErrorHandler(errors)
          }
        })
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
