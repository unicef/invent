<template>
  <el-select
    v-model="innerValue"
    :disabled="disabled"
    :placeholder="$gettext('Select region') | translate"
    clearable
  >
    <el-option
      v-for="region in regions"
      :key="region.id"
      :label="region.name"
      :value="region.id"
    />
  </el-select>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: [Number, String],
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      regions: 'system/getRegions'
    }),
    innerValue: {
      get () {
        return this.value;
      },
      set (value) {
        this.$emit('change', value);
      }
    }
  }
};
</script>

<style>

</style>
