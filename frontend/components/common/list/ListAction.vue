<template>
  <el-button
    class="ListActionButton"
    type="text"
    @click="$emit('click')"
  >
    <fa
      icon="check"
      class="normal"
    />
    <fa
      icon="times"
      class="hovered"
    />
  </el-button>
</template>

<script>
export default {

};
</script>

<style lang="less">
  .ListActionButton {
     .hovered {
        display: none;
      }
    &:hover {
      .normal {
        display: none;
      }
      .hovered {
        display: inline;
      }
    }
  }

</style>
