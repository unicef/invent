<template>
  <section class="portfolio-area">
    <div class="content-area">
      <div class="tabs-wrapper">
        <div class="title">
          <nuxt-link
            :to="localePath({ name: 'organisation-portfolio-management' })"
          >
            <fa icon="angle-left" size="sm" />
            <translate>Back</translate>
          </nuxt-link>
          <h2>
            <translate :parameters="{ name }">
              Edit `{name}` portfolio
            </translate>
          </h2>
        </div>
        <div class="tabs">
          <p
            v-for="item in tabs"
            :key="item.id"
            :class="`${item.id === tab && 'active'}`"
            @click="setTab(item.id)"
          >
            <fa :icon="item.icon" />
            {{ $gettext(item.name) | translate }}
            {{ ` (${item.total})` }}
          </p>
        </div>
      </div>
      <div class="DashboardListView">
        <el-row>
          <table-top-actions />
        </el-row>
        <el-row>
          <main-table />
        </el-row>
      </div>
    </div>
    <aside class="filter-area">
      <advanced-search />
    </aside>
    <!-- dialogs -->
    <error />
  </section>
</template>

<script>
import AdvancedSearch from "@/components/dashboard/AdvancedSearch";
import MainTable from "@/components/portfolio/dashboard/MainTable";
import TableTopActions from "@/components/portfolio/dashboard/TableTopActions";
import { mapState, mapGetters, mapActions } from "vuex";
import debounce from "lodash/debounce";
// dialogs
import Error from "@/components/portfolio/dashboard/dialog/Error";

export default {
  components: {
    AdvancedSearch,
    MainTable,
    TableTopActions,
    Error,
  },
  async fetch({ store, query, error, params }) {
    store.dispatch("landing/resetSearch");
    store.dispatch("dashboard/setDashboardSection", "list");
    await Promise.all([
      store.dispatch("projects/loadUserProjects"),
      store.dispatch("projects/loadProjectStructure"),
      store.dispatch("portfolio/getProjects", params.id),
    ]);
    await store.dispatch("dashboard/setSearchOptions", query);
    try {
      await store.dispatch("dashboard/loadProjectList");
    } catch (e) {
      console.log(e);
      error({
        statusCode: 404,
        message: "Unable to process the search with the current parameters",
      });
    }
    // todo: integration should handle the status to refill data of projects
  },
  computed: {
    ...mapState({
      tabs: (state) => state.portfolio.tabs,
      tab: (state) => state.portfolio.tab,
      name: (state) => state.portfolio.name,
      errorDisplay: (state) => state.portfolio.errorDisplay,
      errorMessage: (state) => state.portfolio.errorMessage,
    }),
    ...mapGetters({
      searchParameters: "dashboard/getSearchParameters",
      dashboardSection: "dashboard/getDashboardSection",
    }),
  },
  watch: {
    searchParameters: {
      immediate: false,
      handler(query) {
        this.searchParameterChanged(query);
      },
    },
  },
  mounted() {
    if (window) {
      const savedFilters = window.localStorage.getItem("savedFilters");
      if (savedFilters) {
        this.setSavedFilters(JSON.parse(savedFilters));
      }
    }
  },
  methods: {
    ...mapActions({
      loadProjectList: "dashboard/loadProjectList",
      setSavedFilters: "dashboard/setSavedFilters",
      setTab: "portfolio/setTab",
    }),
    searchParameterChanged: debounce(function (query) {
      if (this.dashboardSection === "list") {
        this.$router.replace({ ...this.$route, query });
        this.load();
      }
    }, 100),
    async load() {
      this.$nuxt.$loading.start();
      await this.loadProjectList();
      this.$nuxt.$loading.finish();
    },
  },
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.portfolio-area {
  height: calc(
    100vh - @topBarHeightSubpage - @actionBarHeight - @appFooterHeight
  );

  .content-area {
    overflow-y: scroll;
    > div {
      background-color: #fbfaf8;
    }
    .alert-portfolio {
      position: absolute;
      background-color: #fce9e8;
    }
    .tabs-wrapper {
      height: 158px;
      background-color: @colorWhite;
      & > div {
        background-color: @colorWhite;
      }
      padding: 0 43px;
      .title {
        display: flex;
        align-items: center;
        margin-top: 50px;
        margin-bottom: 25px;
        h2 {
          transform: translateX(-25px);
          margin: 0;
          color: @colorBrandPrimary;
          font-size: 36px;
          letter-spacing: -1px;
          line-height: 45px;
          font-weight: 100;
          flex-grow: 2;
          text-align: center;
        }
        a {
          text-decoration: none;
          z-index: 1;
        }
      }
      .tabs {
        display: flex;
        align-items: center;
        justify-content: center;
        p {
          cursor: pointer;
          color: @colorBrandGrayDark;
          font-size: 14px;
          text-transform: uppercase;
          letter-spacing: 0;
          line-height: 18px;
          padding-bottom: 17px;
          margin: 0 15px;
          border-bottom: 3px solid transparent;
          svg {
            margin-right: 8px;
          }
          &.active {
            color: @colorTextPrimary;
            border-bottom: 3px solid @colorBrandPrimary;
          }
        }
      }
    }
  }
}
</style>
