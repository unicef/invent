<template>
  <div :class="['DhaMap', 'LandingMap', {'Searched': isSearched}]">
    <no-ssr>
      <l-map
        ref="mainMap"
        :zoom="zoom"
        :world-copy-jump="true"
        :options="mapOptions"
        @zoomend="zoomChangeHandler"
        @leaflet:load="setMapReady(true)"
      >
        <l-tilelayer
          :url="tileServer"
        />

        <custom-marker-cluster
          ref="markerCluster"
          :options="clusterOptions"
          :total="countriesPin.length"
        >
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
          :national-level-coverage="activeTab ==='national'"
          :sub-national-projects="subNationalProjects"
          :national-projects="nationalProjects"
        />
        <switch-view-box
          v-if="activeCountry"
          :active-tab.sync="activeTab"
        />
        <world-zoom-button />

        <l-control-zoom
          position="bottomright"
        />
      </l-map>
    </no-ssr>
  </div>
</template>

<script>

import MapMixin from '../mixins/MapMixin';

import NoSSR from 'vue-no-ssr';
import CountryCenterMarker from '../common/map/CountryCenterMarker';
import CountryDetailsOverlay from '../common/map/CountryDetailsOverlay';
import WorldZoomButton from '../common/map/WorldZoomButton';
import SwitchViewBox from '../common/map/SwitchViewBox';

export default {
  components: {
    'no-ssr': NoSSR,
    CountryCenterMarker,
    CountryDetailsOverlay,
    WorldZoomButton,
    SwitchViewBox
  },
  mixins: [MapMixin]
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .LandingMap {
    height: @landingMapHeight;
    min-height: @landingMapMinHeight;
  }
</style>
