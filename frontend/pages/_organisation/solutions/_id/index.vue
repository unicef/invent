<template>
  <div class="SolutionPublishedView">
    <div class="PageTitle">
      <el-row>
        <el-col :span="18">
          <h2 class="Title"><translate>View Solution Information</translate></h2>
        </el-col>
        <el-col :span="6">
          <el-button v-if="canEdit" type="primary" size="medium" @click="goToEdit">
            <translate>Edit Solution</translate>
          </el-button>
        </el-col>
      </el-row>
    </div>
    <solution-data />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SolutionData from '@/components/solution/SolutionData'

export default {
  components: {
    SolutionData,
  },
  scrollToTop: true,
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
    }),
    canEdit() {
      return (
        (this.user && this.user.is_superuser) ||
        (this.user && this.user.global_portfolio_owner) ||
        (this.user && this.user.manager.length > 0)
      )
    },
  },
  async fetch({ store, params, error }) {
    try {
      await store.dispatch('solution/loadProblemPortfoliolists')
      await store.dispatch('solution/loadSolution', params.id)
    } catch (e) {
      error({ statusCode: e.status ?? 400, message: e.message ?? 'Unknown error' })
    }
  },
  methods: {
    goToEdit() {
      const localised = this.localePath({
        name: `organisation-solutions-id-edit`,
        params: { ...this.$route.params },
        query: { portfolio: this.$route.query.portfolio },
      })
      this.$router.push(localised)
    },
  },
  // async fetch({ store, params, error }) {
  //   store.dispatch('landing/resetSearch')
  //   await fetchProjectData(store, params, error)
  //   if (!store.state.project.published || store.state.project.published.name === null) {
  //     error({
  //       statusCode: 404,
  //       message: 'Initiative is not published',
  //     })
  //   }
  // },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SolutionPublishedView {
  .CollapsibleCard {
    .el-card__header {
      background-color: lighten(@colorPublished, 10%) !important;
      color: @colorWhite !important;
    }
  }

  .Stepper {
    li {
      &.active,
      &:hover,
      &:active {
        .el-button {
          .Step {
            color: @colorWhite;
            background-color: lighten(@colorPublished, 10%) !important;
          }
        }
      }
    }
  }

  .PublishedLabel {
    display: inline-block;
    height: 23px;
    margin: 0 6px;
    padding: 0 10px;
    font-size: @fontSizeSmall;
    font-weight: 700;
    line-height: 24px;
    text-transform: uppercase;
    border-radius: 12px;
    background-color: @colorPublished;
    color: @colorWhite;
  }
  .PageTitle {
    .Title {
      padding-left: 35%;
    }
  }
}
</style>
