<template>
  <div class="project-review">
    <review-state-info
      :complete="item.complete"
      :portfolio="item.portfolio ? item.portfolio.name : ''"
    >
      <template slot="actions">
        <p v-if="item.complete" class="completed" @click="handleReview(item)">
          <fa icon="comment-alt" /><translate>View Review</translate>
        </p>
        <p v-else class="not-completed" @click="handleReview(item)">
          <fa icon="comment-alt" /><translate>Complete Review</translate>
        </p>
      </template>
    </review-state-info>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import ReviewStateInfo from '@/components/review/ReviewStateInfo'

export default {
  components: {
    ReviewStateInfo,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'projects/setReviewDialog',
      setCurrentProjectReview: 'projects/setCurrentProjectReview',
    }),
    handleReview(review) {
      this.setReviewDialog(true)
      this.setCurrentProjectReview(review)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.project-review {
  padding: 0 30px;
  height: 54px;
  border-bottom: 1px solid #eae6e2;
}
</style>
