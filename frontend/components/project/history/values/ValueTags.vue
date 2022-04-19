<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-if="changedValues.length === 0" class="value old warning">
      <i class="el-icon-warning-outline"></i>
      <translate>Can't find the changes</translate>
    </div>
    <div v-for="(value, idx) in changedValues" :key="idx" :class="`value ${value.changeType}`">
      <i :class="value.changeTypeIcon"></i>
      <div class="tag">
        {{ value.value }}
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
  computed: {
    changedValues() {
      const added = this.changes.values.added.value.reduce((tags, v) => {
        tags.push({
          changeType: this.changes.values.added.changeType,
          changeTypeIcon: this.changes.values.added.changeTypeIcon,
          value: v,
        })
        return tags
      }, [])
      const removed = this.changes.values.removed.value.reduce((tags, v) => {
        tags.push({
          changeType: this.changes.values.removed.changeType,
          changeTypeIcon: this.changes.values.removed.changeTypeIcon,
          value: v,
        })
        return tags
      }, [])
      return [...added, ...removed]
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
    &.warning {
      align-items: center;
      i {
        margin: 0;
      }
    }
    .tag {
      line-height: 20px;
      word-break: break-word;
    }
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
