<template>
  <div :class="style">
    <translate v-if="status === 'draft'" key="draft">Draft</translate>
    <translate v-if="status === 'published'" key="pub">Published</translate>
    <translate v-if="status === 'unpublished'" key="unpub">Unublished</translate>
  </div>
</template>

<script>
export default {
  props: {
    status: {
      type: String,
      default: 'draft',
      required: true,
      validator: (val) =>
        ['created', 'noversionDraft', 'noversionPublished', 'draft', 'published', 'unpublished'].includes(val),
    },
    large: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    style() {
      return `badge ${this.status} ${this.large ? 'large' : ''}`
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.badge {
  text-transform: uppercase;
  font-size: 9px;
  font-weight: 700;
  text-align: center;
  border-radius: 12px;
  width: 78px;
  height: 22px;
  line-height: 22px;
  &.draft {
    color: @colorTextPrimary;
    background-color: @colorDraft;
  }
  &.published {
    color: @colorWhite;
    background-color: @colorPublished;
  }
  &.unpublished {
    color: @colorWhite;
    background-color: #f44336;
  }
  &.large {
    font-size: 11px;
    width: 90px;
    height: 23px;
    line-height: 23px;
  }
}
</style>
