<template>
  <div>
    <div v-for="(item, i) in items" :key="i" class="reviewers">
      <div :class="`${item.complete && 'complete'}`">
        <p>
          <b>{{ item.reviewer.name }}</b>
        </p>
        <p class="uppercase" :class="reviewStatuses[item.status]">
          {{ $gettext(reviewStatuses[item.status]) }}
        </p>
      </div>
    </div>
    <p
      v-if="portfolioPage === 'review'"
      class="assing"
      @click="handleReview(id)"
    >
      <fa icon="plus" />
      <translate>Assign Reviewers</translate>
    </p>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
  },
  computed: {
    ...mapState({
      portfolioPage: (state) => state.search.filter.portfolio_page,
    }),
    ...mapGetters({
      reviewStatuses: 'system/getReviewStatuses',
    }),
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'portfolio/setReviewDialog',
      setCurrentProjectId: 'portfolio/setCurrentProjectId',
    }),
    handleReview(id) {
      this.setReviewDialog(true)
      this.setCurrentProjectId(id)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

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
.Pending {
  color: @colorBrandGrayDark;
}
.Draft {
  // color: #fbde88;
  color: #ebb20a;
}
.Complete {
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
