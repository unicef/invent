<template>
  <div>
    <p @click="handleScore()" class="assing mb-10">
      <fa icon="list" />
      <translate v-if="tab === 2">Change / view score</translate>
      <translate v-if="tab === 3">View score</translate>
    </p>
    <p v-if="scores.reviewed && tab === 2" class="complete uppercase">
      <translate>Completed</translate>
    </p>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    scores: {
      type: Object,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    tab: {
      type: Number,
      required: true,
    },
  },
  methods: {
    ...mapActions({
      getManagerScore: "portfolio/getManagerScore",
    }),
    handleScore() {
      this.getManagerScore({ id: this.scores.id, name: this.name });
    },
  },
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.complete {
  color: #0eb455;
}
.uppercase {
  text-transform: uppercase;
  font-size: 10px !important;
}
.assing {
  display: flex;
  align-items: center;
  color: @colorBrandPrimary;
  cursor: pointer;
  &.mb-10 {
    margin-bottom: 10px !important;
  }
}
</style>
