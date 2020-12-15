<template>
  <div class="DashboardFiltersHeader">
    <span class="ProjectToShow">
      <translate :parameters="{ total }">
        {total} initiative(s) to show
      </translate>
    </span>
    <!-- <el-button class="ToggleFiltersButton">
      <fa icon="chevron-right" />
    </el-button> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters({
      total: 'dashboard/getTotal',
    }),
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.DashboardFiltersHeader {
  background-color: @colorBrandPrimaryDark;
  transform: translateX(40px);

  .ProjectToShow {
    display: inline-block;
    box-sizing: border-box;
    padding-left: 20px;
    width: @advancedSearchWidth - @actionBarHeight;
    color: @colorWhite;
    font-size: @fontSizeBase;
    font-weight: 700;
    line-height: @actionBarHeight;

    .svg-inline--fa {
      margin-right: 4px;
    }
  }

  .ToggleFiltersButton {
    width: @actionBarHeight;
    height: @actionBarHeight;
    padding: 0;
    border: 0;
    background-color: @colorBrandPrimaryDark;

    &:hover {
      background-color: lighten(@colorBrandPrimaryDark, 10%);
    }
  }
}
</style>
