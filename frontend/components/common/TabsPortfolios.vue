<template>
  <div class="tabs-wrapper">
    <div class="tabs-col">
      <div class="title">
        <slot name="title" />
      </div>
      <div :class="`tabs ${center && 'center'}`">
        <p
          v-for="item in tabs"
          :key="item.id"
          :class="`${item.id === tab && 'active'}`"
          @click="$emit('handleTab', item.id)"
        >
          <fa :icon="item.icon" size="lg" />
          {{ $gettext(item.name) | translate }}
          <template v-if="item.total">
            {{ ` (${item.total})` }}
          </template>
        </p>
        <span></span>
      </div>
    </div>
    <div class="actionButton">
      <slot name="actionButton" />
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
    center: {
      type: Boolean,
      default: true,
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
  display: flex;
  flex-direction: row;

  .tabs-col {
    display: flex;
    flex-direction: column;
  }
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
  .actionButton {
    margin: 0 0 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }
  .tabs {
    display: flex;
    &.center {
      align-items: center;
      justify-content: center;
    }
    p {
      cursor: pointer;
      color: @colorBrandGrayDark;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0;
      line-height: 18px;
      padding-bottom: 16px;
      margin: 0 32px 0 0;
      border-bottom: 3px solid transparent;
      svg {
        margin-right: 8px;
        color: #a8a8a9;
      }
      &.active {
        color: @colorTextPrimary;
        font-weight: bold;
        border-bottom: 3px solid @colorBrandPrimary;
        svg {
          color: @colorTextPrimary;
        }
      }
    }
  }
}
</style>
