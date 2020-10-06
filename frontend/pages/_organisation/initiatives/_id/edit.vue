<template>
  <div class="ProjectEdit">
    <nuxt-child />
  </div>
</template>

<script>
import { fetchProjectData } from '@/utilities/projects'
export default {
  fetch({ store, params, error }) {
    store.dispatch('landing/resetSearch')
    return fetchProjectData(store, params, error)
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
