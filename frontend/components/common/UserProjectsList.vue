<template>
  <div class="user-projects-list">
    <p class="headline">
      {{ headline[tab - 1] }}
    </p>
    <div v-loading="loadingProject" class="loading-mask">
      <template v-if="!loadingProject">
        <empty-projects v-if="!hasProjects" />
        <extended-project-card
          v-for="project in limited"
          :id="project.id"
          :key="project.id"
          :type="cardType"
          :project="project"
        />
      </template>
    </div>
    <review-dialog />
  </div>
</template>

<script>
import { mapState } from 'vuex'

import ReviewDialog from '@/components/review/ReviewDialog'
import ExtendedProjectCard from '@/components/common/ExtendedProjectCard'
import EmptyProjects from '@/components/common/EmptyProjects'

export default {
  components: {
    EmptyProjects,
    ExtendedProjectCard,
    ReviewDialog,
  },
  props: {
    limit: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      headline: [
        this.$gettext(
          'Please specify headline copy text for each tabs, thank you.'
        ),
        this.$gettext(
          'Please complete portfolio review process for any projects marked “unscored” below.'
        ),
        this.$gettext(
          'Please specify headline copy text for each tabs, thank you.'
        ),
      ],
    }
  },
  computed: {
    ...mapState({
      projects: (state) => state.projects.userProjects,
      tab: (state) => state.projects.tab,
      loadingProject: (state) => state.projects.loadingProject,
    }),
    limited() {
      return this.limit && this.projects.length > 3
        ? this.projects.slice(0, this.limit)
        : this.projects
    },
    hasProjects() {
      return this.projects.length > 0
    },
    cardType() {
      return this.tab === 2 ? 'review' : 'regular'
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.loading-mask {
  width: 100%;
  min-height: 500px;
}
.user-projects-list {
  padding: 50px 80px 60px;
  .headline {
    font-size: 14px;
    letter-spacing: 0;
    line-height: 20px;
    text-align: center;
    margin-bottom: 52px;
  }
}
</style>
