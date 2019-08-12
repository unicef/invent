<template>
  <lazy-el-select
    :value="value"
    :disabled="!goalArea && !showAll"
    :placeholder="realPlaceholder"
    filterable
    clearable
    popper-class="ResultAreasSelectorDropdown"
    class="ResultAreasSelector"
    @change="changeHandler"
  >
    <el-option
      v-for="item in filtered"
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
    goalArea: {
      type: Number,
      default: null
    },
    placeholder: {
      type: String,
      default: null
    },
    showAll: {
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
      items: 'projects/getResultAreas'
    }),
    filtered () {
      return this.showAll ? this.items : this.items.filter(ra => ra.goal_area_id === this.goalArea);
    },
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
.ResultAreasSelector {
  width: 100%;
}
.ResultAreasSelectorDropdown {

}
</style>
