<template>
  <div class="HealthSystemChallengesList">
    <ul>
      <li
        v-for="hsc in selected"
        :key="hsc.id"
      >
        <list-action
          v-if="actions"
          @click="$emit('delete', hsc.id)"
        />
        <span>{{ hsc.challenge }} </span>
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
      healthSystemChallenges: 'projects/getHscChallenges'
    }),
    selected () {
      const hscs = this.healthSystemChallenges.reduce((a, c) => [...a, ...c.challenges], []);
      const result = hscs.filter(hfa => this.value.includes(hfa.id));
      return this.limit ? result.slice(0, this.limit) : result;
    }
  }
};
</script>

<style lang="less">
.HealthSystemChallengesList {
  width: 100%;
}
</style>
