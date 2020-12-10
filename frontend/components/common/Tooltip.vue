<template>
  <span class="TooltipContainer">
    <el-tooltip
      :content="text"
      :placement="placement"
      effect="dark"
      popper-class="TooltipElement"
    >
      <fa icon="question-circle" />
    </el-tooltip>
  </span>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true,
    },
    placement: {
      type: String,
      default: 'right',
    },
  },
}
</script>

<style lang="less">
.TooltipContainer {
  width: auto;
  color: #9b9b9b !important;
}
.TooltipElement {
  max-width: 257px;
}
</style>
