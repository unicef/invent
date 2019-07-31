<template>
  <div class="CustomAnswersCell">
    <ul v-if="type > 3">
      <li
        v-for="(v, index) in limited"
        :key="index"
      >
        <span>
          <fa
            icon="check"
            size="xs"
          />
        </span>
        <span>{{ v }}</span>
      </li>
      <li v-show="excluded > 0">
        <span>
          <fa
            icon="check"
            size="xs"
          />
        </span>
        <span>
          <translate :parameters="{excluded}">
            ... {excluded} more
          </translate>
        </span>
      </li>
    </ul>
    <p v-if="type < 4">
      {{ values[0] }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    row: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: Number,
      default: null
    },
    type: {
      type: Number,
      default: null
    },
    donorId: {
      type: Number,
      default: null
    },
    limit: {
      type: Number,
      default: null
    }
  },
  computed: {
    source () {
      return this.donorId ? 'donor_answers' : 'country_answers';
    },
    values () {
      if (this.id && this.row && this.row[this.source]) {
        const module = this.row[this.source];
        if (this.donorId) {
          return module[this.donorId] && module[this.donorId][this.id] ? module[this.donorId][this.id] : [];
        }
        return module[this.id] ? module[this.id] : [];
      }
      return [];
    },
    limited () {
      return this.limit && this.values.length > this.limit ? this.values.slice(0, this.limit) : this.values;
    },
    excluded () {
      if (this.values && this.limited) {
        return this.values.length - this.limited.length;
      }
      return 0;
    }
  }
};
</script>

<style lang="less">
.CustomAnswersCell {
  width: 100%;
}
</style>
