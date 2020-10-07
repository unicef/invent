<template>
  <el-form-item
    class="CustomRequiredFormItem"
    v-bind="propsAndAttrs"
    v-on="listeners"
  >
    <template slot="label">
      <slot name="label" />
      <span v-show="draftRequired" class="Required DraftRequired">
        <span> * </span>
      </span>
      <span v-show="publishRequired" class="Required PublishRequired">
        <span> * </span>
      </span>
      <span class="pull-right">
        <el-tooltip
          class="item"
          effect="dark"
          content="You need a unicef.org email to add users"
          placement="left"
        >
          <i class="el-icon-warning warning" />
        </el-tooltip>
      </span>
    </template>
    <slot />
  </el-form-item>
</template>

<script>
export default {
  name: 'CustomRequiredFormTeamItem',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    draftRule: {
      type: Object,
      default: null,
    },
    publishRule: {
      type: Object,
      default: null,
    },
    value: {
      type: Array,
      default: null,
    },
  },
  data() {
    return {
      inputValue: '',
    }
  },
  computed: {
    propsAndAttrs() {
      return { ...this.$props, ...this.$attrs }
    },
    listeners() {
      return { ...this.$listeners }
    },
    draftRequired() {
      return this.draftRule && this.draftRule.required
    },
    publishRequired() {
      return this.publishRule && this.publishRule.required
    },
  },
  methods: {},
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
.CustomRequiredFormItem {
  .Required {
    display: inline-block;
    width: 12px;
    height: 12px;
    font-size: 16px;
    line-height: 12px;
    font-weight: 900;
    text-align: center;
    color: #ffffff;
    border-radius: 50%;
    > span {
      position: relative;
      top: 4px;
    }
  }
  .DraftRequired {
    background-color: @colorDraft;
  }
  .PublishRequired {
    background-color: @colorPublished;
  }
}
.pull-right {
  position: absolute;
  right: 6px;
}
.warning {
  // color: @colorBrandAccentLight;
  cursor: pointer;
}
</style>
