<template>
  <div
    v-model="innerValue"
    v-bind="{ ...$props, ...$attrs }"
    v-on="{ ...$listeners }"
    class="icon-select"
  >
    <div v-if="!$attrs.value" class="dropdown" @click="open = true">
      <span><translate>Choose icon</translate></span>
      <fa icon="sort-down" />
    </div>
    <div v-else>{{ $attrs.value }}</div>
    <!-- <p @click="handleClick">click here</p> -->
    <div v-if="open" class="select">
      me abri
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  model: {
    prop: "value",
    event: "change"
  },
  computed: {
    innerValue: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("change", value);
      }
    }
  },
  data() {
    return {
      open: false
    };
  },
  mounted() {},
  methods: {
    handleClick() {
      this.innerValue = 1;
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.icon-select {
  position: relative;
  .dropdown {
    display: flex;
    align-items: baseline;
    cursor: pointer;
    color: @colorBrandPrimary;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;
    margin-top: 10px;
    svg {
      margin-left: 6px;
    }
  }
  .select {
    position: absolute;
    top: 0;
    z-index: 100;
    height: 301px;
    width: 274px;
    background-color: #ffffff;
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.18);
    overflow: hidden;
    overflow-y: scroll;
  }
}
</style>
