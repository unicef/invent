<template>
  <div class="DonorList">
    <ul>
      <li v-for="p in selected" :key="p.id" class="DonorItem">
        <span v-show="showIcon">
          <fa :icon="['far', 'user']" size="xs" />
        </span>
        <span>{{ p.name }}</span>
      </li>
      <li v-show="excluded">
        <span>
          <fa icon="arrow-alt-circle-right" size="xs" />
        </span>
        <span>
          <translate :parameters="{ excluded }">
            ... {excluded} more
          </translate>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  components: {},
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    limit: {
      type: Number,
      default: null,
    },
    showIcon: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      donors: 'system/getDonors',
    }),
    selected() {
      const result = this.donors.filter((p) => this.value.includes(p.id))
      return this.limit ? result.slice(0, this.limit) : result
    },
    limited() {
      return this.limit ? this.selected.slice(0, this.limit) : this.selected
    },
    excluded() {
      return this.selected.length - this.limited.length
    },
  },
}
</script>

<style lang="less">
.DonorList {
  width: 100%;
}
</style>
