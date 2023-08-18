<template>
  <div class="EditProject">
    <div class="PageTitle">
      <h2><translate>Create Solution</translate></h2>
    </div>
    <new-solution-form />
  </div>
</template>

<script>
import NewSolutionForm from '@/components/solution/NewSolutionForm.vue'
import { mapGetters } from 'vuex'
export default {
  components: {
    NewSolutionForm,
  },
  scrollToTop: true,
  async fetch({ store }) {
    store.dispatch('solution/loadProblemPortfoliolists')
  },
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
    }),
  },
  watch: {
    currentProject: {
      immediate: true,
      handler() {
        const allowed =
          this.profile.is_superuser ||
          this.profile.global_portfolio_owner ||
          this.profile.manager.length > 0 ||
          this.$route.name.split('__')[0] === 'organisation-solutions-id'
        // this.profile.member.includes(parseInt(this.$route.params.id, 10))
        if (!allowed) {
          this.$alert(this.$gettext('You are not authorized to access this view'), this.$gettext('Warning'), {
            confirmButtonText: 'OK',
            callback: () => {
              const path = this.localePath({
                name: 'organisation-solutions',
                params: this.$route.params,
              })
              this.$router.replace(path)
            },
          })
        }
      },
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.EditProject {
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
