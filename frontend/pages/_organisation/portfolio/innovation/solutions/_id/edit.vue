<template>
  <div class="ProjectEdit">
    <nuxt-child />
  </div>
</template>

<script>
export default {
  async fetch({ store, params, error }) {
    // store.dispatch('landing/resetSearch')
    try {
      await store.dispatch('solution/loadSolution', params.id)
    } catch (e) {
      error({ statusCode: e.status ?? 400, message: e.message ?? 'Unknown error' })
    }
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ProjectEdit {
  .CollapsibleCard {
    .el-card__header {
      background-color: lighten(@colorDraft, 10%) !important;
      color: @colorTextPrimary !important;
    }

    .CollapsibleHeader {
      .CollapseToggle {
        color: @colorTextPrimary !important;
      }
    }
  }

  .Stepper {
    li {
      &.active,
      &:hover,
      &:active {
        .el-button {
          .Step {
            background-color: lighten(@colorDraft, 10%) !important;
            color: @colorTextPrimary !important;
          }
        }
      }
    }
  }
}
</style>
