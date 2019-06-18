<template>
  <div class="DHICategoriesList">
    <ul class="SelectedDHICategories">
      <li
        v-for="item in selected"
        :key="item.id"
      >
        <list-action
          v-if="actions"
          @click="$emit('delete', item.id)"
        />
        <span>{{ item.name }}</span>
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
      digitalHealthInterventions: 'projects/getDigitalHealthInterventions'
    }),
    selected () {
      const subGroups = this.digitalHealthInterventions.reduce((a, c) => [...a, ...c.subGroups], []);
      const result = subGroups.filter(sb => this.value.includes(sb.id));
      return this.limit ? result.slice(0, this.limit) : result;
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

</style>
