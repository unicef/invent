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
    <metrics
      ref="metrics"
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
        <translate>Dismiss changes</translate>
      </el-button>
      <el-button v-if="edit" type="text" size="large" class="create-btn" @click="handleEdit">
        <translate>Save Portfolio</translate>
      </el-button>
      <el-button v-else type="text" size="large" class="create-btn" @click="handleCreate">
        <translate>Add Portfolio</translate>
      </el-button>
    </div>
  </el-form>
</template>

<script>
import isEmpty from 'lodash/isEmpty'
import join from 'lodash/join'

import { mapActions } from 'vuex'
import { publishRules, draftRules } from '@/utilities/portfolio'
import GeneralSettings from '@/components/portfolio/form/GeneralSettings'
import Managers from '@/components/portfolio/form/Managers'
import ProblemStatement from '@/components/portfolio/form/ProblemStatement'
import Metrics from '@/components/portfolio/form/Metrics.vue'

export default {
  components: {
    GeneralSettings,
    Managers,
    ProblemStatement,
    Metrics,
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
    draftRules,
    publishRules,
    rules() {
      return this.usePublishRules ? this.publishRules : this.draftRules
    },
  },
  methods: {
    ...mapActions({
      createPortfolio: 'portfolio/createPortfolio',
      editPortfolio: 'portfolio/editPortfolio',
      setLoading: 'portfolio/setLoading',
    }),
    async unCaughtErrorHandler(errors) {
      const errorList = Object.entries(this.apiErrors).map((e) => {
        if (e[0] === 'problem_statements') {
          return `${e[0]}: ${join(
            e[1].map((problem) => problem.description),
            '\n'
          )}`
        }
        return `${e[0]}: ${e[1]}`
      })

      console.log(errorList)
      await this.$confirm(
        isEmpty(this.apiErrors)
          ? this.$gettext('There was an un-caught validation error an automatic report has been submitted')
          : join(errorList, '\n'),
        this.$gettext('Warning'),
        {
          confirmButtonText: this.$gettext('Reload'),
        }
      )
      window.location.reload(true)
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
      const validations = await Promise.all([this.$refs.generalSettings.validate(), this.$refs.metrics.validate()])
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
        const general = await this.validate()

        if (general) {
          try {
            await this.createPortfolio()
            const localised = this.localePath({
              name: 'organisation-portfolio-innovation-id',
              params: { id: this.$route.params.id },
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
        } else {
          this.$alert(
            this.$gettext('Please correct all errors in required fields before save.'),
            this.$gettext('Error'),
            {
              confirmButtonText: this.$gettext('Close'),
            }
          )
        }
        // this.handleErrorMessages()
      })
    },
    async handleEdit() {
      this.clearValidation()
      this.usePublishRules = false
      await this.$nextTick(async () => {
        const general = await this.validate()

        if (general) {
          try {
            // const id = await this.editPortfolio(this.$route.params.id)
            await this.editPortfolio(this.$route.params.id)
            const localised = this.localePath({
              name: 'organisation-portfolio-innovation-id',
              params: { id: this.$route.params.id },
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
        } else {
          this.$alert(
            this.$gettext('Please correct all errors in required fields before save.'),
            this.$gettext('Error'),
            {
              confirmButtonText: this.$gettext('Close'),
            }
          )
        }
        // this.handleErrorMessages()
      })
    },
    handleCancel() {
      this.$router.push(
        this.localePath({ name: 'organisation-portfolio-innovation-id', params: { id: this.$route.params.id } })
      )
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

&::v-deep {
  .el-input__inner,
  .el-textarea__inner {
    border: 1px solid #a8a8a9;
  }
  .el-tag.el-tag--info {
    background-color: #f5f3ef;
    border: none;
    padding: 3px 9px;
    .el-tag__close {
      color: #a8a8a9;
    }
  }
  .el-select .el-tag {
    box-sizing: inherit;
  }
  .el-select .el-tag__close.el-icon-close {
    background-color: transparent;
  }
  .el-tag .el-icon-close {
    font-size: 18px;
    height: 18px;
    width: 18px;
  }
}

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
      opacity: 0.8;
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
