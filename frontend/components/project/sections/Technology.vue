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
        <select-box
          v-model="platforms"
          v-validate="rules.platforms"
          filterable
          multiple
          source="software"
          data-vv-name="platforms"
          :options="softwareList"
          :new-info-title="newInfoSoftware"
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
            <select-box
              v-model="hardware"
              v-validate="rules.hardware"
              filterable
              multiple
              source="hardware"
              data-vv-name="hardware"
              :options="hardwareList"
              :new-info-title="newInfoHardware"
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
            <select-box
              v-model="nontech"
              v-validate="rules.nontech"
              filterable
              multiple
              source="nontech"
              data-vv-name="nontech"
              :options="nontechList"
              :new-info-title="newInfoNontech"
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
            <select-box
              v-model="functions"
              v-validate="rules.functions"
              filterable
              multiple
              source="function"
              data-vv-name="functions"
              :options="functionList"
              :new-info-title="newInfoFunction"
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
      <el-row :gutter="20" type="flex">
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('isc')"
            :draft-rule="draftRules.isc"
            :publish-rule="publishRules.isc"
          >
            <template slot="label">
              <translate key="isc-label">
                Has the initiative completed a Information Security
                Classification via UNICEF's Classi Tool?
              </translate>
            </template>

            <single-select
              v-model="isc"
              v-validate="rules.isc"
              data-vv-name="isc"
              data-vv-as="Information Security"
              source="projects/getInfoSec"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  All digital initiatives at UNICEF are required to undertake an
                  information security risk classification. Classi is a UNICEF
                  tool that helps to prioritize and define UNICEF information
                  assets, their value and how we shall protect them. It helps
                  evaluate the risk associated in the information in case there
                  is a loss in confidentiality, integrity and availability. For
                  more info visit: https://uni.cf/CLASSI
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
// import MultiSelector from '@/components/project/MultiSelector'
import { mapGetters } from 'vuex'
import { mapGettersActions } from '@/utilities/form'
// import PlatformSelector from '@/components/project/PlatformSelector'
import SelectBox from '@/components/project/SelectBox'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import SingleSelect from '~/components/common/SingleSelect'

export default {
  components: {
    CollapsibleCard,
    SingleSelect,
    SelectBox,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  data() {
    return {
      newInfoSoftware: this.$gettext(
        'DHA Admin will update the Software list to include your new software name'
      ),
      newInfoHardware: this.$gettext(
        'DHA Admin will update the Hardware list to include your new hardware name'
      ),
      newInfoNontech: this.$gettext(
        'DHA Admin will update the Nontech list to include your new nontech name'
      ),
      newInfoFunction: this.$gettext(
        'DHA Admin will update the Function list to include your new function name'
      ),
    }
  },
  computed: {
    ...mapGetters({
      modified: 'project/getModified',
      softwareList: 'projects/getTechnologyPlatforms',
      hardwareList: 'projects/getHardware',
      nontechList: 'projects/getNontech',
      functionList: 'projects/getFunctions',
    }),
    ...mapGettersActions({
      hardware: ['project', 'getHardware', 'setHardware', 0],
      functions: ['project', 'getFunctions', 'setFunctions', 0],
      nontech: ['project', 'getNontech', 'setNontech', 0],
      platforms: ['project', 'getPlatforms', 'setPlatforms', 0],
      isc: ['project', 'getInfoSec', 'setInfoSec', 0],
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
        this.$validator.validate('platforms'),
        this.$validator.validate('isc'),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less"></style>
