<template>
  <div class="project-review">
    <review-state-info :complete="complete" portfolio="Portfolio Name B">
      <template slot="actions">
        <p
          v-if="complete"
          class="completed"
          @click="handleReview({ id: 1, reviewed: true })"
        >
          <fa icon="comment-alt" /><translate>View Review</translate>
        </p>
        <p
          v-else
          class="not-completed"
          @click="handleReview({ id: 1, reviewed: false })"
        >
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
  computed: {
    complete() {
      return Math.random() >= 0.5
    },
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'projects/setReviewDialog',
      setCurrentProjectReviewer: 'projects/setCurrentProjectReviewer',
    }),
    handleReview(review) {
      this.setReviewDialog(true)
      this.setCurrentProjectReviewer(review)
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
