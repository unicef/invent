<template>
  <div>
    <l-marker
      v-if="show"
      ref="countryMarker"
      :icon="icon"
      :options="options"
      :lat-lng="pin.latlng"
      class="MapMarker"
      @click="markerClickHandler"
    >
      <l-popup v-if="!disableTooltip" ref="tooltip" :options="popupOptions">
        <div
          class="MouseEventSpy"
          @mouseenter="mouseEnterHandler"
          @mouseleave="mouseLeaveHandler"
        >
          <el-button
            type="primary"
            class="CountryViewBtn"
            @click="openCountryView"
          >
            <fa icon="search-plus" />
            <span v-show="popUpHover" class="Text">
              <translate>Country view</translate>
            </span>
          </el-button>
        </div>
      </l-popup>
    </l-marker>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  components: {},
  props: {
    pin: {
      type: Object,
      required: true,
    },
    icon: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    options: {
      type: Object,
      default: () => ({}),
    },
    selectedCountry: {
      type: Number,
      default: null,
    },
    activeCountry: {
      type: Number,
      default: null,
    },
    disableTooltip: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      popUpHover: false,
      popupOptions: {
        className: `CountryViewPopup`,
        closeButton: false,
      },
      show: false,
    }
  },
  computed: {
    ...mapGetters({
      getCountryProjects: 'landing/getCountryProjects',
    }),
  },
  mounted() {
    setTimeout(() => {
      this.show = true
    }, 500)
  },
  methods: {
    markerClickHandler() {
      this.$emit('update:activeCountry', this.pin.id)
    },
    safeMapObjectFunctionCall(ref, functionName) {
      if (this.$refs[ref] && this.$refs[ref].mapObject) {
        this.$refs[ref].mapObject[functionName]()
      }
    },
    openCountryView() {
      this.$emit('update:selectedCountry', this.pin.id)
      this.safeMapObjectFunctionCall('countryMarker', 'closePopup')
    },
    mouseEnterHandler(event) {
      this.popUpHover = true
    },
    mouseLeaveHandler(event) {
      this.popUpHover = false
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.CountryViewPopup {
  &.leaflet-popup {
    margin-bottom: 55px;
  }

  .leaflet-popup-content-wrapper {
    background-color: transparent;
    box-shadow: none;

    .leaflet-popup-content {
      width: 36px !important;
      margin: 0;
    }
  }

  .leaflet-popup-tip-container {
    display: none;
  }

  .MouseEventSpy {
    position: relative;
    width: 36px;
    height: 36px;
  }

  .CountryViewBtn {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 36px;
    height: 36px;
    margin: 0;
    padding: 0 12px;
    overflow: hidden;
    border: 0;
    border-radius: 36px;
    background-color: fade(@colorBrandAccent, 90%);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.12), 0 5px 5px rgba(0, 0, 0, 0.24);
    transition: @transitionAll;

    > span {
      display: inline-flex;
      height: 100%;
      align-items: center;
    }

    .svg-inline--fa {
      font-size: 16px;
      margin-left: -1px;
    }

    .Text {
      display: none;
      font-size: 12px;
      line-height: 36px;
      padding-left: 4px;
    }

    &:hover {
      width: auto;
      background-color: @colorBrandAccent;

      .Text {
        display: inline;
      }
    }
  }
}
</style>
