<template>
  <lazy-el-select
    :value="platforms"
    multiple
    filterable
    :placeholder="$gettext('Select from list') | translate"
    popper-class="PlatformSelectorDropdown"
    class="PlatformSelector"
    value-key="id"
    @change="changeHandler"
    @blur="$emit('blur')"
  >
    <el-option
      v-for="platform in sourceList"
      :key="platform.id"
      :label="platform.name"
      :value="platform.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: 'MultiSelector',
  model: {
    prop: 'platforms',
    event: 'change'
  },
  $_veeValidate: {
    value () {
      return this.platform;
    }
  },
  props: {
    platforms: {
      type: Array,
      default: () => []
    },
    source: {
      type: String,
      required: true
    }
  },
  computed: {
    sourceList () {
      return this.$store.getters['projects/' + this.source];
    }
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    }
  }
};
</script>

<style lang="less">
  //@import "../../assets/style/variables.less";
  //@import "../../assets/style/mixins.less";

  .PlatformSelector {
    width: 100%;
  }
</style>
