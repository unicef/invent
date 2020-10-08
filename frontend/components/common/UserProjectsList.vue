<template>
  <div class="user-projects-list">
    <p class="headline">
      {{ headline[tab - 1] }}
    </p>
    <empty-projects v-if="!hasProjects" />
    <extended-project-card
      v-for="project in limited"
      :id="project.id"
      :key="project.id"
      :type="cardType"
    />
    <review-dialog />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import ReviewDialog from '@/components/review/ReviewDialog'
import ExtendedProjectCard from '../common/ExtendedProjectCard'
import EmptyProjects from './EmptyProjects'

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
      tab: (state) => state.projects.tab,
    }),
    ...mapGetters({
      userProjecList: 'projects/getUserProjectList',
    }),
    limited() {
      return this.limit && this.userProjecList.length > 3
        ? this.userProjecList.slice(0, this.limit)
        : this.userProjecList
    },
    hasProjects() {
      return this.userProjecList.length > 0
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
