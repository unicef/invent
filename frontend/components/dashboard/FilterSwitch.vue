<template>
  <el-row
    type="flex"
    justify="space-between"
    align="middle"
    class="FilterSwitch"
  >
    <el-col class="SwitchComponent">
      <el-row type="flex" align="middle">
        <el-col class="SwitchHandler">
          <el-switch :value="value" @change="switchChangeHandler" />
        </el-col>
        <el-col class="SwitchLabel">
          {{ label }}
        </el-col>
      </el-row>
    </el-col>
    <el-col class="SwitchTooltip">
      <el-tooltip
        v-model="showTooltip"
        :content="tooltip"
        effect="dark"
        placement="left"
        popper-class="FilterSwitchTooltip"
        manual
      >
        <el-button
          type="text"
          class="MutedButton"
          @click="showTooltip = !showTooltip"
        >
          <fa icon="question-circle" />
        </el-button>
      </el-tooltip>
    </el-col>
  </el-row>
</template>

<script>
export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      required: true,
    },
    tooltip: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showTooltip: false,
    }
  },
  methods: {
    switchChangeHandler(value) {
      this.$emit('change', value)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FilterSwitch {
  margin-bottom: 10px;

  &:last-child {
    margin: 0;
  }

  .SwitchComponent {
    width: 100%;

    .SwitchHandler {
      width: auto;
      padding-right: 10px;
    }

    .SwitchLabel {
      font-size: @fontSizeBase;
      line-height: 19px;
      color: @colorTextPrimary;
    }
  }

  .SwitchTooltip {
    width: auto;
    padding-left: 10px;

    .el-button {
      padding: 0;
    }
  }
}

.FilterSwitchTooltip {
  max-width: @advancedSearchWidth;
}
</style>
