<template>
  <el-upload
    :auto-upload="false"
    :disabled="disabled"
    :on-remove="handleChange"
    :on-change="handleChange"
    :list-type="listType"
    :file-list="files"
    class="FileUpload"
    action="doing it manually, so this prop isnt used, still needed"
  >
    <el-row
      v-if="files.length < limit"
      type="flex"
      align="middle"
    >
      <el-button
        v-if="!disabled"
        type="text"
        class="IconLeft"
      >
        <fa icon="plus" /> <translate>Upload file</translate>
      </el-button>
      <div
        v-if="files.length === 0"
        class="NoFile"
      >
        <translate>No file chosen</translate>
      </div>
    </el-row>
  </el-upload>
</template>

<script>
export default {
  props: {
    files: {
      required: true,
      type: Array
    },
    limit: {
      type: Number,
      default: 1
    },
    disabled: {
      type: Boolean,
      default: false
    },
    listType: {
      type: String,
      default: 'picture'
    }
  },

  methods: {
    handleChange (file, fileList) {
      this.$emit('update:files', fileList);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .FileUpload {
    .el-upload {
      float: left;
      margin-bottom: 10px;
    }

    .NoFile {
      padding-left: 30px;
      font-size: @fontSizeBase;
      color: @colorTextMuted;
    }
  }
</style>
