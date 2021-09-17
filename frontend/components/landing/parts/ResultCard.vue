<template>
  <nuxt-link class="ResultProject" :to="projectUrl">
    <div v-if="project.cover" class="cover" :style="`background-image: url(${project.cover})`"></div>
    <div class="project">
      <h1>{{ project.name }}</h1>
      <Location :location-info="locationInfo" size="tiny" />
      <div class="foundin">
        <fa icon="search" size="sm" />
        <translate :parameters="{ found }">Found in "{found}"</translate>
      </div>
    </div>
  </nuxt-link>
</template>

<script>
import Location from '@/components/landing/parts/Location.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    Location,
  },
  props: {
    project: {
      type: Object,
      required: true,
    },
    foundIn: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      getOfficeDetails: 'offices/getOfficeDetails',
      getRegionDetails: 'system/getRegionDetails',
    }),
    projectUrl() {
      return this.localePath({
        name: 'organisation-initiatives-id-published',
        params: { ...this.$route.params, id: this.project.id },
      })
    },
    country() {
      return this.getCountryDetails(this.project.country)
    },
    office() {
      return this.getOfficeDetails(this.project.country_office)
    },
    region() {
      return this.getRegionDetails(this.country.unicef_region)
    },
    locationInfo() {
      return {
        countryCode: this.country?.code,
        country: this.country?.name,
        office: this.office?.name,
        region: this.region?.name,
      }
    },
    found() {
      const nameMApping = {
        country: this.$gettext('Country'),
        donor: this.$gettext('Investor'),
        loc: this.$gettext('Location'),
        name: this.$gettext('Name'),
        desc: this.$gettext('Description'),
        org: this.$gettext('Organisation'),
        overview: this.$gettext('Implementation Overview'),
        partner: this.$gettext('Partners'),
        region: this.$gettext('Region'),
      }
      if (this.foundIn) {
        return this.foundIn.map((f) => nameMApping[f]).join(', ')
      }
      return ''
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.ResultProject {
  display: flex;
  height: 108px;
  width: 480px;
  border-radius: 3px;
  overflow: hidden;
  background-color: #ffffff;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.08), 1px 2px 4px 0 rgba(0, 0, 0, 0.12);
  text-decoration: none;
  .cover {
    flex-basis: 144px;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center bottom;
  }
  .project {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
    margin: 8px 16px;
    h1 {
      margin: 0 0 8px 0;
      max-height: 40px;
      font-size: @fontSizeMedium;
      color: @colorBrandPrimary;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }
    .foundin {
      position: absolute;
      bottom: 0;
      font-size: @fontSizeSmall;
      height: 20px;
      color: #a8a8a9;
      letter-spacing: 0;
      line-height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      .svg-inline--fa {
        position: relative;
        margin-right: 4px;
      }
    }
  }
}
</style>
