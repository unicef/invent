<template>
  <div :class="['Header', `${postion}`]">
    <div class="title">
      <slot name="title" />
    </div>
    <div class="action">
      <slot name="action" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    postion: {
      type: String,
      default: 'top',
      validator: (value) => {
        return ['top', 'between'].includes(value)
      },
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.Header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  &.top {
    margin-bottom: 46px;
    .title {
      font-size: @fontSizeTitle;
    }
  }
  &.between {
    margin-top: 20px;
    margin-bottom: 34px;
    .title {
      font-size: @fontSizeLarge;
    }
  }
  .title {
    color: @colorTextPrimary;
    font-size: @fontSizeTitle;
  }
  .action {
    display: flex;
    gap: 30px;
  }
}
</style>
