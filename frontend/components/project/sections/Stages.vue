<template>
  <div id="phase" class="GeneralOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Phase') | translate"
      show-legend
    >
      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('start_date')"
            :draft-rule="draftRules.start_date"
            :publish-rule="publishRules.start_date"
          >
            <template slot="label">
              <translate key="start-date"> Initiative start date </translate>
              <form-hint>
                <translate key="start-date-hint">
                  When did the overall project, not just the digital health
                  component, start.
                </translate>
              </form-hint>
            </template>

            <SafeDatePicker
              ref="Start date"
              v-model="start_date"
              v-validate="rules.start_date"
              :placeholder="$gettext('Start date') | translate"
              data-vv-name="start_date"
              data-vv-as="Start date"
              class="Date"
              align="left"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('phase')"
            :draft-rule="draftRules.phase"
            :publish-rule="publishRules.phase"
          >
            <template slot="label">
              <translate key="phase-label">
                Please select which phase the initiative has reached to date.
              </translate>
            </template>

            <single-select
              v-model="phase"
              v-validate="rules.phase"
              data-vv-name="phase"
              data-vv-as="Phase of Initiative"
              source="projects/getPhases"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('end_date') || endDateError"
            :draft-rule="draftRules.end_date"
            :publish-rule="publishRules.end_date"
          >
            <template slot="label">
              <translate key="end-date"> Initiative end date </translate>
              <form-hint>
                <translate key="end-date-hint">
                  When will the overall project be completed. If your project is
                  ongoing, leave this field blank.
                </translate>
              </form-hint>
            </template>

            <SafeDatePicker
              v-model="end_date"
              v-validate="rules.end_date"
              :placeholder="$gettext('End date') | translate"
              data-vv-name="end_date"
              data-vv-as="End date"
              class="Date"
              align="left"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import SingleSelect from '@/components/common/SingleSelect'
import { mapGetters } from 'vuex'
import { isAfter } from 'date-fns'
import { mapGettersActions } from '@/utilities/form'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import FormHint from '../FormHint'

export default {
  components: {
    CollapsibleCard,
    SingleSelect,
    FormHint,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified',
    }),
    ...mapGettersActions({
      phase: ['project', 'getPhase', 'setPhase', 0],
      start_date: ['project', 'getStartDate', 'setStartDate', 0],
      end_date: ['project', 'getEndDate', 'setEndDate', 0],
    }),
    endDateError() {
      if (
        this.usePublishRules &&
        this.start_date &&
        this.end_date &&
        isAfter(this.start_date, this.end_date)
      ) {
        return this.$gettext('End date must be after Start date')
      }
      return ''
    },
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate(),
        Promise.resolve(this.endDateError === ''),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate('phase')])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
