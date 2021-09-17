<template>
  <div :class="`location ${size}`">
    <CountryFlag :code="locationInfo.countryCode" :size="size" />
    <span>{{ locationInfo.office }}</span>
    <span v-if="locationInfo.country" :class="{ divider: locationInfo.office }">
      {{ locationInfo.country }}
    </span>
    <span v-if="locationInfo.region" :class="{ divider: locationInfo.country }">{{ locationInfo.region }}</span>
  </div>
</template>

<script>
import CountryFlag from '@/components/common/CountryFlag.vue'

export default {
  components: {
    CountryFlag,
  },
  props: {
    locationInfo: {
      type: Object,
      required: true,
    },
    size: {
      type: String,
      default: 'small',
      validator: (value) => {
        return ['tiny', 'small'].includes(value)
      },
    },
  },
  coputed: {
    countryFlag() {
      if (this.project) {
        return `/static/flags/${this.landingData.code.toLowerCase()}.png`
      }
      return null
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.location {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7995a2;
  font-size: @fontSizeBase;
  margin-bottom: 14px;
  &.small {
    font-size: @fontSizeBase;
  }
  &.tiny {
    font-size: @fontSizeSmall;
  }
  span {
    position: relative;
    &.divider {
      &::before {
        content: '';
        border: 1px solid @colorBrandGrayLight;
        margin-right: 8px;
      }
    }
  }
}
</style>
