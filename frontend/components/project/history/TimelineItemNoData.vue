<template>
  <div class="TimeLineItem">
    <div class="event"></div>
    <div class="divider"></div>
    <div class="body">
      <translate>History data is unavailable for this period</translate>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimeLineItemNoData',
}
</script>

<style lang="less" scoped>
.TimeLineItem {
  display: flex;
  line-height: 28px;
  .event {
    width: 75px;
  }
  .divider {
    position: relative;
    width: 90px;
    &::before {
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      border-left: 1px dashed #eae6e1;
    }
  }
  .body {
    margin: 0 0 20px 18px;
  }
}
</style>
