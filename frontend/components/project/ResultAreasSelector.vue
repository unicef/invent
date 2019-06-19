<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select from list') | translate"
    filterable
    popper-class="ResultAreasSelectorDropdown"
    class="ResultAreasSelector"
    @change="changeHandler"
  >
    <el-option
      v-for="item in items"
      :key="item.id"
      :label="item.name"
      :value="item.id"
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
  data () {
    return {
      open: false
    };
  },
  computed: {
    ...mapGetters({
      items: 'projects/getResultAreas'
    })
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    },
    toggleHandler (value) {
      if (value) {
        this.open = value;
      }
    }
  }
};
</script>

<style lang="less">
.ResultAreasSelector {
  width: 100%;
}
.ResultAreasSelectorDropdown {

}
</style>
