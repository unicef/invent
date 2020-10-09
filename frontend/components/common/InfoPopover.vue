<template>
  <el-popover
    trigger="hover"
    popper-class="score-popover"
    v-bind="{ ...$props, ...$attrs }"
  >
    <slot></slot>
    <fa
      slot="reference"
      class="question-icon"
      :icon="['fas', 'question-circle']"
    />
  </el-popover>
</template>

<script>
export default {}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.score-popover.el-popover {
  padding: 0 !important;
  margin-left: 14px !important;
  &.left {
    margin-left: 0px !important;
    margin-right: 14px !important;
  }
  .el-popover__title {
    font-size: 18px;
    letter-spacing: -0.5px;
    line-height: 23px;
    padding: 20px;
    border-bottom: 1px solid #eae6e2;
  }
  p {
    font-size: 14px;
    letter-spacing: 0;
    line-height: 21px;
    padding: 17px 20px 23px;
  }
  .popper__arrow {
    display: inline;
  }
}
.question-icon {
  cursor: pointer;
  color: #a8a8a9;
  font-size: 18px;
  &:hover {
    color: @colorTextPrimary;
  }
}
</style>
