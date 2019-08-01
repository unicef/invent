<template>
  <lazy-el-select
    :value="value"
    :placeholder="realPlaceholder"
    filterable
    :clearable="clearable"
    popper-class="GoalAreasSelectorDropdown"
    class="GoalAreasSelector"
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
    },
    placeholder: {
      type: String,
      default: null
    },
    clearable: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      open: false
    };
  },
  computed: {
    ...mapGetters({
      items: 'projects/getGoalAreas'
    }),
    realPlaceholder () {
      return this.placeholder || this.$gettext('Select from list');
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
.GoalAreasSelector {
  width: 100%;
}
.GoalAreasSelectorDropdown {

}
</style>
