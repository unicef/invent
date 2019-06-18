<template>
  <el-row class="CheckboxAndLink">
    <el-col :span="12">
      <el-checkbox
        :value="selected"
        @change="selectedChangeHandler"
      >
        {{ item.pre }} {{ item.name }}
      </el-checkbox>
    </el-col>
    <el-col :span="12">
      <el-form-item :error="errors.first('link', 'interoperability_link_' + index)">
        <el-input
          v-model="innerLinkValue"
          v-validate="rules.interoperability_links"
          :disabled="!selected"
          :placeholder="$gettext('Specify URL') | translate"
          :data-as-name="item.pre + item.name"
          :data-vv-scope="'interoperability_link_' + index"
          data-vv-name="link"
          type="text"
        />
      </el-form-item>
    </el-col>
  </el-row>
</template>

<script>
import VeeValidationMixin from '../mixins/VeeValidationMixin.js';

export default {
  mixins: [VeeValidationMixin],
  props: {
    item: {
      type: Object,
      required: true
    },
    interoperabilityLinks: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      default: null
    }
  },
  computed: {
    interoperabilityLink () {
      if (this.interoperabilityLinks && this.item) {
        return this.interoperabilityLinks[this.item.id] || {};
      }
      return {};
    },
    selected () {
      return this.interoperabilityLink.selected;
    },
    link () {
      return this.interoperabilityLink.link;
    },
    innerLinkValue: {
      get () {
        return this.link;
      },
      set (link) {
        const ir = { ...this.interoperabilityLinks };
        ir[this.item.id] = { ...this.interoperabilityLink, link };
        this.$emit('update:interoperabilityLinks', ir);
      }
    }
  },
  methods: {
    selectedChangeHandler (selected) {
      const ir = { ...this.interoperabilityLinks };
      ir[this.item.id] = { ...this.interoperabilityLink, selected };
      this.$emit('update:interoperabilityLinks', ir);
    },
    async validate () {
      return this.$validator.validate();
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .CheckboxAndLink {
    margin-bottom: 20px;

    .el-checkbox {
      padding-right: 30px;
      box-sizing: border-box;
      line-height: 19px;
      padding: 10px 0;

      .el-checkbox__input {
        vertical-align: top;
        top: 2px;
      }

      .el-checkbox__label {
        white-space: normal;
        padding-right: 30px;
      }
    }
  }
</style>
