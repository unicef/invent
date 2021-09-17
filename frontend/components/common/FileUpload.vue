<template>
  <div>
    <el-upload
      ref="uploader"
      :auto-upload="false"
      :disabled="disabled"
      :on-remove="handleChange"
      :on-change="handleChange"
      :list-type="listType"
      :file-list="files"
      :accept="accept"
      class="FileUpload"
      action="doing it manually, so this prop isnt used, still needed"
    >
      <el-row v-if="files.length < limit" type="flex" align="middle">
        <el-button v-if="!disabled" type="text" class="IconLeft">
          <fa icon="plus" /> <translate>Upload file</translate>
        </el-button>
        <div v-if="files.length === 0" class="NoFile">
          <translate>No file chosen</translate>
        </div>
      </el-row>
      <template slot="file" slot-scope="{ file }">
        <img :src="file.url" class="el-upload-list__item-thumbnail" @click="handleImageCardPreview(file)" />
        <span class="el-upload-list__item-name"> <i class="el-icon-document"></i>{{ file.name }} </span>
        <label class="el-upload-list__item-status-label">
          <i class="el-icon-upload-success el-icon-check"></i>
        </label>
        <i class="el-icon-close" @click="handleRemove(file)"></i>
        <i class="el-icon-close-tip">press delete to remove</i>
      </template>
    </el-upload>

    <el-dialog
      :title="imagePreviewTitle"
      :visible.sync="previewDialog"
      custom-class="ImgPreviewDialog"
      modal
      @opened="getImgDimensions"
    >
      <img ref="preview" :src="previewImage" />
      <template slot="footer">
        <strong><translate>Dimensions</translate>:</strong>
        <span><translate>Width</translate>:</span>
        <span>{{ previewImageWidth }}px,</span>
        <span><translate>Height</translate>:</span>
        <span>{{ previewImageHeight }}px</span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: {
    files: {
      required: true,
      type: Array,
    },
    limit: {
      type: Number,
      default: 1,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    listType: {
      type: String,
      default: 'picture',
    },
    previewTitle: {
      type: String,
      default: 'Image',
    },
    accept: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      previewDialog: false,
      previewImage: '',
      previewImageWidth: null,
      previewImageHeight: null,
    }
  },
  computed: {
    imagePreviewTitle() {
      return this.$gettext(`${this.previewTitle} preview`)
    },
  },
  methods: {
    handleChange(file, fileList) {
      this.$emit('update:files', fileList)
    },
    handleImageCardPreview(file) {
      this.previewImage = file.url
      this.previewDialog = true
    },
    handleRemove(file) {
      this.$emit('clear')
      this.$refs.uploader.clearFiles()
    },
    getImgDimensions() {
      this.previewImageWidth = this.$refs.preview.width
      this.previewImageHeight = this.$refs.preview.height
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FileUpload {
  .el-upload {
    float: left;
    margin-bottom: 10px;
  }
  .el-upload-list__item img {
    &:hover {
      cursor: zoom-in;
    }
  }
  .NoFile {
    padding-left: 30px;
    font-size: @fontSizeBase;
    color: @colorTextMuted;
  }
}

.ImgPreviewDialog {
  &.el-dialog {
    margin: 0 !important;
    width: fit-content;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 90%;
    max-height: 90%;
    overflow: hidden;

    .el-dialog__body {
      max-height: initial;
      overflow: hidden;
      padding: 1em;
      display: flex;
      align-items: center;
      justify-content: center;
      img {
        height: auto;
        width: auto;
        max-height: 68vh;
        max-width: 84vw;
        margin-left: auto;
        margin-right: auto;
        display: block;
      }
    }

    .el-dialog__footer {
      display: flex;
      align-items: center;
      gap: 6px;
    }
  }
}
</style>
