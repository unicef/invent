<template>
  <div
    class="Circle"
    :style="`left: ${left}px; top: ${top}px`"
    v-on="$listeners"
  >
    <div
      :class="`Shape ${state}`"
      :style="`width: ${size}px; height: ${size}px`"
    />
  </div>
</template>

<script>
const size = 560;
export default {
  name: 'MatrixElement',
  props: {
    x: {
      type: Number,
      required: true
    },
    y: {
      type: Number,
      required: true
    },
    ratio: {
      type: Number,
      required: true
    },
    state: {
      type: String,
      default: ''
    }
  },
  computed: {
    left () {
      return Math.floor(size / 5 * (this.x - 1));
    },
    top () {
      return Math.floor(size / 5 * (5 - this.y));
    },
    size () {
      return Math.floor(this.ratio * 100 / 25 + 1) * 20;
    }
  }
};
</script>

<style lang="less" scoped>
.Circle {
  position: absolute;
  width: 100px;
  height: 100px;
  cursor: pointer;
  .Shape {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background-color: #154051;
    opacity: 0.8;
    &.inactive {
      opacity: 0.4;
    }
    &.active {
      opacity: 1;
      box-shadow: 5px 5px 20px 0 rgba(0,0,0,0.12);
    }
  }
}
</style>
