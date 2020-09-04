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
          <h2><translate>Edit portfolio</translate></h2>
        </div>
        <div class="tabs">
          <p
            v-for="item in tabs"
            :key="item.id"
            @click="handleTab(item.id)"
            :class="`${item.id === tab && 'active'}`"
          >
            <fa :icon="item.icon" />
            {{ `${item.name} (${item.total})` }}
          </p>
        </div>
      </div>
      <div>
        <p>will display filter for {{ tab }}</p>
      </div>
    </div>

    <aside class="filter-area">
      <advanced-search />
    </aside>
  </section>
</template>

<script>
import AdvancedSearch from "@/components/dashboard/AdvancedSearch";
// import { mapActions } from "vuex";

export default {
  components: {
    AdvancedSearch
  },
  fetch({ store }) {
    // store.dispatch("landing/resetSearch");
  },
  data() {
    return {
      tabs: [
        { id: 1, name: "Inventory", icon: "folder", total: 46 },
        { id: 2, name: "For review", icon: "eye", total: 18 },
        { id: 3, name: "Portfolio", icon: "briefcase", total: 35 }
      ],
      tab: 1
    };
  },
  mounted() {
    // if (window) {
    //   const savedFilters = window.localStorage.getItem("savedFilters");
    //   if (savedFilters) {
    //     this.setSavedFilters(JSON.parse(savedFilters));
    //   }
    // }
  },
  methods: {
    ...mapActions({
      // setSavedFilters: "dashboard/setSavedFilters"
    }),
    handleTab(id) {
      this.tab = id;
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.portfolio-area {
  position: relative;
  display: flex;
  overflow: hidden;
  width: 100vw;
  min-width: @appWidthMinLimit;
  max-width: @appWidthMaxLimit;
  height: calc(
    100vh - @topBarHeightSubpage - @actionBarHeight - @appFooterHeight
  );

  .content-area {
    z-index: 1;
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100vw - @advancedSearchWidth);
    min-width: @appWidthMinLimit - @advancedSearchWidth;
    max-width: @appWidthMaxLimit - @advancedSearchWidth;
    height: 100%;

    div {
      background-color: #fbfaf8;
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

  .filter-area {
    z-index: 2;
    position: relative;
    width: @advancedSearchWidth;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
  }
}
</style>
