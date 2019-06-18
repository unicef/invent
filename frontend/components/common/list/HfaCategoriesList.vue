<template>
  <div class="HealthFocusAreasList">
    <ul>
      <li
        v-for="hfa in selected"
        :key="hfa.id"
      >
        <list-action
          v-if="actions"
          @click="$emit('delete', hfa.id)"
        />
        <span> {{ hfa.name }} </span>
      </li>
    </ul>
  </div>
</template>

<script>
import ListAction from './ListAction';
import { mapGetters } from 'vuex';
export default {
  components: {
    ListAction
  },
  props: {
    value: {
      type: Array,
      default: () => []
    },
    actions: {
      type: Boolean,
      default: false
    },
    limit: {
      type: Number,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      healthFocusAreas: 'projects/getHealthFocusAreas'
    }),
    selected () {
      const result = this.healthFocusAreas.filter(h => this.value.includes(h.id));
      return this.limit ? result.slice(0, this.limit) : result;
    }
  }
};
</script>

<style lang="less">
.HealthFocusAreasList {
  width: 100%;
}
.HealthFocusAreasSelectorDropdown {

}
</style>
