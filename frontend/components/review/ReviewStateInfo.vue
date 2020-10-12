<template>
  <div class="review-state">
    <div>
      <p v-if="complete" key="complete-info" class="completed">
        <fa icon="check-circle" /><translate>Reviewed</translate>
      </p>
      <p v-else key="not-complete-info" class="not-completed">
        <fa icon="comment-slash" /><translate>Unscored</translate>
      </p>
    </div>
    <div class="info">
      <translate :parameters="{ name: portfolio }">
        Review for '{name}'
      </translate>
    </div>
    <div>
      <slot name="actions" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    complete: {
      type: Boolean,
      required: true,
      default: false,
    },
    portfolio: {
      type: String,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.review-state {
  height: inherit;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  .completed {
    color: #0eb455;
  }
  .not-completed {
    color: @colorBrandAccent;
  }
  .info {
    font-size: @fontSizeBase;
    font-weight: 400;
    color: @colorBrandGrayDark;
    margin-left: 12px;
    padding-left: 12px;
    border-left: 1px solid #ddd7d0;
  }
  div:last-child {
    margin-left: auto;
    p {
      cursor: pointer;
    }
    .completed {
      color: @colorBrandPrimary;
    }
  }
  svg {
    margin-right: 8px;
  }
  p {
    font-size: @fontSizeBase;
    font-weight: bold;
    letter-spacing: -0.2px;
    line-height: 18px;
  }
}
</style>
