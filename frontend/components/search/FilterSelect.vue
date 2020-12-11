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
      :class="optionClass"
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
    optionClass: {
      type: String,
      default: '',
    },
  },
}
</script>

<style lang="less" scoped>
.select {
  width: 100%;
}
</style>
