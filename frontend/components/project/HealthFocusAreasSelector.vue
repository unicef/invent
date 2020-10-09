<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select from list') | translate"
    multiple
    filterable
    popper-class="HealthFocusAreasSelectorDropdown"
    class="HealthFocusAreasSelector"
    @change="changeHandler"
  >
    <el-option-group
      v-for="group in healthFocusAreas"
      :key="group.id"
      :label="group.name"
    >
      <el-option
        v-for="hfa in group.health_focus_areas"
        :key="hfa.id"
        :label="hfa.name"
        :value="hfa.id"
      />
    </el-option-group>
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Array,
      default: null,
    },
  },
  data() {
    return {
      open: false,
    }
  },
  computed: {
    ...mapGetters({
      healthFocusAreas: 'projects/getHealthFocusAreas',
    }),
  },
  methods: {
    changeHandler(value) {
      this.$emit('change', value)
    },
    toggleHandler(value) {
      if (value) {
        this.open = value
      }
    },
  },
}
</script>

<style lang="less">
.HealthFocusAreasSelector {
  width: 100%;
}
.HealthFocusAreasSelectorDropdown {
}
</style>
