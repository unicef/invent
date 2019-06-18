<template>
  <div class="EditProject">
    <div class="PageTitle">
      <h2><translate>Edit Project Info</translate></h2>
      <p>
        <translate>You are viewing the</translate>
        <span class="DraftLabel">
          <translate>Draft</translate>
        </span>
        <translate>version of the project.</translate>
      </p>
    </div>
    <project-form />
  </div>
</template>

<script>
import ProjectForm from '../../../../../components/project/ProjectForm';

export default {
  components: {
    ProjectForm
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

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
