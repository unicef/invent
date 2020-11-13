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
              <translate key="start-date">
                Please select the date the initiative was started.
              </translate>
            </template>
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="Date format: YYYY-MM-DD"
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
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
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  The official start of the initiative. This could be a launch,
                  meeting with government partners, signing of concept note,
                  inclusion in workplan, etc.
                </translate>
              </p>
            </span>
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

            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Come back and update the status as the initiative progresses.
                  For a detailed overview of each stage visit:
                  https://uni.cf/invent-help
                </translate>
              </p>
            </span>
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
              <translate key="end-date">
                What is the (projected) end date of the initiative?
              </translate>
            </template>
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="Date format: YYYY-MM-DD"
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
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
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  An estimated end date for the Initiative. This could refer to
                  the end of a programme cycle, humanitarian response plan,
                  hand-over to government, etc.
                </translate>
              </p>
            </span>
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

export default {
  components: {
    CollapsibleCard,
    SingleSelect,
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
