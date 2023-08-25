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
          <el-col :span="4" class="SolutionsButton"
            ><nuxt-link
              v-if="canCreateNew"
              :to="
                localePath({
                  name: 'organisation-solutions-create',
                })
              "
            >
              <translate>Create new Solution</translate>
            </nuxt-link></el-col
          >
        </el-row>
        <MainAllSolutionsTable />
      </div>
    </div>
  </section>
</template>

<script>
import MainAllSolutionsTable from '~/components/solution/dashboard/MainAllSolutionsTable.vue'
import { mapGetters } from 'vuex'
export default {
  components: {
    MainAllSolutionsTable,
  },
  async fetch({ store }) {
    await store.dispatch('solutions/loadAllActiveSolutionsList')
  },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
    }),
    canCreateNew() {
      if (this.user) {
        return this.user.is_superuser || this.user.global_portfolio_owner || this.user.manager.length > 0
      }
      return false
    },
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
.SolutionsButton {
  width: 40%;
  display: flex;
  align-items: flex-end;
  color: @colorBrandPrimary;
  padding-bottom: 80px;
  a {
    margin-left: auto;
    margin-right: 12px;
    background-color: @colorBrandPrimary;
    color: @colorWhite;
    height: 22px;
    padding: 11px 24px 13px 24px;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 20px;
    text-align: center;
    text-decoration: none;
  }
}
</style>
