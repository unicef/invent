Go<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select from list') | translate"
    filterable
    multiple
    popper-class="CapabilitySelectorDropdown"
    class="CapabilitySelector"
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
export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: Array,
      default: null
    },
    goalArea: {
      type: Number,
      default: null
    },
    valuesFunction: {
      type: Function,
      required: true
    }
  },
  $_veeValidate: {
    value () {
      return this.value;
    },
    events: 'change'
  },
  data () {
    return {
      open: false
    };
  },
  computed: {
    items () {
      return this.valuesFunction(this.goalArea);
    }
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
.CapabilitySelector {
  width: 100%;
}
.CapabilitySelectorDropdown {

}
</style>
