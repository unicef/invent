<template>
  <section class="portfolio-area">
    <div class="content-area-full">
      <div class="AllSolutions">
        <h1>
          <translate>Solutions</translate>
        </h1>
        <el-row :gutter="20" type="flex">
          <el-col :span="16"
            ><p>
              <translate>
                This page lists all solutions, including those that are not currently in a portfolio. For more details,
                or to modify or delete a solution, go to the solution's page.
              </translate>
            </p></el-col
          >
          <el-col :span="4"></el-col>
        </el-row>
        <MainAllSolutionsTable />
      </div>
    </div>
  </section>
</template>

<script>
import MainAllSolutionsTable from '~/components/solution/dashboard/MainAllSolutionsTable.vue'

export default {
  components: {
    MainAllSolutionsTable,
  },
  async fetch({ store }) {
    await store.dispatch('solutions/loadAllActiveSolutionsList')
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.AllSolutions {
  p {
    padding-bottom: 80px;
  }
}

h1 {
  color: @colorBrandPrimary;
  font-size: 36px;
  letter-spacing: -1px;
  line-height: 45px;
  font-weight: 100;
}
</style>
