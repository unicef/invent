<template>
  <el-popover
    trigger="hover"
    popper-class="score-popover"
    v-bind="{ ...$props, ...$attrs }"
  >
    <div class="text-info" :class="{ 'no-title': !this.$attrs.title }">
      <slot></slot>
    </div>
    <fa slot="reference" class="question-icon" :icon="icon" />
  </el-popover>
</template>

<script>
export default {
  props: {
    icon: {
      type: Array,
      default: () => ['fas', 'question-circle'],
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.score-popover.el-popover {
  padding: 0 !important;
  margin-left: 14px !important;
  border: none;
  &.left {
    margin-left: 0px !important;
    margin-right: 14px !important;
  }
  .el-popover__title {
    font-size: 18px;
    letter-spacing: -0.5px;
    line-height: 23px;
    padding: 20px;
    margin-bottom: 0;
    border-bottom: 1px solid #eae6e2;
  }
  .text-info {
    padding: 0;
    &.no-title {
      padding: 17px 20px;
    }
    span,
    p {
      font-size: 14px;
      letter-spacing: 0;
      line-height: 21px;
      text-align: left;
      white-space: pre-line;
      margin: 16px 20px;
    }
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
