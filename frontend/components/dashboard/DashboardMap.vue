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
import MapMixin from '../mixins/MapMixin'

import CountryCenterMarker from '../common/map/CountryCenterMarker'
import CountryDetailsOverlay from '../common/map/CountryDetailsOverlay'
import WorldZoomButton from '../common/map/WorldZoomButton'

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
      allCountriesPin: 'dashboard/getCountryPins',
      getActiveCountry: 'dashboard/getActiveCountry',
      geoJson: 'countries/getGeoJsonLibrary',
      getSelectedCountry: 'dashboard/getSelectedCountry',
      subLevelPins: 'dashboard/getSubLevelPins',
      getCountryProjects: 'dashboard/getCountryProjects',
      mapReady: 'dashboard/getMapReady',
      getActiveTab: 'dashboard/getProjectBoxActiveTab',
      subNationalProjects: 'dashboard/getSelectedCountrySubNationalProjects',
      nationalProjects: 'dashboard/getSelectedCountryNationalProjects',
      mapProjects: 'dashboard/getProjectsMap',
      currentZoom: 'dashboard/getCurrentZoom',
      getSearched: 'dashboard/getSearched',
    }),
  },
  methods: {
    ...mapActions({
      setCurrentZoom: 'dashboard/setCurrentZoom',
      setMapReady: 'dashboard/setMapReady',
      setSelectedCountry: 'dashboard/setSelectedCountry',
      setActiveCountry: 'dashboard/setActiveCountry',
      setActiveTab: 'dashboard/setProjectBoxActiveTab',
    }),
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.DashboardMap {
  height: 80vh;
}
</style>
