<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select investor') | translate"
    popper-class="DonorSelectorPopper"
    class="DonorSelector"
    @change="changeHandler"
  >
    <el-option
      v-for="donor in donors"
      :key="donor.id"
      :label="donor.name"
      :value="donor.id"
    />
  </lazy-el-select>
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
      type: Number,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      donors: 'system/getDonors'
    })
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .DonorSelectorPopper {
    max-width: @advancedSearchWidth - 40px;
  }
</style>
