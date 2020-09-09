<template>
  <div
    :class="`Radio ${trueValue ? 'Selected' : ''} ${disabled ? 'Disabled' : ''}`"
    @click="update"
  >
    <i
      v-show="trueValue"
      class="fas fa-check-circle"
    />
    <i
      v-show="!trueValue"
      class="far fa-circle"
    />
    <span>
      <slot />
    </span>
  </div>
</template>

<script>
export default {
  name: 'Radio',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    trueValue () {
      return this.disabled ? false : this.value;
    }
  },
  methods: {
    update () {
      if (this.disabled) {
        return;
      }
      this.$emit('update', !this.value);
    }
  }
};
</script>

<style lang="less" scoped>
.Radio {
  padding: 11px;
  margin: 1px 10px;
  cursor: pointer;
  border: 1px solid transparent;
  &.Disabled {
    opacity: 0.4;
  }
  &.Selected {
    span {
      font-weight: bold;
    }
  }
  .fa-check-circle, .fa-circle {
    margin-top: 1px;
    position: absolute;
  }
  span {
    display: block;
    margin-left: 28px;
    color: #404041;
    font-size: 14px;
    letter-spacing: 0;
    line-height: 20px;
  }
  &:not(.Disabled):hover {
    border: 1px solid #404041;
    border-radius: 5px;
    span {
      //font-weight: bold;
    }
  }
}
</style>
