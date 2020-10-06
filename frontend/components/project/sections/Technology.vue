<template>
  <div id="Technology" class="GeneralOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Technology') | translate"
      show-legend
    >
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('hardware')"
            :draft-rule="draftRules.hardware"
            :publish-rule="publishRules.hardware"
          >
            <template slot="label">
              <translate key="hardware-label">
                Please select all the hardware platform(s) used in the
                deployment of the initiative.
              </translate>
            </template>

            <multi-selector
              v-model="hardware"
              v-validate="rules.hardware"
              data-vv-name="hardware"
              data-vv-as="Hardware Platform(s) and Physical Product(s)"
              source="getHardware"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('nontech')"
            :draft-rule="draftRules.nontech"
            :publish-rule="publishRules.nontech"
          >
            <template slot="label">
              <translate key="nontech-label">
                Please select all the Progamme Innovation and Non-Technology
                platform(s) used in the deployment of the initiative.
              </translate>
            </template>

            <multi-selector
              v-model="nontech"
              v-validate="rules.nontech"
              data-vv-name="nontech"
              data-vv-as="Programme Innovation(s) and Non-Technology Platform(s)"
              source="getNontech"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Examples of Progamme Innovation and Non-Technology platform(s)
                  include, but are not limited to, UpShift, Innovative Finance,
                  Partnerships, etc.
                </translate>
              </p>
            </span>
          </custom-required-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('functions')"
            :draft-rule="draftRules.functions"
            :publish-rule="publishRules.functions"
          >
            <template slot="label">
              <translate key="functions-label">
                Please select all applicable functions the platform performs.
              </translate>
            </template>

            <multi-selector
              v-model="functions"
              v-validate="rules.functions"
              data-vv-name="functions"
              data-vv-as="Function(s) of Platform"
              source="getFunctions"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import MultiSelector from '@/components/project/MultiSelector'
import { mapGetters } from 'vuex'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import { mapGettersActions } from '../../../utilities/form'

export default {
  components: {
    CollapsibleCard,
    MultiSelector,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified',
    }),
    ...mapGettersActions({
      hardware: ['project', 'getHardware', 'setHardware', 0],
      functions: ['project', 'getFunctions', 'setFunctions', 0],
      nontech: ['project', 'getNontech', 'setNontech', 0],
    }),
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('hardware'),
        this.$validator.validate('nontech'),
        this.$validator.validate('functions'),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less"></style>
