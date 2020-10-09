<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="multiple"
    :disabled="disabled"
    :placeholder="$gettext('Select Unicef office') | translate"
    filterable
    class="select-office"
  >
    <el-option
      v-for="office in officeList"
      :key="office.id"
      :label="office.name"
      :value="office.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [Number, Array],
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
      required: false,
    },
    multiple: {
      type: Boolean,
      default: false,
      required: false,
    },
    regionFilter: {
      type: [Number, String],
      default: undefined,
    },
  },
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
    }),
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    officeList() {
      if (
        this.regionFilter === undefined ||
        this.regionFilter === null ||
        typeof this.regionFilter !== 'number'
      ) {
        return this.offices
      }
      return this.offices
        ? this.offices.filter((office) => office.region === this.regionFilter)
        : []
    },
  },
  mounted() {
    this.loadOffices()
  },
  methods: {
    ...mapActions({
      loadOffices: 'offices/loadOffices',
    }),
  },
}
</script>

<style lang="less" scoped>
.select-office {
  width: 100%;
}
</style>
