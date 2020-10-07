<template>
  <div class="HealthFocusAreasList">
    <ul>
      <li v-for="item in selected" :key="item.id">
        <list-action v-if="actions" @click="$emit('delete', item.id)" />
        <span> {{ item.name }} </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ListAction from './ListAction'
export default {
  components: {
    ListAction,
  },
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    actions: {
      type: Boolean,
      default: false,
    },
    limit: {
      type: Number,
      default: null,
    },
    goalArea: {
      type: Number,
      required: true,
    },
    type: {
      type: String,
      required: true,
      validator: (value) =>
        [
          'capabilityLevels',
          'capabilityCategories',
          'capabilitySubcategories',
        ].includes(value),
    },
  },
  computed: {
    ...mapGetters({
      capabilityLevels: 'projects/getCapabilityLevels',
      capabilityCategories: 'projects/getCapabilityCategories',
      capabilitySubcategories: 'projects/getCapabilitySubcategories',
    }),
    items() {
      return this[this.type](this.goalArea)
    },
    selected() {
      const result = this.items.filter((h) => this.value.includes(h.id))
      return this.limit ? result.slice(0, this.limit) : result
    },
  },
}
</script>

<style lang="less">
.HealthFocusAreasList {
  width: 100%;
}
.HealthFocusAreasSelectorDropdown {
}
</style>
