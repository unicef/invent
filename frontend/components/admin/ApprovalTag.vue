<template>
  <div class="ApprovalTag">
    <el-tag
      :type="value ? 'success' : value === null ? 'warning' : 'danger'"
      size="small"
      disable-transitions
      :key="value"
    >
      <span v-show="value === true">
        <translate>Yes</translate>
      </span>
      <span v-show="value === false">
        <translate>No</translate>
      </span>
      <span v-show="value === null">
        <translate>Pending</translate>
      </span>
    </el-tag>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: null
    }
  }
};
</script>

<style lang="less">
.ApprovalTag {
  .el-tag--small {
    height: 26px;
    font-weight: 700;
    line-height: 24px;
  }
}
</style>
