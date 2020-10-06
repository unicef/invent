<template>
  <div class="SwitchViewBox">
    <div class="SwitchViewWrapper">
      <el-switch
        :value="activeTab"
        :active-text="$gettext('National') | translate"
        :inactive-text="$gettext('Sub-national') | translate"
        active-value="national"
        active-color="#F26A21"
        inactive-value="subNational"
        inactive-color="#FFC20E"
        @change="setActiveTab($event)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    activeTab: {
      type: String,
      required: true,
    },
  },
  methods: {
    setActiveTab($event) {
      this.$emit('update:activeTab', $event)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SwitchViewBox {
  z-index: 1010;
  position: relative;

  .SwitchViewWrapper {
    position: absolute;
    right: 40px;
    top: 40px;
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 2px;
    box-shadow: 0 0 20px 5px rgba(0, 0, 0, 0.15);

    .el-switch {
      .el-switch__label {
        color: @colorGray;
        font-weight: 700;

        &.is-active {
          color: @colorTextPrimary;
        }
      }
    }
  }
}
</style>
