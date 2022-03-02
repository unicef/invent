<template>
  <div class="change">
    <div class="field">{{ index + 1 }}) {{ changes.fieldTitle }}</div>
    <div v-for="(value, idx) in changes.values" :key="idx" :class="`value ${value.changeType}`">
      <i :class="value.changeTypeIcon"></i>
      <div class="partner">
        <div class="type"><translate>Type</translate>: {{ value.partner.type }}</div>
        <div><translate>Name</translate>: {{ value.partner.name }}</div>
        <div><translate>Contact</translate>: {{ value.partner.contact }}</div>
        <div><translate>Email</translate>: {{ value.partner.email }}</div>
        <div><translate>Website</translate>: {{ value.partner.website }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    index: {
      type: Number,
      default: 0,
    },
    changes: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.change {
  .field {
    font-weight: bold;
  }
  .value {
    display: flex;
    gap: 10px;
    margin-left: 19px;
    margin-top: 10px;
    .partner {
      font-size: @fontSizeSmall;
      line-height: 16px;
      .type {
        font-size: @fontSizeBase;
        line-height: 20px;
      }
    }
    &.new {
      color: @colorTextPrimary;
    }
    &.old {
      color: @colorTextMuted;
    }
    &.deleted {
      color: #f44336;
    }
  }
  i {
    margin-top: 3px;
  }
}
</style>
