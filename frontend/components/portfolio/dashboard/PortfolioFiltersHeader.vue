<template>
  <div class="header">
    <fa icon="bars" size="sm" />
    <p>
      <b>{{ total }}</b>
      <translate>project(s) to show</translate>
    </p>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters({
      total: "dashboard/getTotal"
    })
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.header {
  display: flex;
  align-items: center;
  background-color: #44c9f6;
  box-shadow: -1px 0 0 0 @colorBrandPrimary;
  padding: 1px 20px;
  transform: translateX(40px);
  svg {
    color: @colorWhite;
    margin-right: 8px;
  }
  p {
    color: @colorWhite;
    font-size: 14px;
    letter-spacing: 0;
    line-height: 18px;
  }
}
</style>
