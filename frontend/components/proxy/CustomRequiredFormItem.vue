<template>
  <el-form-item
    :class="`CustomRequiredFormItem ${row ? 'row-input' : ''}`"
    v-bind="propsAndAttrs"
    v-on="listeners"
  >
    <template slot="label">
      <slot name="label" />
      <template v-if="!row">
        <span
          v-show="draftRequired"
          class="Required DraftRequired"
        >
          <span>
            *
          </span>
        </span>
        <span
          v-show="publishRequired"
          class="Required PublishRequired"
        >
          <span>
            *
          </span>
        </span>
      </template>
    </template>
    <slot />
  </el-form-item>
</template>

<script>
export default {
  name: 'CustomRequiredFormItem',
  props: {
    draftRule: {
      type: Object,
      default: null
    },
    publishRule: {
      type: Object,
      default: null
    },
    row: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    propsAndAttrs () {
      return { ...this.$props, ...this.$attrs };
    },
    listeners () {
      return { ...this.$listeners };
    },
    draftRequired () {
      return this.draftRule && this.draftRule.required;
    },
    publishRequired () {
      return this.publishRule && this.publishRule.required;
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";
.CustomRequiredFormItem {
  &.row-input {
    display: flex;
    width: 100%;
    label {
      width: 315px;
    }
    .el-form-item__content {
      width: 100%;
    }
  }
  .Required {
    display: inline-block;
    width: 12px;
    height: 12px;
    font-size: 16px;
    line-height: 12px;
    font-weight: 900;
    text-align: center;
    border-radius: 50%;

    > span {
      position: relative;
      top: 4px;
    }
  }
  .DraftRequired {
    color: @colorTextPrimary;
    background-color: @colorDraft;
  }
  .PublishRequired {
    color: @colorWhite;
    background-color: @colorPublished;
  }
}
</style>
