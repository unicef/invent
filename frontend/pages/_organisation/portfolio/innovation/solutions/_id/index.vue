<template>
  <div class="ProjectDraftView">
    <div class="PageTitle">
      <h2><translate>View Solution Info</translate></h2>
      <p>
        <translate>You are viewing the</translate>
        <span class="DraftLabel">
          <translate>Draft</translate>
        </span>
        <translate>version of the solution.</translate>
      </p>
    </div>
    <solution-data show-draft :canEdit="true" />
  </div>
</template>

<script>
//import { fetchProjectData } from '@/utilities/projects'
import SolutionData from '@/components/solution/SolutionData'
export default {
  components: {
    SolutionData,
  },
  scrollToTop: true,
  // async fetch({ store, params, error }) {
  //   try {
  //     await store.dispatch('solution/loadSolution', params.id)
  //   } catch (e) {
  //     error({ statusCode: e.status ?? 400, message: e.message ?? 'Unknown error' })
  //   }
  // },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
    }),
    canEdit() {
      return true
      // return (
      //   (this.user && this.user.is_superuser) ||
      //   (this.user && this.user.global_portfolio_owner) ||
      //   (this.user && this.user.manager.length > 0)
      // )
    },
  },
  // fetch({ store, params, error }) {
  //   store.dispatch('landing/resetSearch')
  //   return fetchProjectData(store, params, error)
  // },
}
</script>

<style lang="less">
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.ProjectDraftView {
  .DraftLabel {
    display: inline-block;
    height: 23px;
    margin: 0 6px;
    padding: 0 10px;
    font-size: @fontSizeSmall;
    font-weight: 700;
    line-height: 24px;
    text-transform: uppercase;
    border-radius: 12px;
    background-color: @colorDraft;
    color: @colorTextPrimary;
  }
}
</style>
