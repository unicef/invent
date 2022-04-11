<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div :class="`value ${changes.values.added.changeType}`">
      <i :class="` ${changes.values.added.changeTypeIcon}`"></i>
      <template v-if="changes.values.added.value">
        {{ changes.values.added.value }}
      </template>
      <template v-else>N/A</template>
    </div>
    <div :class="`value ${changes.values.removed.changeType}`">
      <i :class="` ${changes.values.removed.changeTypeIcon}`"></i>
      <template v-if="changes.values.removed.value">
        {{ changes.values.removed.value }}
      </template>
      <template v-else>N/A</template>
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
    &.new {
      color: @colorTextPrimary;
      i {
        font-weight: bold;
      }
    }
    &.old {
      color: @colorTextMuted;
    }
    &.deleted {
      color: #f44336;
    }
  }
  i {
    margin-top: 3px;
  }
}
</style>
