<template>
  <div class="CapabilitiesList">
    <ul>
      <li
        v-for="item in selected"
        :key="item.id"
      >
        <span v-if="showIcon">
          <fa
            icon="check"
            size="xs"
          />
        </span>
        <span>{{ item.name }}</span>
      </li>
    </ul>
  </div>
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
    },
    showIcon: {
      type: Boolean,
      defaultL: false
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
      if (this.value && Array.isArray(this.value)) {
        return this.items.filter(i => this.value.some(v => v === i.id));
      }
      return [];
    }
  }
};
</script>

<style lang="less">
.CapabilitiesList {
  width: 100%;
}
</style>
