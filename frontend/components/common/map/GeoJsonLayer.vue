<template>
  <div class="GeoJsonLayer">
    <l-feature-group
      ref="geoJsonGroup"
      @layeradd="layerAddHandler"
      @click="clickHandler"
    >
      <l-geo-json
        v-if="geoJson"
        ref="geoJson"
        :options="geoJsonOptions"
        :geojson="geoJson"
      />
    </l-feature-group>
  </div>
</template>

<script>
// eslint-disable-next-line
import * as topojson from 'topojson'

export default {
  props: {
    country: {
      type: Number,
      default: null,
    },
    collection: {
      type: Object,
      required: true,
    },
    activeSubLevel: {
      type: String,
      default: null,
    },
    nationalLevelCoverage: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      id: null,
      geoJsonLoaded: false,
      defaultlSubLevelStyle: {
        fillColor: '#FBC02D',
        fillOpacity: 0.4,
        color: '#E0AC28',
        opacity: 0.8,
      },
      activelSubLevelStyle: {
        fillColor: '#FBC02D',
        fillOpacity: 0.8,
        color: '#FFFFFF',
        opacity: 1,
      },
      nationalLevelCoverageStyle: {
        fillColor: '#FB7E37',
        fillOpacity: 0.4,
        color: '#E3793B',
        opacity: 0.8,
      },
    }
  },
  computed: {
    geoJsonOptions() {
      return {
        style: this.defaultlSubLevelStyle,
      }
    },
    geoJson() {
      const topo = this.collection[this.id]
      if (topo) {
        const subKey = Object.keys(topo.objects)[0]
        // eslint-disable-next-line
        const geo = topojson.feature(topo, topo.objects[subKey])
        geo.id = this.id
        return geo
      }
      return null
    },
    geoJsonLoadedAndActiveSubLevel() {
      if (this.geoJsonLoaded && this.activeSubLevel) {
        return this.activeSubLevel
      }
      return undefined
    },
    geoJsonLoadedAndNationalLevelCoverage() {
      if (this.geoJsonLoaded) {
        return this.nationalLevelCoverage
      }
      return undefined
    },
  },
  watch: {
    country: {
      immediate: true,
      handler(id) {
        if (this.id) {
          this.id = null
          this.$nextTick(() => {
            this.id = id
          })
        } else {
          this.id = id
        }
      },
    },
    geoJsonLoadedAndActiveSubLevel: {
      immediate: true,
      handler(subLevel) {
        if (subLevel) {
          this.updateGeoJsonStyle(false, subLevel)
        }
      },
    },
    geoJsonLoadedAndNationalLevelCoverage: {
      immediate: true,
      handler(nationalLevelCoverage) {
        if (nationalLevelCoverage !== undefined) {
          this.updateGeoJsonStyle(nationalLevelCoverage, this.activeSubLevel)
        }
      },
    },
  },
  methods: {
    layerAddHandler(event) {
      if (event && event.layer) {
        this.geoJsonLoaded = true
        this.$root.$emit('map:fit-on', event.layer.getBounds())
      }
    },
    clickHandler(event) {
      if (
        !this.nationalLevelCoverage &&
        event &&
        event.layer &&
        event.layer.feature &&
        event.layer.feature.properties
      ) {
        this.$emit('geo-json:click', event.layer.feature.properties.id)
      }
    },
    updateGeoJsonStyle(nationalLevelCoverage, subLevel) {
      this.$nextTick(() => {
        if (this.$refs.geoJson && this.$refs.geoJson.mapObject) {
          this.$refs.geoJson.mapObject.eachLayer((layer) => {
            if (nationalLevelCoverage) {
              layer.setStyle(this.nationalLevelCoverageStyle)
            } else if (subLevel === layer.feature.properties.id) {
              layer.setStyle(this.activelSubLevelStyle)
              layer.bringToFront()
            } else {
              layer.setStyle(this.defaultlSubLevelStyle)
              layer.bringToBack()
            }
          })
        }
      })
    },
  },
}
</script>

<style></style>
