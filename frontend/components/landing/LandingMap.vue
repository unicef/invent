<template>
  <div :class="['DhaMap', 'LandingMap', { Searched: isSearched }]">
    <no-ssr>
      <SearchComponent />
      <l-map
        ref="mainMap"
        :zoom="zoom"
        :world-copy-jump="true"
        :options="mapOptions"
        @zoomend="zoomChangeHandler"
        @leaflet:load="setMapReady(true)"
      >
        <l-tilelayer :url="tileServer" />

        <custom-marker-cluster ref="markerCluster" :options="clusterOptions" :total="countriesPin.length">
          <country-center-marker
            v-for="pin in countriesPin"
            :key="pin.id"
            :icon="countryCenterIcons[pin.id]"
            :pin="pin"
            :options="countryCenterOptions[pin.id]"
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
import NoSSR from 'vue-no-ssr'
import MapMixin from '@/components/mixins/MapMixin'

import SearchComponent from '@/components/common/SearchComponent.vue'
import CountryCenterMarker from '@/components/common/map/CountryCenterMarker'
import CountryDetailsOverlay from '@/components/common/map/CountryDetailsOverlay'
import WorldZoomButton from '@/components/common/map/WorldZoomButton'

export default {
  components: {
    'no-ssr': NoSSR,
    SearchComponent,
    CountryCenterMarker,
    CountryDetailsOverlay,
    WorldZoomButton,
  },
  mixins: [MapMixin],
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.LandingMap {
  height: @landingMapHeight;
  min-height: @landingMapMinHeight;
  max-height: @landingMapMaxHeight;
}
</style>
