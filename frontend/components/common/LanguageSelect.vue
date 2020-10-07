<template>
  <el-select
    :value="value"
    :size="size"
    :placeholder="$gettext('Select language') | translate"
    class="LanguageSelectorDropdown"
    popper-class="LanguageSelectorPopper"
    @change="changeHandler"
  >
    <el-option
      v-for="language in languages"
      :key="language.code"
      :label="language.name"
      :value="language.code"
    />
  </el-select>
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
      type: String,
      default: null,
    },
    size: {
      type: String,
      default: undefined,
    },
  },
  computed: {
    ...mapGetters({
      languages: 'system/getLanguages',
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
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.LanguageSelectorDropdown {
  width: auto;
  margin: 4px 0 8px;
}

.LanguageSelectorPopper {
}
</style>
