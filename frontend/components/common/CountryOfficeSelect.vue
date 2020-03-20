<template>
  <lazy-el-select
    v-model="innerValue"
    :disabled="disabled"
    :placeholder="$gettext('Select country office') | translate"
    filterable
    class="select-office"
  >
    <el-option
      v-for="office in officeList"
      :key="office.id"
      :label="office.name"
      :value="office.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: [Number, Array],
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    },
    regionFilter: {
      type: [Number, String],
      default: NaN
    }
  },
  computed: {
    ...mapState({
      offices: state => state.offices.offices
    }),
    innerValue: {
      get () {
        return this.value;
      },
      set (value) {
        this.$emit('change', value);
      }
    },
    officeList () {
      if (this.regionFilter !== NaN) {
        return this.offices.filter((office) => office.region === this.regionFilter);
      }
      return this.offices;
    }
  },
  mounted () {
    this.loadOffices();
  },
  methods: {
    ...mapActions({
      loadOffices: 'offices/loadOffices'
    })
  }
};
</script>

<style lang="less" scoped>
  .select-office {
    width: 100%;
  }
</style>
