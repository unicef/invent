<template>
  <div class="ProjectPublishedView">
    <div class="PageTitle">
      <h2><translate>View Initiative Info</translate></h2>
      <p>
        <translate>You are viewing the</translate>
        <span class="PublishedLabel">
          <translate>Published</translate>
        </span>
        <translate>version of the initiative.</translate>
      </p>
    </div>
    <project-data />
  </div>
</template>

<script>
import { fetchProjectData } from "@/utilities/projects";
import ProjectData from "@/components/project/ProjectData";
export default {
  components: {
    ProjectData,
  },
  async fetch({ store, params, error }) {
    store.dispatch("landing/resetSearch");
    await fetchProjectData(store, params, error);
    if (
      !store.state.project.published ||
      store.state.project.published.name === null
    ) {
      error({
        statusCode: 404,
        message: "Initiative is not published",
      });
    }
  },
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.ProjectPublishedView {
  .CollapsibleCard {
    .el-card__header {
      background-color: lighten(@colorPublished, 10%) !important;
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
}
</style>
