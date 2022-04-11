<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-for="(value, idx) in changes.values" :key="idx" :class="`value ${value.changeType}`">
      <i :class="value.changeTypeIcon"></i>
      <div>
        <div>{{ value.value.website }}</div>
        <div>
          <a :href="value.value.url" target="_blank">{{ value.value.url }}</a>
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
    line-height: 20px;
    a {
      font-size: @fontSizeSmall;
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }

    &.new {
      color: @colorTextPrimary;
      a {
        color: @colorBrandPrimary;
        &:hover {
          color: @colorBrandPrimaryLight;
        }
      }
    }
    &.old {
      color: @colorTextMuted;
      a {
        color: @colorTextMuted;
        &:hover {
          color: @colorTextSecondary;
        }
      }
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
