<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-if="!isNothing(changes.values.added.value)" :class="`value ${changes.values.added.changeType}`">
      <i :class="` ${changes.values.added.changeTypeIcon}`"></i>
      <span>{{ changes.values.added.value }}</span>
    </div>
    <div v-if="!isNothing(changes.values.removed.value)" :class="`value ${changes.values.removed.changeType}`">
      <i :class="` ${changes.values.removed.changeTypeIcon}`"></i>
      <span>{{ changes.values.removed.value }}</span>
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
  methods: {
    isNothing(value) {
      return value === null || value === ''
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
    white-space: pre-line;
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
