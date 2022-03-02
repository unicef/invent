<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-for="(value, idx) in changes.values" :key="idx" :class="`value ${value.changeType}`">
      <i :class="value.changeTypeIcon"></i>
      <div>
        <div v-for="(tag, i) in value.tags" :key="i" class="tag">
          {{ tag }}
        </div>
      </div>
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
    .tag {
      line-height: 20px;
    }
    &.new {
      color: @colorTextPrimary;
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
