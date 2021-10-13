<template>
  <div class="user-projects-list">
    <p v-if="tab === 1" key="own" class="headline">
      <translate>Here are all the initiatives you are a</translate>
      <fa icon="star" class="OwnerIcon" />
      <translate tag="strong">Member</translate>
      <translate>or</translate>
      <fa icon="eye" class="ViewerIcon" />
      <translate tag="strong">Viewer</translate>
      <translate>of.</translate>
    </p>
    <p v-if="tab === 4" key="country" class="headline">
      <translate>Here are all the initiatives you are</translate>
      <translate tag="strong">Country Manager</translate>
      <translate>of.</translate>
    </p>
    <p v-if="tab === 2" key="review" class="headline">
      <translate>
        Any initiatives you have been requested to review as part of the innovation portfolio review process will appear below.
      </translate>
      <br />
      <translate>Please complete review for any initiatives marked</translate>
      <fa icon="comment-slash" class="UnscoredIcon" />
      <translate tag="strong" class="UnscoredIcon">Unscored</translate>
      <translate>below.</translate>
    </p>
    <p v-if="tab === 3" key="favorite" class="headline">
      <translate>Initiatives you have added to your favorites will appear below.</translate>
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
  data() {
    return {
      pageSizeOption: [10, 20, 50, 100],
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
      return this.limit && this.projects.length > 3 ? this.projects.slice(0, this.limit) : this.projects
    },
    hasProjects() {
      return this.projects.length > 0
    },
    cardType() {
      return this.tab === 2 ? 'review' : 'regular'
    },
    paginationOrderStr() {
      const loc = this.$i18n.locale
      return loc === 'ar' ? 'sizes, next, slot, prev' : 'sizes, prev, slot, next'
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
  padding: 40px 80px 60px;
  .headline {
    font-size: 14px;
    letter-spacing: 0;
    line-height: 20px;
    text-align: center;
    margin: 0 0 40px 0;
    .OwnerIcon {
      color: @colorOwner;
    }
    .ViewerIcon {
      color: @colorViewer;
    }
    .DonorIcon {
      color: @colorDonor;
    }
    .CountryAdminIcon {
      color: @colorCountryAdmin;
    }
    .UnscoredIcon {
      color: @colorBrandAccent;
    }
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
