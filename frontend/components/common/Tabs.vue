<template>
  <div class="tabs-wrapper">
    <div class="title">
      <slot name="title" />
    </div>
    <div class="tabs">
      <p
        v-for="item in tabs"
        :key="item.id"
        :class="`${item.id === tab && 'active'}`"
        @click="$emit('handleTab', item.id)"
      >
        <fa :icon="item.icon" />
        {{ $gettext(item.name) | translate }}
        {{ ` (${item.total})` }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      required: true,
    },
    tab: {
      type: Number,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.tabs-wrapper {
  // height: 158px;
  background-color: @colorWhite!important;
  padding: 0 43px;
  .title {
    display: flex;
    align-items: center;
    padding-top: 50px;
    padding-bottom: 25px;
    h2 {
      margin: 0;
      color: @colorBrandPrimary;
      font-size: 36px;
      letter-spacing: -1px;
      line-height: 45px;
      font-weight: 100;
      flex-grow: 2;
      text-align: center;
    }
    .translate {
      transform: translateX(-25px);
    }
    a {
      text-decoration: none;
      z-index: 1;
    }
  }
  .tabs {
    display: flex;
    align-items: center;
    justify-content: center;
    p {
      cursor: pointer;
      color: @colorBrandGrayDark;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0;
      line-height: 18px;
      padding-bottom: 17px;
      margin: 0 15px;
      border-bottom: 3px solid transparent;
      svg {
        margin-right: 8px;
      }
      &.active {
        color: @colorTextPrimary;
        border-bottom: 3px solid @colorBrandPrimary;
      }
    }
  }
}
</style>
