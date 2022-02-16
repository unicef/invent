<template>
  <div class="Timeline">
    <slot />
  </div>
</template>

<script>
export default {}
</script>

<style lang="less" scoped>
.Timeline {
  display: flex;
  flex-direction: column;
  padding: 30px 40px;
}
</style>
