<template>
  <div
    class="WorldZoomButton"
    @click="zoomToWorld"
  >
    <fa
      icon="globe-africa"
    />
  </div>
</template>

<script>
export default {
  methods: {
    zoomToWorld () {
      this.$root.$emit('map:reset-zoom', 3);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .WorldZoomButton {
    position: absolute;
    z-index: 1010;
    right: 40px;
    bottom: 121px;
    display: inline-block;
    width: 30px;
    height: 30px;
    background-color: rgba(255,255,255,.9);
    border-radius: 2px;
    box-shadow: 0 0 20px 5px rgba(0,0,0,.15);
    cursor: pointer;
    transition: @transitionAll;

    &:hover {
      background-color: fade(@colorGrayLightest, 90%);

      .svg-inline--fa {
        color: @colorBrandPrimary;
      }
    }

    .svg-inline--fa {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 18px;
      color: @colorTextSecondary;
      transition: @transitionAll;
    }
  }
</style>
