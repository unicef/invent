<template>
  <div class="DigitalHealthInterventionsList">
    <ul class="SelectedDigitalHealthInterventions">
      <li v-for="item in selected" :key="item">
        <list-action v-if="actions" @click="$emit('delete', item)" />
        <digital-health-intervention-item :id="item" />
      </li>
    </ul>
  </div>
</template>

<script>
import DigitalHealthInterventionItem from '../DigitalHealthInterventionItem'
import ListAction from './ListAction'

export default {
  components: {
    DigitalHealthInterventionItem,
    ListAction,
  },
  props: {
    platform: {
      type: Number,
      default: null,
    },
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
  },
  computed: {
    selected() {
      if (this.platform) {
        const result = this.value
          .filter((dhi) => dhi.platform === this.platform)
          .map((dhi) => dhi.id)
        return this.limit ? result.slice(0, this.limit) : result
      }
      return this.limit ? this.value.slice(0, this.limit) : this.value
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
