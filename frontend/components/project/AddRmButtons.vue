<template>
  <div class="AddRmButtons">
    <el-button
      v-show="showRm"
      key="delete"
      type="text"
      class="DeleteButton IconLeft IViewert"
      @click="$emit('rm')"
    >
      <fa icon="minus" />
      <translate>Delete</translate>
    </el-button>
    <el-button
      v-show="showAdd"
      key="show"
      type="text"
      class="AddButton IconLeft"
      @click="$emit('add')"
    >
      <fa icon="plus" />
      <translate>Add</translate>
    </el-button>
  </div>
</template>

<script>
export default {
  props: {
    showRm: {
      type: Boolean,
      default: false,
    },
    showAdd: {
      type: Boolean,
      default: true,
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.AddRmButtons {
  padding-left: 30px;

  .el-button {
    margin-left: 0;
  }

  .DeleteButton {
    margin-right: 20px;
  }

  .svg-inline--fa {
    width: 16px;
  }
}
</style>
