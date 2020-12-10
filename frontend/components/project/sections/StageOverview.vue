<template>
  <div id="stages" class="StageOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Completion of initiative stages') | translate"
      show-legend
    >
      <!-- stages -->
      <el-row>
        <!-- research section -->
        <!-- <el-col :span="24">
          <div class="research">
            <el-switch
              v-model="research"
              active-color="#008DC9"
              :disabled="researchDisabled"
            />
            <p class="research__switch">
              <translate key="research-project-title">
                Set initiative as ‘Research initiative’
              </translate>
            </p>
            <p class="info">
              <fa icon="info-circle" class="info__icon" />
              <span>
                <translate key="research-project-info">
                  If your initiative is focused on research activities, please
                  indicate here. The unique initiative ID can be shared as a
                  reference during in your publication.
                </translate>
              </span>
            </p>
          </div>
        </el-col> -->
        <!-- research section -->
        <!-- Start date section -->
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('start_date')"
            :draft-rule="draftRules.start_date"
            :publish-rule="publishRules.start_date"
          >
            <template slot="label">
              <translate key="start-date">
                Set start date of initiative
              </translate>
              <tooltip
                :text="$gettext('Date format: YYYY-MM-DD') | translate"
              />
            </template>
            <p class="info info--free-margin">
              <fa icon="info-circle" class="info__icon" />
              <span>
                <translate key="research-project-info">
                  When your initiative activities have completed, you can
                  indicated by setting the end of the initiative. Note that the
                  initiative will still be visible on the global map as a
                  completed initiative.
                </translate>
              </span>
            </p>
            <safe-date-picker
              ref="Start date"
              v-model="start_date"
              v-validate="rules.start_date"
              :placeholder="$gettext('Pick a date (required)') | translate"
              data-vv-name="start_date"
              data-vv-as="Start date"
              class="Date"
              align="left"
            />
          </custom-required-form-item>
        </el-col>
        <!-- Stages section -->
        <el-col :span="24">
          <el-row class="stages">
            <custom-required-form-item>
              <template slot="label">
                <translate key="stages">
                  Set current and previous stages of initiative
                </translate>
              </template>
              <el-col
                v-for="(stage, idx) in stagesDraft"
                :key="stage.id"
                :span="24"
                :class="`stage ${stage.checked ? 'active' : ''}`"
              >
                <p class="stage__number">{{ idx + 1 }}.</p>
                <el-checkbox
                  :value="stage.checked"
                  class="stage__checkbox"
                  :label="stage.id"
                  @input="
                    updateStagesDraft(stage.id, 'checked', !stage.checked)
                  "
                >
                  {{ stage.name }}
                  <el-tooltip
                    v-if="stage.tooltip && !stage.checked"
                    effect="dark"
                    :content="stage.tooltip"
                    placement="right"
                    popper-class="stages__tooltip"
                  >
                    <fa icon="question-circle" class="info__icon" />
                  </el-tooltip>
                </el-checkbox>
                <transition name="toggle">
                  <div v-if="stage.checked" class="stage__form">
                    <p v-if="stage.tooltip" class="info stage__info">
                      <span>
                        <translate :key="`stage-tooltip-${idx + 1}`">
                          {{ stage.tooltip }}
                        </translate>
                      </span>
                    </p>
                    <custom-required-form-item
                      class="stage__picker"
                      :error="!stage.date ? stageDateError : ''"
                    >
                      <safe-date-picker
                        v-validate="rules.note_date"
                        :value="stage.date"
                        :placeholder="
                          $gettext('Pick a date (required)') | translate
                        "
                        data-vv-name="note_date"
                        data-vv-as="Note date"
                        class="Date stage__input--full"
                        align="left"
                        @input="updateStagesDraft(stage.id, 'date', $event)"
                      />
                    </custom-required-form-item>
                    <custom-required-form-item class="stage__input">
                      <el-input
                        :value="stage.note"
                        :placeholder="
                          $gettext('Add note (optional)') | translate
                        "
                        class="stage__input--full"
                        @input="updateStagesDraft(stage.id, 'note', $event)"
                      >
                        <i
                          slot="prefix"
                          class="el-input__icon el-icon-document"
                        />
                      </el-input>
                    </custom-required-form-item>
                  </div>
                </transition>
              </el-col>
            </custom-required-form-item>
          </el-row>
        </el-col>
        <!-- End date section -->
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('end_date') || endDateError"
            :draft-rule="draftRules.end_date"
            :publish-rule="publishRules.end_date"
          >
            <template slot="label">
              <translate key="end-date">
                Set end stage of initiative
              </translate>
              <tooltip
                :text="$gettext('Date format: YYYY-MM-DD') | translate"
              />
            </template>
            <p class="info info--free-margin">
              <fa icon="info-circle" class="info__icon" />
              <span>
                <translate key="research-project-info">
                  An estimated end date for the Initiative. This could refer to
                  the end of a programme cycle, humanitarian response plan,
                  hand-over to government, etc.
                </translate>
              </span>
            </p>

            <el-row type="flex">
              <safe-date-picker
                v-model="end_date"
                v-validate="rules.end_date"
                :placeholder="$gettext('Pick a date (optional)') | translate"
                data-vv-name="end_date"
                data-vv-as="End date"
                align="left"
              />

              <el-input
                key="end_date_note"
                v-model="end_date_note"
                v-validate="rules.end_date_note"
                class="note"
                data-vv-name="end_date_note"
                data-vv-as="End date note"
                :placeholder="$gettext('Add note (optional)') | translate"
              >
                <i slot="prefix" class="el-input__icon el-icon-document" />
              </el-input>
            </el-row>
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import { isAfter } from 'date-fns'
import { mapState, mapActions } from 'vuex'
import { mapGettersActions } from '@/utilities/form'
import Tooltip from '@/components/common/Tooltip'
import CollapsibleCard from '@/components/project/CollapsibleCard'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'

export default {
  components: {
    CollapsibleCard,
    Tooltip,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  data() {
    return {
      researchDisabled: false,
    }
  },
  computed: {
    ...mapState({
      stagesDraft: (state) => state.project.stagesDraft,
      stateObj: (state) => state.project,
    }),
    ...mapGettersActions({
      start_date: ['project', 'getStartDate', 'setStartDate', 0],
      end_date: ['project', 'getEndDate', 'setEndDate', 0],
      end_date_note: ['project', 'getEndDateNote', 'setEndDateNote', 0],
      research: ['project', 'getResearch', 'setResearch', 0],
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
    stageDateError() {
      if (
        this.stagesDraft &&
        this.stagesDraft.filter(
          (i) => i.checked && (i.date === '' || i.date === null)
        ).length > 0
      ) {
        return this.$gettext('Stage date is required')
      }
      return ''
    },
  },
  mounted() {
    this.loadStagesDraft()
    // research custom logic
    if (this.research === undefined) {
      // this.researchDisabled = false
      this.research = false
    } else {
      // this.researchDisabled = true
    }
    // eslint-disable-next-line no-self-assign
    this.start_date = this.start_date
  },
  methods: {
    ...mapActions({
      loadStagesDraft: 'project/loadStagesDraft',
    }),
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate(),
        Promise.resolve(this.endDateError === ''),
        Promise.resolve(this.stageDateError === ''),
      ])
      console.log('Initiative stages published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('start_date'),
        this.$validator.validate('end_date'),
        Promise.resolve(this.stageDateError === ''),
      ])
      console.log('Initiative stages draft validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    updateStagesDraft(id, key, value) {
      this.$store.dispatch(
        'project/setStagesDraft',
        this.stagesDraft.map((item) => {
          if (item.id === id) {
            return { ...item, [key]: value }
          }
          return item
        }),
        { root: true }
      )
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.stages__tooltip {
  max-width: 320px;
}

.StageOverview {
  .research {
    width: 721px;
    max-width: 721px;
    margin-bottom: 30px;
  }
  .research__switch {
    font-size: @fontSizeBase;
    margin-left: 8px;
    display: inline;
  }
  .info {
    margin-top: 24px;
    margin-bottom: 0px;
    font-size: @fontSizeSmall;
    color: @colorTextSecondary;
    display: flex;
    line-height: 18px;
  }
  .info--free-margin {
    margin-top: 0;
    margin-bottom: 25px;
  }
  .info__icon {
    color: @colorTextMuted;
    margin-right: 8px;
    margin-top: 3px;
  }

  .stages {
    color: @colorTextMuted;
  }
  .stage {
    &:hover,
    &.active {
      .stage__number {
        color: @colorTextPrimary;
      }
      .stage__checkbox {
        color: @colorTextPrimary;
        .el-checkbox__inner {
          border-color: @colorTextPrimary;
        }
      }
    }
    &.active {
      .stage__checkbox {
        .el-checkbox__inner {
          border-color: @colorBrandPrimary;
        }
      }
    }
  }
  .stage__checkbox {
    color: @colorTextMuted;
    .el-checkbox__inner {
      border-color: @colorTextMuted;
      border-radius: 2px;
    }
  }
  .stage__number {
    display: inline-block;
    width: 20px;
    margin-right: 16px;
  }
  .stage__form {
    border-left: 5px solid @colorGrayLight;
    margin-left: 44px;
    padding: 12px 0 12px 14px;
    display: flex;
    flex-wrap: wrap;
  }
  .stage__info {
    flex-basis: 100%;
    // margin: 0 0 16px 0;
    margin: 0 0 16px 0;
  }
  .stage__picker {
    flex-basis: 30%;
    margin-right: 20px;
  }
  .stage__input {
    flex-basis: 67%;
  }
  .stage__input--full {
    width: 100%;
  }
  .note {
    width: 518px;
    margin-left: auto;
  }
}
// animation toggle
.toggle-enter {
  opacity: 0;
  max-height: 0px;
}

.toggle-enter-active,
.toggle-leave-active {
  transition: all 0.5s ease-out;
  max-height: 98px;
}

.toggle-leave-to {
  opacity: 0;
  max-height: 0px;
}
</style>
