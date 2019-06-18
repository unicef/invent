<template>
  <div class="HisBucketList">
    <ul>
      <li
        v-for="his in selected"
        :key="his.id"
      >
        <list-action
          v-if="actions"
          @click="$emit('delete', his.id)"
        />
        <span>{{ his.name }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ListAction from './ListAction';
export default {
  components: {
    ListAction
  },
  props: {
    value: {
      type: Array,
      default: null
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
      hisBucket: 'projects/getHisBucket'
    }),
    selected () {
      const result = this.hisBucket.filter(his => this.value.includes(his.id));
      return this.limit ? result.slice(0, this.limit) : result;
    }
  }
};
</script>

<style lang="less">
.HisBucketList {
  width: 100%;
}
</style>
