<template>
  <div class="EditProject">
    <div class="PageTitle">
      <h2><translate>Edit Solution Info</translate></h2>
    </div>
    <solution-form />
  </div>
</template>

<script>
import SolutionForm from '@/components/solution/SolutionForm.vue'

export default {
  components: {
    SolutionForm,
  },
  scrollToTop: true,
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
