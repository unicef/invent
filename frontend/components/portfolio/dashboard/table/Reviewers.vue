<template>
  <div>
    <div v-for="item in items" class="reviewers">
      <div :class="`${item.complete && 'complete'}`">
        <p>
          <b>{{ item.reviewer.name }}</b>
        </p>
        <p v-if="item.complete" class="uppercase">
          <translate>Complete</translate>
        </p>
        <p v-else class="uppercase pending">
          <translate>Pending</translate>
        </p>
      </div>
    </div>
    <p @click="handleReview(id)" class="assing">
      <fa icon="plus" />
      <translate>Assign Reviewers</translate>
    </p>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    id: {
      type: Number,
      required: true
    },
    items: {
      type: Array,
      required: true
    }
  },
  methods: {
    ...mapActions({
      setReviewDialog: "portfolio/setReviewDialog",
      setCurrentProjectId: "portfolio/setCurrentProjectId"
    }),
    handleReview(id) {
      this.setReviewDialog(true);
      this.setCurrentProjectId(id);
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.reviewers {
  display: flex;
  flex-direction: column;
  & > div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }
}
.complete {
  color: #0eb455;
}
.pending {
  color: @colorBrandGrayDark;
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
