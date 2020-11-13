<template>
  <div>
    <tabs :tabs="tabs" :tab="tab" @handleTab="setTab">
      <template slot="title">
        <h2>
          <translate>My Initiatives</translate>
        </h2>
      </template>
    </tabs>
    <user-project-list />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

import UserProjectList from '@/components/common/UserProjectsList'
import Tabs from '@/components/common/Tabs'
import toInteger from 'lodash/toInteger'

export default {
  components: {
    UserProjectList,
    Tabs,
  },
  computed: {
    ...mapState({
      tabs: (state) => state.projects.tabs,
      tab: (state) => state.projects.tab,
      projects: (state) => state.projects.userProjects,
    }),
  },
  async mounted() {
    if (this.$route.query.review) {
      // filter popup for open an id
      await this.setTab(2)
      const review = this.projects.find(
        (i) => i.reviewId === toInteger(this.$route.query.review)
      )
      if (review) {
        await this.setCurrentProjectReview(review)
        this.setReviewDialog(true)
      }
    } else {
      await this.setTab(1)
    }
  },
  methods: {
    ...mapActions({
      setTab: 'projects/setTab',
      setCurrentProjectReview: 'projects/setCurrentProjectReview',
      setReviewDialog: 'projects/setReviewDialog',
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
