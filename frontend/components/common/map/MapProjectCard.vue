<template>
  <nuxt-link :to="projectUrl" class="MapProjectCard">
    <div class="name">
      {{ project.name }}
    </div>
    <div class="office">
      <span>{{ office.name }}</span>
      <span>&nbsp;|&nbsp;{{ region.name }}</span>
    </div>
    <fa icon="arrow-right" class="arrow" />
  </nuxt-link>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    project: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    ...mapGetters({
      offices: 'offices/getOffices',
      regions: 'system/getRegions',
    }),
    office() {
      const relOffice = this.offices.find((o) => o.id === this.project.country_office)
      return relOffice || ''
    },
    region() {
      return this.office ? this.regions.find((r) => r.id === this.office.region) : ''
    },
    projectUrl() {
      return this.localePath({
        name: 'organisation-initiatives-id-published',
        params: { ...this.$route.params, id: this.project.id },
      })
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';

.MapProjectCard {
  position: relative;
  display: block;
  padding: 12px;
  margin: 0 10px 8px;
  background-color: white;
  border: solid #d6d6d6;
  border-width: 1px 1px 2px;
  &:first-child {
    margin-top: 8px;
  }
  &:hover {
    .name {
      color: @colorBrandPrimary;
    }
    .arrow {
      opacity: 1;
    }
  }
  .name {
    padding-right: 12px;
    color: @colorTextPrimary;
    font-size: @fontSizeBase;
    font-weight: 700;
    line-height: 20px;
    // max-height: 40px;
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    -webkit-line-clamp: 1;
  }
  .office {
    padding-right: 12px;
    margin-top: 8px;
    color: @colorTextSecondary;
    font-size: @fontSizeSmall;
    font-weight: normal;
    line-height: 16px;
    // color: #6d6d6d;
    max-height: 16px;
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    -webkit-line-clamp: 1;
  }
  .arrow {
    position: absolute;
    top: calc(50% - 8px);
    right: 14px;
    opacity: 0;
    color: @colorBrandPrimary;
    transition: opacity 200ms ease;
  }
}
</style>
