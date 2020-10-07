<template>
  <div class="CoverageFieldset">
    <el-row :gutter="20" type="flex">
      <el-col :span="8">
        <custom-required-form-item
          :error="errors.first('health_workers', scope)"
          :draft-rule="draftRules.health_workers"
          :publish-rule="publishRules.health_workers"
        >
          <template slot="label">
            <translate key="health-workers">
              How many health workers use the system?
            </translate>
            <form-hint>
              <translate key="health-workers-hint">
                Health workers include all recognized health professionals
                directly accessing the software. If there are no users of this
                type, put 0.
              </translate>
            </form-hint>
          </template>

          <el-input
            v-model="localHealthWorkers"
            v-validate="rules.health_workers"
            :disabled="disabled"
            :data-vv-scope="scope"
            data-vv-name="health_workers"
            data-vv-as="Health workers"
            type="number"
            min="0"
            max="10000000"
            step="1"
          />
        </custom-required-form-item>
      </el-col>
      <el-col :span="8">
        <custom-required-form-item
          :error="errors.first('facilities', scope)"
          :draft-rule="draftRules.facilities"
          :publish-rule="publishRules.facilities"
        >
          <template slot="label">
            <translate key="facilities">
              How many facilities use the system?
            </translate>
            <form-hint>
              <translate key="facilities-hint">
                Health facilities using the system refers to all facilities that
                have direct access to the software. If there are no users of
                this type, put 0.
              </translate>
            </form-hint>
          </template>

          <el-input
            v-model="localFacilities"
            v-validate="rules.facilities"
            :disabled="disableFacilities"
            :data-vv-scope="scope"
            data-vv-name="facilities"
            data-vv-as="Facilities"
            type="number"
            min="0"
            max="10000000"
            step="1"
          />
        </custom-required-form-item>
      </el-col>
      <el-col :span="8">
        <custom-required-form-item
          :error="errors.first('clients', scope)"
          :draft-rule="draftRules.clients"
          :publish-rule="publishRules.clients"
        >
          <template slot="label">
            <translate key="facilities">
              How many clients use the system?
            </translate>
            <form-hint>
              <translate key="facilities-hint">
                Client users refers to all care recipients who have direct
                access to the software. If there are no users of this type, put
                0.
              </translate>
            </form-hint>
          </template>
          <el-input
            v-model="localClients"
            v-validate="rules.clients"
            :disabled="disabled"
            :data-vv-scope="scope"
            data-vv-name="clients"
            data-vv-as="Clients"
            type="number"
            min="0"
            max="10000000"
            step="1"
          />
        </custom-required-form-item>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import VeeValidationMixin from '../mixins/VeeValidationMixin.js'
import FormHint from './FormHint'

export default {
  components: {
    FormHint,
  },
  mixins: [VeeValidationMixin],
  props: {
    disabled: {
      type: Boolean,
      default: true,
    },
    healthWorkers: {
      type: [Number, String],
      default: null,
    },
    clients: {
      type: [Number, String],
      default: null,
    },
    facilities: {
      type: [Number, String],
      default: null,
    },
    isNlc: {
      type: Boolean,
      default: false,
    },
    scope: {
      type: String,
      default: null,
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
    ...mapGetters({
      country: 'project/getCountry',
      getFacilities: 'countries/getCountryFacilityList',
    }),
    hasFacilityList() {
      return !!this.getFacilities(this.country).length
    },
    disableFacilities() {
      if (this.isNlc) {
        return false
      }
      return !!(this.disabled || this.hasFacilityList)
    },
    localHealthWorkers: {
      get() {
        return this.healthWorkers
      },
      set(value) {
        this.$emit('update:healthWorkers', value)
      },
    },
    localClients: {
      get() {
        return this.clients
      },
      set(value) {
        this.$emit('update:clients', value)
      },
    },
    localFacilities: {
      get() {
        return this.facilities
      },
      set(value) {
        this.$emit('update:facilities', value)
      },
    },
  },
  methods: {
    validate() {
      return this.$validator.validate()
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.CoverageFieldset {
  .el-form-item__label {
    line-height: 20px;
    height: 50px;
  }
}
</style>
