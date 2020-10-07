<template>
  <el-checkbox-group :value="value" class="OnePerRow" @input="changeHandler">
    <el-checkbox
      v-for="license in licenses"
      :key="license.id"
      :label="license.id"
    >
      {{ license.name }}
    </el-checkbox>
  </el-checkbox-group>
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
      default: () => [],
    },
  },
  computed: {
    ...mapGetters({
      licenses: 'projects/getLicenses',
    }),
  },
  methods: {
    changeHandler(value) {
      this.$emit('change', value)
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';
</style>
