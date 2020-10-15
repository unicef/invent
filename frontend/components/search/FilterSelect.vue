<template>
  <el-select
    clearable
    v-bind="{ ...$props, ...$attrs }"
    class="select"
    v-on="{ ...$listeners }"
  >
    <el-option
      v-for="item in items"
      :key="item.id"
      :label="item.name"
      :value="item.id"
    >
    </el-option>
  </el-select>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
// @import '~assets/style/variables.less';
// @import '~assets/style/mixins.less';
.select {
  width: 100%;
}
</style>
