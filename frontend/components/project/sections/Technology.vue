<template>
  <div id="technology" class="GeneralOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Technology') | translate"
      show-legend
    >
      <custom-required-form-item
        :error="errors.first('platforms')"
        :draft-rule="draftRules.platforms"
        :publish-rule="publishRules.platforms"
      >
        <template slot="label">
          <translate key="platform-label">
            Select all the software platform(s) used in the deployment of the
            initiative.
          </translate>
        </template>
        <template slot="tooltip">
          <el-tooltip
            class="item"
            content="If you encounter an error and/or can not locate
                the software platform in this list, please send a request
                to add additional products to invent@unicef.org "
            placement="right"
          >
            <i class="el-icon-warning warning" />
          </el-tooltip>
        </template>
        <platform-selector
          v-model="platforms"
          v-validate="rules.platforms"
          data-vv-name="platforms"
          data-vv-as="Software"
        />
      </custom-required-form-item>

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
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="If you encounter an error and/or can not locate the
                hardware platform in this list, please send a request to add
                additional platforms to invent@unicef.org "
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
            </template>
            <multi-selector
              v-model="hardware"
              v-validate="rules.hardware"
              data-vv-name="hardware"
              data-vv-as="Hardware Platform(s) and Physical Product(s)"
              source="getHardware"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Only complete this field if there is a significant hardware or
                  Product Innovation as part of the initiative.
                </translate>
              </p>
            </span>
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
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="If you encounter an error and/or can not locate
                the entry you would like to see in this list, please send
                a request with details to invent@unicef.org "
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
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
                  Only complete this field if the initiative includes
                  organisational methods and processes ('soft'
                  technologies/innovations).
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
            <template slot="tooltip">
              <el-tooltip
                class="item"
                content="If you encounter an error and/or can not locate
                the entry you would like to see in this list, please send
                a request with details to invent@unicef.org "
                placement="right"
              >
                <i class="el-icon-warning warning" />
              </el-tooltip>
            </template>
            <multi-selector
              v-model="functions"
              v-validate="rules.functions"
              data-vv-name="functions"
              data-vv-as="Function(s) of Platform"
              source="getFunctions"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Platform functions represent the types of ICT applications,
                  innovations and information systems designed to enable
                  programmes.
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
import MultiSelector from '@/components/project/MultiSelector'
import { mapGetters } from 'vuex'
import { mapGettersActions } from '@/utilities/form'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import PlatformSelector from '../PlatformSelector'

export default {
  components: {
    CollapsibleCard,
    MultiSelector,
    PlatformSelector,
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
      platforms: ['project', 'getPlatforms', 'setPlatforms', 0],
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
