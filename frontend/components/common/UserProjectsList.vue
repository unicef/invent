<template>
  <div :class="`user-projects-list ${landing && 'landing'}`">
    <p v-if="!landing" class="headline">
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
    <div v-show="total > 10 && !loadingProject" class="ProjectsPagination">
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="pageSizeOption"
        :total="total"
        :layout="paginationOrderStr"
      >
        <current-page :total="total" :page-size="pageSize" :page="page" />
      </el-pagination>
    </div>
    <review-dialog />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import { mapGettersActions } from '@/utilities/form.js'
import ReviewDialog from '@/components/review/ReviewDialog'
import ExtendedProjectCard from '@/components/common/ExtendedProjectCard'
import EmptyProjects from '@/components/common/EmptyProjects'
import CurrentPage from '@/components/dashboard/CurrentPage'

export default {
  components: {
    EmptyProjects,
    ExtendedProjectCard,
    ReviewDialog,
    CurrentPage,
  },
  props: {
    limit: {
      type: Number,
      default: null,
    },
    landing: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      pageSizeOption: [10, 20, 50, 100],
      headline: [
        this.$gettext(
          'Here are all the initiatives you are a Member or a Viewer of'
        ),
        this.$gettext(
          'Any initiatives you have been requested to review as part of the innovation portfolio review process will appear below. Please complete review for any initiatives marked “Unscored” below.'
        ),
        this.$gettext(
          'Initiatives you have added to your favorites will appear below.'
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
    ...mapGetters({
      page: 'projects/getCurrentPage',
      total: 'projects/getTotal',
    }),
    ...mapGettersActions({
      pageSize: ['projects', 'getPageSize', 'setPageSize', 0],
      currentPage: ['projects', 'getCurrentPage', 'setCurrentPage', 0],
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
    paginationOrderStr() {
      const loc = this.$i18n.locale
      return loc === 'ar'
        ? 'sizes, next, slot, prev'
        : 'sizes, prev, slot, next'
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
  &.landing {
    padding: 40px 24px 10px;
  }
  .headline {
    font-size: 14px;
    letter-spacing: 0;
    line-height: 20px;
    text-align: center;
    margin-bottom: 52px;
  }
}

.ProjectsPagination {
  margin-top: 50px;
  width: 100%;
  background-color: @colorWhite;
  text-align: right;

  .el-pagination {
    padding: 13px 30px;
    font-weight: 400;

    .el-pagination__sizes {
      float: left;
      margin: 0;
    }

    .PageCounter {
      display: inline-block;
      margin: 0 10px;
      font-size: @fontSizeSmall;
      color: @colorTextSecondary;
      letter-spacing: 0;
      line-height: 15px;
    }

    button {
      padding: 0;
      background-color: transparent;
      transition: @transitionAll;
      i {
        font-size: @fontSizeLarge !important;
        font-weight: 700 !important;
      }
    }
  }
}
</style>
