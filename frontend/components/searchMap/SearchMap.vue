<template>
  <div :class="['DhaMap', 'DashboardMap', { Searched: isSearched }]">
    <no-ssr>
      <l-map
        ref="mainMap"
        :zoom="zoom"
        :world-copy-jump="true"
        :options="mapOptions"
        @zoomend="zoomChangeHandler"
        @leaflet:load="setMapReady(true)"
      >
        <l-tilelayer :url="tileServer" />

        <custom-marker-cluster
          ref="markerCluster"
          :options="clusterOptions"
          :total="countriesPin.length"
        >
          <country-center-marker
            v-for="pin in countriesPin"
            :key="pin.id"
            :icon="countryCenterIcons[pin.id]"
            :options="countryCenterOptions[pin.id]"
            :pin="pin"
            :selected-country.sync="selectedCountry"
            :active-country.sync="activeCountry"
          />
        </custom-marker-cluster>

        <country-details-overlay
          :selected-country="selectedCountry"
          :active-country.sync="activeCountry"
          :geo-json="geoJson"
          :sub-level-pins="subLevelPins"
          :map-ready="mapReady"
          :selected-country-pin="selectedCountryPin"
          :active-sub-level.sync="activeSubLevel"
          :national-level-coverage="true"
          :sub-national-projects="subNationalProjects"
          :national-projects="nationalProjects"
        />
        <world-zoom-button />

        <l-control-zoom position="bottomright" />
      </l-map>
    </no-ssr>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import NoSSR from 'vue-no-ssr'

import CountryCenterMarker from '@/components/common/map/CountryCenterMarker'
import CountryDetailsOverlay from '@/components/common/map/CountryDetailsOverlay'
import WorldZoomButton from '@/components/common/map/WorldZoomButton'

import MapMixin from '@/components/mixins/MapMixin'

export default {
  components: {
    'no-ssr': NoSSR,
    CountryCenterMarker,
    CountryDetailsOverlay,
    WorldZoomButton,
  },
  mixins: [MapMixin],
  computed: {
    ...mapGetters({
      // non related
      allCountriesPin: 'search/getCountryPins',
      getActiveCountry: 'search/getActiveCountry',
      getSelectedCountry: 'search/getSelectedCountry',
      getCountryProjects: 'search/getCountryProjects',
      getActiveTab: 'search/getProjectBoxActiveTab',
      mapProjects: 'search/getProjectsMap',
      currentZoom: 'search/getCurrentZoom',
      getSearched: 'dashboard/getSearched',
      // related
      geoJson: 'countries/getGeoJsonLibrary',
      subLevelPins: 'search/getSubLevelPins',
      mapReady: 'search/getMapReady',
      subNationalProjects: 'search/getSelectedCountrySubNationalProjects',
      nationalProjects: 'search/getSelectedCountryNationalProjects',
    }),
  },
  beforeDestroy() {
    this.setActiveCountry(null)
  },
  methods: {
    ...mapActions({
      // non related
      setCurrentZoom: 'search/setCurrentZoom',
      setSelectedCountry: 'search/setSelectedCountry',
      setActiveCountry: 'search/setActiveCountry',
      // related
      setMapReady: 'search/setMapReady',
      setActiveTab: 'search/setProjectBoxActiveTab',
    }),
  },
}
</script>

<style lang="less">
// @import '~assets/style/variables.less';
// @import '~assets/style/mixins.less';

.DashboardMap {
  height: 80vh;
}
</style>
