<template>
  <div class="SelectorDialogColumn">
    <div class="Header">
      <span v-show="!headerSelectable">
        {{ header }}
      </span>
      <template v-if="expand">
        <span
          class="toggle-expand primary"
          @click="handleToggleExpand(false)"
        >
          <small><translate>Collapse</translate></small>
        </span>
        <span class="toggle-expand divider">/</span>
        <span
          class="toggle-expand primary"
          @click="handleToggleExpand(true)"
        >
          <small><translate>Expand</translate></small>
        </span>
      </template>
      <el-checkbox
        v-show="headerSelectable"
        :value="selected"
        @change="headerSelected"
      >
        {{ header }}
      </el-checkbox>
      <span v-show="!headerSelectable">{{ header }}</span>
    </div>
    <div class="Main">
      <slot />
    </div>
  </div>
</template>

<script>

export default {
  components: {
  },
  props: {
    header: {
      type: String,
      required: true
    },
    headerSelectable: {
      type: Boolean,
      default: false
    },
    selected: {
      type: Boolean,
      default: false
    },
    expand: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      expand: false
    };
  },
  computed: {
  },
  methods: {
    headerSelected (value) {
      this.$emit('headerSelected', value);
    },
    handleToggleExpand (val) {
      this.expand = val;
      this.$emit('handleToggleExpand', this.header, val);
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .SelectorDialogColumn {
    position: relative;

    .Header {
      position: fixed;
      z-index: 10000;
      box-sizing: border-box;
      padding: 0 30px;
      width: calc((90vw / 4) - 1px);
      max-width: calc((@appWidthMaxLimit * 0.9) / 4 - 1px);
      height: @dialogHeaderFooterHeight;
      line-height: @dialogHeaderFooterHeight;
      border-bottom: 1px solid @colorGrayLight;
      background-color: @colorGrayLightest;
      font-size: @fontSizeBase;
      font-weight: 700;
      text-transform: uppercase;

      .el-checkbox {
        .el-checkbox__label {
          font-weight: 700;
        }
      }
    }

    .Main {
      position: relative;
      top: @dialogHeaderFooterHeight;
      box-sizing: border-box;
      padding: 10px 20px 50px 30px;
      height: calc(80vh - (@dialogHeaderFooterHeight * 3));
      overflow-y: scroll;
    }

    .toggle-expand {
      text-transform: none;
      float: right;
      font-weight: 300;
      cursor: pointer;
      &.primary {
        color: @colorBrandPrimary;
      }
      &.divider{
        padding: 0 5px;
      }
    }
  }
</style>
