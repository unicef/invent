<template>
  <el-select
    clearable
    v-bind="{ ...$props, ...$attrs }"
    class="select"
    v-on="{ ...$listeners }"
  >
    <el-option
      v-for="item in richItems"
      :key="item.id"
      :label="item.name"
      :value="item.id"
      :class="optionClass"
      :disabled="item.disabled"
    >
    </el-option>
  </el-select>
</template>

<script>
export default {
  props: {
    value: {
      required: true,
      validator: (prop) =>
        typeof prop === 'string' ||
        Array.isArray(prop) ||
        typeof prop === 'number' ||
        prop === null,
    },
    items: {
      type: Array,
      required: true,
    },
    optionClass: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      richItems: this.items.map((i) => {
        return { ...i, disabled: false }
      }),
    }
  },
  watch: {
    value(val) {
      const target = this.items.find((i) => i.name === 'N/A')
      if (target !== undefined && val.includes(target.id)) {
        this.richItems = this.items.map((i) => {
          if (i.name === 'N/A') {
            return { ...i, disabled: false }
          }
          return { ...i, disabled: true }
        })
      } else {
        this.richItems = this.items.map((i) => {
          return { ...i, disabled: false }
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.select {
  width: 100%;
}
</style>
