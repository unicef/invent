<template>
  <span class="link" :class="{ greyed: disabled }" @click="$emit('click')">
    <nuxt-link v-if="url" :to="url">
      <fa v-if="chevron === 'left'" class="left" icon="chevron-left" size="sm" />
      <slot />
      <fa v-if="chevron === 'right'" class="right" icon="chevron-right" size="sm" />
    </nuxt-link>
    <template v-else>
      <fa v-if="chevron === 'left'" class="left" icon="chevron-left" size="sm" />
      <slot />
      <fa v-if="chevron === 'right'" class="right" icon="chevron-right" size="sm" />
    </template>
  </span>
</template>

<script>
export default {
  props: {
    chevron: {
      type: String,
      default: 'none',
      validator: (value) => {
        return ['none', 'left', 'right'].includes(value)
      },
    },
    url: {
      type: String,
      default: '',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.link {
  cursor: pointer;
  font-size: @fontSizeBase;
  color: @colorBrandPrimary;
  font-weight: bold;
  letter-spacing: 0.25px;
  line-height: 18px;
  a {
    text-decoration: none;
  }
}
.left {
  font-size: 0.9em;
  margin-right: 4px;
}
.right {
  font-size: 0.9em;
  margin-left: 4px;
}
.greyed {
  color: #a8a8a9;
  cursor: default;
}
</style>
