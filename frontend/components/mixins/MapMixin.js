import { mapGetters, mapActions } from 'vuex'

const MapMixin = {
  data() {
    return {
      zoom: 2,
      countryCenterIcons: {},
      countryCenterOptions: {},
      mapOptions: {
        zoomControl: false,
        attributionControl: false,
        scrollWheelZoom: false,
      },
    }
  },
  computed: {
    ...mapGetters({
      // related
      allCountriesPin: 'landing/getCountryPins',
      getActiveCountry: 'landing/getActiveCountry',
      getSelectedCountry: 'landing/getSelectedCountry',
      getCountryProjects: 'landing/getCountryProjects',
      mapReady: 'landing/getMapReady',
      getActiveTab: 'landing/getProjectBoxActiveTab',
      getActiveSubLevel: 'landing/getActiveSubLevel',
      mapProjects: 'landing/getProjectsMap',
      currentZoom: 'landing/getCurrentZoom',
      getSearched: 'landing/getSearched',
      // non related
      geoJson: 'countries/getGeoJsonLibrary',
      subLevelPins: 'landing/getSubLevelPins',
      subNationalProjects: 'landing/getSelectedCountrySubNationalProjects',
      nationalProjects: 'landing/getSelectedCountryNationalProjects',
    }),
    isSearched() {
      return !!this.getSearched
    },
    tileServer() {
      if (this.$i18n.locale === 'ar') {
        return 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png?lang=ar'
      }
      return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
    },
    activeCountry: {
      get() {
        return this.getActiveCountry
      },
      set(value) {
        this.setActiveCountry(value)
      },
    },
    selectedCountry: {
      get() {
        return this.getSelectedCountry
      },
      set(value) {
        this.setSelectedCountry(value)
      },
    },
    activeTab: {
      get() {
        return this.getActiveTab
      },
      set(value) {
        this.setActiveTab(value)
      },
    },
    activeSubLevel: {
      get() {
        return this.getActiveSubLevel
      },
      set(value) {
        this.setActiveSubLevel(value)
      },
    },
    countriesPin() {
      return this.allCountriesPin
        ? this.allCountriesPin.filter((cp) => cp.id !== this.selectedCountry)
        : []
    },
    selectedCountryPin() {
      return this.allCountriesPin.find((cp) => cp.id === this.selectedCountry)
    },
    activeCountryAndMapReady() {
      if (this.activeCountry && this.mapReady) {
        return this.activeCountry
      }
    },
    selectedCountryAndMapReady() {
      if (this.mapReady) {
        return this.selectedCountry
      }
    },
    clusterOptions() {
      return {
        disableClusteringAtZoom: 8,
        spiderfyOnMaxZoom: false,
        polygonOptions: {
          stroke: false,
          fillColor: '#42B883',
        },
        iconCreateFunction: (cluster) => {
          if (cluster) {
            const projects = cluster
              .getAllChildMarkers()
              .reduce((a, c) => a + c.options.projects, 0)
            const html = `<span>${projects}</span>`
            const classes = ['CountryClusterIcon']
            if (projects === 0) {
              classes.push('EmptyCluster')
            }
            // eslint-disable-next-line
            return L.divIcon({
              className: classes.join(' '),
              html,
              iconSize: [40, 40],
              iconAnchor: [20, 40],
            })
          }
          // eslint-disable-next-line
          return L.divIcon({})
        },
      }
    },
  },
  watch: {
    activeCountryAndMapReady: {
      immediate: true,
      handler(id, old) {
        if (old) {
          ;[
            this.countryCenterIcons[old],
            this.countryCenterOptions[old],
          ] = this.pinOptionsAndIconGenerator(old, false)
        }
        if (id) {
          ;[
            this.countryCenterIcons[id],
            this.countryCenterOptions[id],
          ] = this.pinOptionsAndIconGenerator(id, true)
        }
      },
    },
    mapProjects: {
      immediate: false,
      handler() {
        this.iconsGenerator()
        this.$nextTick(() => {
          if (this.$refs.markerCluster.mapObject) {
            try {
              this.$refs.markerCluster.mapObject.refreshClusters()
            } catch (e) {
              console.log(e)
            }
          }
        })
      },
    },
    selectedCountryAndMapReady: {
      immediate: false,
      handler(selectedCountry, old) {
        if (old && !selectedCountry && this.currentZoom >= 4) {
          this.centerOn([0, 0], 2)
        }
      },
    },
  },
  mounted() {
    this.$root.$on('map:center-on', this.centerOn)
    this.$root.$on('map:fit-on', this.fitOn)
    this.$root.$on('map:zoom-at', this.zoomAt)
    this.$root.$on('map:reset-zoom', this.resetZoom)
    this.iconsGenerator()
  },
  beforeDestroy() {
    this.$root.$off([
      'map:center-on',
      'map:fit-on',
      'map:zoom-at',
      'map:reset-zoom',
    ])
  },
  methods: {
    ...mapActions({
      setCurrentZoom: 'landing/setCurrentZoom',
      setMapReady: 'landing/setMapReady',
      setSelectedCountry: 'landing/setSelectedCountry',
      setActiveCountry: 'landing/setActiveCountry',
      setActiveTab: 'landing/setProjectBoxActiveTab',
      setActiveSubLevel: 'landing/setActiveSubLevel',
    }),
    centerOn(latlng, zoom = 13) {
      if (this.$refs.mainMap && this.$refs.mainMap.mapObject) {
        this.$refs.mainMap.mapObject.flyTo(latlng, zoom)
      }
    },
    fitOn(bounds) {
      if (this.$refs.mainMap && this.$refs.mainMap.mapObject) {
        this.$refs.mainMap.mapObject.fitBounds(bounds)
      }
    },
    zoomAt(zoom) {
      if (this.$refs.mainMap && this.$refs.mainMap.mapObject) {
        this.$refs.mainMap.mapObject.setZoom(zoom)
      }
    },
    resetZoom() {
      // removing active and selected country will reset the zoom
      this.setActiveCountry(null)
      if (!this.selectedCountry) {
        this.centerOn([0, 0], 2)
      }
    },
    zoomChangeHandler(event) {
      this.setCurrentZoom(event.target.getZoom())
    },
    pinOptionsAndIconGenerator(id, isActive = false) {
      const projects = this.getCountryProjects(id).length
      const markerClasses = ['CountryCenterIcon']
      if (isActive) {
        markerClasses.push('ActiveCountry')
      }
      if (projects === 0) {
        markerClasses.push('EmptyMarker')
      }
      const html = `<span>${projects}</span>`
      // eslint-disable-next-line
      const icon = L.divIcon({
        className: markerClasses.join(' '),
        html,
        iconSize: [27, 44],
        iconAnchor: [13.5, 44],
      })
      const option = { projects }
      return [icon, option]
    },
    iconsGenerator() {
      const icons = {}
      const options = {}
      if (this.countriesPin.length > 0) {
        this.countriesPin.forEach((cp) => {
          ;[icons[cp.id], options[cp.id]] = this.pinOptionsAndIconGenerator(
            cp.id
          )
        })
      }
      this.countryCenterIcons = icons
      this.countryCenterOptions = options
    },
  },
}

export default MapMixin
