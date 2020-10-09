<template>
  <el-form ref="portfolioForm" label-position="top" @submit.native.prevent>
    <general-settings
      ref="generalSettings"
      :use-publish-rules="usePublishRules"
      :rules="rules"
      :draft-rules="draftRules"
      :publish-rules="publishRules"
      :api-errors="apiErrors"
    />
    <managers
      ref="managers"
      :use-publish-rules="usePublishRules"
      :rules="rules"
      :draft-rules="draftRules"
      :publish-rules="publishRules"
      :api-errors="apiErrors"
    />
    <problem-statement
      ref="problemStatement"
      :use-publish-rules="usePublishRules"
      :rules="rules"
      :draft-rules="draftRules"
      :publish-rules="publishRules"
      :api-errors="apiErrors"
    />
    <!-- action forms -->
    <div class="action-form">
      <el-button type="text" size="large" @click="handleCancel">
        <translate>Cancel</translate>
      </el-button>
      <el-button
        v-if="edit"
        type="text"
        size="large"
        class="create-btn"
        @click="handleEdit"
      >
        <translate>Save Portfolio</translate>
      </el-button>
      <el-button
        v-else
        type="text"
        size="large"
        class="create-btn"
        @click="handleCreate"
      >
        <translate>Add Portfolio</translate>
      </el-button>
    </div>
  </el-form>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { publishRules, draftRules } from '@/utilities/portfolio'
import GeneralSettings from '@/components/portfolio/form/GeneralSettings'
import Managers from '@/components/portfolio/form/Managers'
import ProblemStatement from '@/components/portfolio/form/ProblemStatement'

export default {
  components: {
    GeneralSettings,
    Managers,
    ProblemStatement,
  },
  $_veeValidate: {
    validator: 'new',
  },
  props: {
    edit: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      readyElements: 0,
      createdElements: 0,
      usePublishRules: false,
      apiErrors: {},
    }
  },
  computed: {
    ...mapGetters({
      portfolio: 'portfolio/getProjectData',
    }),
    draftRules,
    publishRules,
    rules() {
      return this.usePublishRules ? this.publishRules : this.draftRules
    },
  },
  mounted() {},
  beforeDestroy() {
    this.resetPortfolio()
  },
  methods: {
    ...mapActions({
      createPortfolio: 'portfolio/createPortfolio',
      editPortfolio: 'portfolio/editPortfolio',
      resetPortfolio: 'portfolio/resetPortfolio',
      setLoading: 'portfolio/setLoading',
    }),
    async unCaughtErrorHandler(errors) {
      // todo: change or tune in for portfolio
      if (this.$sentry) {
        this.$sentry.captureMessage(
          'Un-caught validation error in portfolio page',
          {
            level: 'error',
            extra: {
              apiErrors: this.apiErrors,
              errors,
            },
          }
        )
      }

      try {
        await this.$confirm(
          this.$gettext(
            'There was an un-caught validation error an automatic report has been submitted'
          ),
          this.$gettext('Warning'),
          {
            confirmButtonText: this.$gettext('Recover & Reload'),
            cancelButtonText: this.$gettext('Discard changes'),
          }
        )
        const portfolio = {
          ...this.portfolio,
        }
        const toStore = JSON.stringify(portfolio)
        window.localStorage.setItem('rescuedProject', toStore)
        const newUrl =
          window.location.origin +
          this.$route.path +
          `?reloadDataFromStorage=true`
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
        this.$refs.generalSettings.validate(),
      ])
      console.log('root validations', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    clearValidation() {
      this.apiErrors = {}
      this.$refs.generalSettings.clear()
    },
    async handleCreate() {
      this.clearValidation()
      this.usePublishRules = false
      await this.$nextTick(async () => {
        const general = await this.$refs.generalSettings.validateDraft()
        if (general) {
          try {
            // const id = await this.createPortfolio()
            const localised = this.localePath({
              name: 'organisation-portfolio-management',
            })
            this.$router.push(localised)

            this.$alert(
              this.$gettext('Your portfolio has been created successfully'),
              this.$gettext('Congratulation'),
              {
                confirmButtonText: this.$gettext('Close'),
              }
            )
            return
          } catch (e) {
            if (e.response) {
              this.apiErrors = e.response.data
            } else {
              console.error(e)
            }
          }
        }
        this.handleErrorMessages()
      })
    },
    async handleEdit() {
      this.clearValidation()
      this.usePublishRules = false
      await this.$nextTick(async () => {
        const general = await this.$refs.generalSettings.validateDraft()
        if (general) {
          try {
            // const id = await this.editPortfolio(this.$route.params.id)
            const localised = this.localePath({
              name: 'organisation-portfolio-management',
            })
            this.$router.push(localised)

            this.$alert(
              this.$gettext('Your portfolio has been updated successfully'),
              this.$gettext('Congratulation'),
              {
                confirmButtonText: this.$gettext('Close'),
              }
            )
            return
          } catch (e) {
            if (e.response) {
              this.apiErrors = e.response.data
            } else {
              console.error(e)
            }
          }
        }
        this.handleErrorMessages()
      })
    },
    handleCancel() {
      this.$router.push(
        this.localePath({ name: 'organisation-portfolio-management' })
      )
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.action-form {
  margin-top: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  button {
    width: 213px;
    height: 48px;
    padding: 14px 20px;
    border-radius: 0;
    background-color: #a8a8a9;
    font-size: 16px;
    font-weight: bold;
    color: @colorWhite!important;
    &:hover {
      background-color: #a8a8a9;
    }
  }
  .create-btn {
    color: @colorWhite;
    background-color: @colorBrandPrimary;
    &:hover {
      background-color: @colorBrandPrimary;
      opacity: 0.8;
    }
    &.is-disabled {
      color: #a8a8a9 !important;
      background-color: #f5f3ef;
      &:hover {
        background-color: #f5f3ef;
      }
    }
  }
}
</style>
