<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div :class="`value ${changes.values.changeType}`">
      <i :class="` ${changes.values.changeTypeIcon}`"></i>
      {{ changes.values.value }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    index: {
      type: Number,
      default: 0,
    },
    changes: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.change {
  .field {
    font-weight: bold;
  }
  .value {
    display: flex;
    gap: 10px;
    margin-left: 19px;
    margin-top: 10px;
    word-break: normal;
    line-height: 20px;
    &.edit {
      color: @colorTextPrimary;
      i {
        font-weight: bold;
      }
    }
  }
  i {
    margin-top: 3px;
  }
}
</style>
