<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-for="(value, idx) in changes.values" :key="idx" :class="`value ${value.changeType}`">
      <i :class="value.changeTypeIcon"></i>
      <img v-if="value.imageUrl" :src="value.imageUrl" class="cover" loading="lazy" />
      <a v-if="value.imageUrl" :href="value.imageUrl" target="_blank">{{ value.imageUrl }}</a>
      <span v-else>N/A</span>
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
    .cover {
      width: 38px;
      height: 38px;
      border-radius: 4px;
      object-fit: cover;
    }
    a {
      font-size: @fontSizeSmall;
      text-decoration: none;
      word-break: break-word;
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
