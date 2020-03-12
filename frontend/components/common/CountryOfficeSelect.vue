<template>
  <lazy-el-select
    v-model="innerValue"
    :placeholder="$gettext('Select country office') | translate"
    filterable
    class="select-office"
  >
    <el-option
      v-for="office in offices"
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
    }
  },
  mounted () {
    this.loadOffices();
  },
  methods: {
    ...mapActions({
      loadOffices: 'offices/loadOffices',
      loadOffice: 'offices/loadOffice',
      setOffice: 'offices/setOffice'
    })
  }
};
</script>

<style lang="less" scoped>
  .select-office {
    width: 50%;
  }
</style>
