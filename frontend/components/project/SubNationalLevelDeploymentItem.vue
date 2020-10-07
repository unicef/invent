<template>
  <div class="SubNationalLevelDeploymentItem">
    <custom-required-form-item
      :error="errors.first('district', scope + '_' + index)"
      :draft-rule="draftRules.district"
      :publish-rule="publishRules.district"
    >
      <template slot="label">
        {{ levelName }}
      </template>

      <lazy-el-select
        v-model="subLevel"
        v-validate="rules.district"
        :data-vv-as="levelName"
        :data-vv-scope="scope + '_' + index"
        :placeholder="$gettext('Select from list') | translate"
        data-vv-name="district"
        filterable
        popper-class="SubNationalLevelDeploymentRegionDropdown"
        class="SubNationalLevelDeployementRegion"
      >
        <el-option
          v-for="sub in availableSubLevels"
          :key="sub.id"
          :label="sub.name"
          :value="sub.id"
        />
      </lazy-el-select>
      <facility-selector
        ref="facilitySelector"
        v-model="facilitiesList"
        :rules="rules"
        :draft-rules="draftRules"
        :publish-rules="publishRules"
        :api-errors="apiErrors"
        :disabled="!subLevel"
        :scope="scope + '_' + index"
      />
      <coverage-fieldset
        ref="coverageFieldset"
        :rules="rules"
        :api-errors="apiErrors"
        :health-workers.sync="healthWorkers"
        :clients.sync="clients"
        :facilities.sync="facilities"
        :disabled="!subLevel"
        :draft-rules="draftRules"
        :publish-rules="publishRules"
        :scope="scope + '_' + index"
      />
    </custom-required-form-item>
  </div>
</template>

<script>
import VeeValidationMixin from '../mixins/VeeValidationMixin.js'

import { mapGettersActions } from '../../utilities/form'
import CoverageFieldset from './CoverageFieldset'
import FacilitySelector from './FacilitySelector'

export default {
  components: {
    CoverageFieldset,
    FacilitySelector,
  },
  mixins: [VeeValidationMixin],
  props: {
    index: {
      type: [Number],
      default: null,
    },
    levelName: {
      type: String,
      required: true,
    },
    subLevels: {
      type: Array,
      required: true,
    },
    coverage: {
      type: Array,
      default: () => [],
    },
    scope: {
      type: String,
      required: true,
    },
    draftRules: {
      type: Object,
      default: null,
    },
    publishRules: {
      type: Object,
      default: null,
    },
  },
  computed: {
    ...mapGettersActions({
      coverageData: ['project', 'getCoverageData', 'setCoverageData', 0],
    }),
    subLevel: {
      get() {
        return this.coverage[this.index]
      },
      set(value) {
        const cov = [...this.coverage]
        cov[this.index] = value
        this.$emit('update:coverage', cov)
      },
    },
    availableSubLevels() {
      return this.subLevels.filter(
        (tp) =>
          !this.coverage.some((s) => s === tp.id) || tp.id === this.subLevel
      )
    },
    localCoverageData() {
      return this.coverageData[this.subLevel]
    },
    facilitiesList: {
      get() {
        const facilitiesList = this.localCoverageData
          ? this.localCoverageData.facilities_list
          : []
        return facilitiesList || []
      },
      set(value) {
        const coverage = {
          facilities_list: [...value],
          facilities: value.length,
        }
        this.coverageData = { coverage, subLevel: this.subLevel }
      },
    },
    healthWorkers: {
      get() {
        return this.localCoverageData
          ? this.localCoverageData.health_workers
          : null
      },
      set(value) {
        const coverage = { health_workers: value }
        this.coverageData = { coverage, subLevel: this.subLevel }
      },
    },
    clients: {
      get() {
        return this.localCoverageData ? this.localCoverageData.clients : null
      },
      set(value) {
        const coverage = { clients: value }
        this.coverageData = { coverage, subLevel: this.subLevel }
      },
    },
    facilities: {
      get() {
        return this.localCoverageData ? this.localCoverageData.facilities : null
      },
      set(value) {
        const coverage = { facilities: value }
        this.coverageData = { coverage, subLevel: this.subLevel }
      },
    },
  },
  methods: {
    clear() {
      this.errors.clear()
      this.$validator.clear()
      this.$refs.coverageFieldset.clear()
      this.$refs.facilitySelector.clear()
    },
    async validate() {
      const validations = await Promise.all([
        this.$validator.validate(),
        this.$refs.coverageFieldset.validate(),
        this.$refs.facilitySelector.validate(),
      ])
      console.log(
        `sub national level deployment item ${this.scope}`,
        validations
      )
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.SubNationalLevelDeployementRegion {
  width: 100%;
  margin-bottom: 20px;
}
</style>
