<template>
  <ul class="CapabilitiesList">
    <li
      v-for="item in selected"
      :key="item.id"
    >
      {{ item.name }}
    </li>
  </ul>
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
      required: true
    },
    valuesFunction: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      open: false
    };
  },
  computed: {
    items () {
      return this.valuesFunction(this.goalArea);
    },
    selected () {
      return this.items.filter(i => this.value.some(v => v === i.id));
    }
  }
};
</script>

<style lang="less">
.CapabilitiesList {
  width: 100%;
}
</style>
