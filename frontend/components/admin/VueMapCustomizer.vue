<template>
  <el-row
    type="flex"
    class="CountryMapCustomizer"
  >
    <el-col>
      <el-row
        type="flex"
        align="middle"
        class="CountryMapHeader"
      >
        <el-col class="CountryMapTitle">
          <div>{{ country.name }}</div>
        </el-col>
        <el-col class="CountryMapFile">
          <el-row
            type="flex"
            align="middle"
          >
            <span><translate>Map file:</translate></span>
            <el-button
              type="text"
              @click="downloadMap"
            >
              <translate>Download</translate>
            </el-button>
            <el-upload
              ref="mapUploadBtn"
              :show-file-list="false"
              :file-list="mapFileList"
              :limit="1"
              :multiple="false"
              :data="{country: country.id}"
              :headers="uploadHeaders"
              :on-success="mapFileChangeSuccessHandler"
              :before-upload="beforeMapUpload"
              class="UploadComp"
              name="map_file"
              action="/api/map-files/"
            >
              <el-button
                :disabled="uploadMapFile"
                :loading="uploadMapFile"
                class="DeleteButton"
                type="text"
              >
                <translate>Change</translate>
              </el-button>
            </el-upload>
          </el-row>
        </el-col>
      </el-row>

      <div class="CountryMapDemo">
        <no-ssr>
          <l-map
            ref="mainMap"
            :zoom="zoom"
            :world-copy-jump="true"
            :options="mapOptions"
            class="MapContainer"
          >
            <l-tilelayer
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
            />

            <l-feature-group @layeradd="geoJsonLoadHandler">
              <l-geo-json
                v-if="firstSubLevelMap && firstSubLevelMap.length > 0"
                ref="geoJsonLayer"
                :geojson="firstSubLevelMap"
              />
            </l-feature-group>

            <l-marker
              v-if="showCenterPin && countryCenter"
              :lat-lng="countryCenter"
              :draggable="true"
              @moveend="countryCenterMoveHandler"
            >
              <l-tooltip> Country Central Pin </l-tooltip>
            </l-marker>

            <l-feature-group v-if="showSubLevelsPins">
              <l-marker
                v-for="pin in subLevelsPolyCenters"
                :key="pin.name"
                :lat-lng="pin.latlng"
                :draggable="true"
                @moveend="subLevelsPinsMoveHandler($event, pin.name)"
              >
                <l-tooltip> {{ pin.name }} </l-tooltip>
              </l-marker>
            </l-feature-group>
          </l-map>
        </no-ssr>
      </div>

      <div class="CountryMapSettings">
        <el-row
          type="flex"
          align="middle"
        >
          <el-col>
            <div class="PinSwitch CountryCenter">
              <span><translate>Country center pin</translate></span>
              <el-switch
                v-model="showCenterPin"
                :active-text="$gettext('Show') | translate"
                :inactive-text="$gettext('Hide') | translate"
              />
            </div>
            <div class="PinSwitch DistrictsCenter">
              <span><translate>Districts center pin</translate></span>
              <el-switch
                v-model="showSubLevelsPins"
                :active-text="$gettext('Show') | translate"
                :inactive-text="$gettext('Hide') | translate"
              />
            </div>
          </el-col>
          <el-col>
            <el-button
              type="text"
              class="IconLeft"
              @click.prevent="polycenterCalculation"
            >
              <fa icon="sync-alt" /> <translate>Set / Reset Markers</translate>
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-col>

    <el-col>
      <div class="MapSettingSection">
        <h5>Sub Level I <span>(Displayed on the map)</span></h5>
        <div>
          <el-select
            v-model="firstSubLevel"
            placeholder="Admin level"
          >
            <el-option
              v-for="level in subLevels"
              :key="level"
              :label="`admin-level-${level}`"
              :value="level"
            />
          </el-select>
          <el-select
            v-model="firstSubLevelType"
            placeholder="Sub level name"
          >
            <el-option
              v-for="name in firstSubLevelTypes"
              :key="name.name"
              :label="name.displayName"
              :value="name.name"
            />
          </el-select>
        </div>

        <div
          v-show="showFirstSubLevelList"
          class="SubLevelList"
        >
          <h5>List of {{ firstSubLevelType }}</h5>
          <ul>
            <li
              v-for="item in firstSubLevelList"
              :key="item.id"
            >
              <fa icon="map-pin" />
              {{ item.name }}
            </li>
          </ul>
        </div>
      </div>

      <div
        v-show="showFirstSubLevelList"
        class="MapSettingSection"
      >
        <h5>Sub Level II <span>(Only for selection)</span></h5>
        <p>Hover on a district name to highlight it on the country map.</p>
        <div>
          <el-select
            v-model="secondSubLevel"
            placeholder="Admin Level"
            clearable
          >
            <el-option
              v-for="level in availableSubLevels"
              :key="level"
              :label="`admin-level-${level}`"
              :value="level"
            />
          </el-select>
          <el-select
            v-model="secondSubLevelType"
            placeholder="Sub level name"
            clearable
          >
            <el-option
              v-for="name in secondSubLevelTypes"
              :key="name.name"
              :label="name.displayName"
              :value="name.name"
            />
          </el-select>
        </div>

        <div
          v-show="showSecondSubLevelList"
          class="SubLevelList"
        >
          <h5> List of {{ secondSubLevelType }}</h5>
          <ul>
            <li
              v-for="item in secondSubLevelList"
              :key="item.id"
            >
              {{ item.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="MapSettingSection">
        <h5>Facility Import</h5>
        <facility-import
          v-show="showFirstSubLevelList"
          ref="facilityImporter"
          :places="places"
        />
        <p v-show="!showFirstSubLevelList">
          Select at least one level to use the facility import
        </p>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { calculatePolyCenter } from '../../utilities/coords';
import { blobDownloader } from '../../utilities/dom';

import FacilityImport from './FacilityImport';
import NoSSR from 'vue-no-ssr';

export default {
  name: 'VueMapCustomizer',
  components: {
    'no-ssr': NoSSR,
    FacilityImport
  },
  data () {
    return {
      zoom: 3,
      mapOptions: { zoomControl: false, attributionControl: false },
      showCenterPin: true,
      showSubLevelsPins: true,
      forceMapFileChange: false,
      mapFile: {},
      uploadMapFile: false,
      mapFileList: []
    };
  },
  computed: {
    ...mapGetters({
      token: 'user/getToken',
      country: 'admin/country/getData',
      subLevelTypes: 'system/getSubLevelTypes',
      firstSubLevelList: 'admin/map/getFirstSubLevelList',
      secondSubLevelList: 'admin/map/getSecondSubLevelList',
      subLevels: 'admin/map/getSubLevels',
      firstSubLevelMap: 'admin/map/getFirstSubLevelMap',
      getFirstSubLevel: 'admin/map/getFirstSubLevel',
      getFirstSubLevelType: 'admin/map/getFirstSubLevelType',
      getSecondSubLevel: 'admin/map/getSecondSubLevel',
      getSecondSubLevelType: 'admin/map/getSecondSubLevelType',
      countryCenter: 'admin/map/getCountryCenter',
      countryBorder: 'admin/map/getCountryBorder',
      subLevelsPolyCenters: 'admin/map/getSubLevelsPolyCenters'
    }),
    uploadHeaders () {
      return {
        'Authorization': `Token ${this.token}`
      };
    },
    firstSubLevelTypes () {
      return this.subLevelTypes.filter(n => n.name !== this.secondSubLevelType);
    },
    secondSubLevelTypes  () {
      return this.subLevelTypes.filter(n => n.name !== this.firstSubLevelType);
    },
    firstSubLevel: {
      get () {
        return this.getFirstSubLevel;
      },
      set (value) {
        this.setFirstSubLevel(value);
      }
    },
    firstSubLevelType: {
      get () {
        return this.getFirstSubLevelType;
      },
      set (value) {
        this.setFirstSubLevelType(value);
      }
    },
    secondSubLevel: {
      get () {
        return this.getSecondSubLevel;
      },
      set (value) {
        this.setSecondSubLevel(value);
      }
    },
    secondSubLevelType: {
      get () {
        return this.getSecondSubLevelType;
      },
      set (value) {
        this.setSecondSubLevelType(value);
      }
    },
    availableSubLevels () {
      return this.subLevels.filter(sb => sb !== this.firstSubLevel);
    },
    showFirstSubLevelList () {
      return (this.firstSubLevel && this.firstSubLevelType);
    },
    showSecondSubLevelList () {
      return (this.secondSubLevel && this.secondSubLevelType);
    },
    places () {
      return this.secondSubLevel
        ? this.secondSubLevelList
        : this.firstSubLevel ? this.firstSubLevelList : [];
    },
    showSaveButton () {
      return this.showFirstSubLevelList;
    }
  },
  methods: {
    ...mapActions({
      loadGeoJSON: 'admin/map/loadGeoJSON',
      setCountryDataField: 'admin/country/setDataField',
      setFirstSubLevel: 'admin/map/setFirstSubLevel',
      setFirstSubLevelType: 'admin/map/setFirstSubLevelType',
      setSecondSubLevel: 'admin/map/setSecondSubLevel',
      setSecondSubLevelType: 'admin/map/setSecondSubLevelType',
      setCountryCenter: 'admin/map/setCountryCenter',
      setSubLevelsPolyCenters: 'admin/map/setSubLevelsPolyCenters',
      updateSubLevelPolyCenter: 'admin/map/updateSubLevelPolyCenter'
    }),

    async downloadMap () {
      // /api/countries/map-download/${country.id}/
      this.$nuxt.$loading.start();
      try {
        const { data } = await this.$axios.get(`/api/countries/map-download/${this.country.id}/`, { responseType: 'blob' });
        blobDownloader(data, `${this.country.name}_boundaries.zip`, this.$nuxt.$loading.finish);
      } catch (e) {
        this.$message.error(this.$gettext('Map donwload failed, please try again later'));
      }
      this.$nuxt.$loading.finish();
    },

    geoJsonLoadHandler () {
      this.$refs.mainMap.mapObject.fitBounds(this.$refs.geoJsonLayer.mapObject.getBounds());
    },

    countryCenterMoveHandler (event) {
      const newLatLng = event.target.getLatLng();
      this.setCountryCenter(newLatLng);
    },

    polycenterCalculation () {
      const countryCenter = calculatePolyCenter(this.countryBorder.geometry);
      this.setCountryCenter(countryCenter);
      const subLevelsPolycenter = this.firstSubLevelMap.map(sb => {
        return {
          name: sb.properties.name,
          latlng: calculatePolyCenter(sb.geometry)
        };
      }).filter(p => p.latlng);
      this.setSubLevelsPolyCenters(subLevelsPolycenter);
    },

    subLevelsPinsMoveHandler (event, name) {
      const latlng = event.target.getLatLng();
      this.updateSubLevelPolyCenter({ name, latlng });
    },

    beforeMapUpload () {
      this.uploadMapFile = true;
    },

    mapFileChangeSuccessHandler (response) {
      this.setCountryDataField({ field: 'map_files', data: [response] });
      setTimeout(async () => {
        await this.loadGeoJSON();
        this.forceMapFileChange = false;
        this.uploadMapFile = false;
        this.mapFileList = [];
      });
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .CountryMapCustomizer {
    align-items: stretch;
    width: 100%;

    > .el-col {
      // Left side - Vue map
      &:first-child {
        width: 100%;
        min-width: calc(100% - 340px);
      }

      // Right side - Levels & Facilities
      &:last-child {
        min-width: 340px;
        max-width: 340px;
        // MapContainer + CountryMapHeader + CountryMapSettings
        height: calc(50vh + 58px + 90px);
        min-height: calc(50vh + 58px + 90px);
        max-height: calc(500px + 58px + 90px);
        overflow-y: auto;
        padding: 0;
        border-left: 1px solid @colorGrayLight;
        background-color: @colorBrandBlueLight;

        .MapSettingSection {
          padding: 20px 40px;
          border-bottom: 1px solid @colorGrayLight;

          &:last-child {
            padding-bottom: 80px;
            border: 0;
          }

          h5 {
            margin: 10px 0 20px;
            font-size: @fontSizeBase;

            span {
              font-weight: 400;
              color: @colorGray;
            }
          }

          p {
            margin: 0 0 20px;
            font-size: @fontSizeSmall;
            line-height: 18px;
            color: @colorGray;
          }

          .el-select {
            width: 100%;
            margin-bottom: 20px;
          }

          .SubLevelList {
            ul {
              list-style-type: none;
              margin: 0;
              padding: 0;

              li {
                position: relative;
                font-size: @fontSizeBase;
                margin: 0 0 10px;
                padding: 0 20px;
                color: @colorBrandPrimary;
                cursor: pointer;
                transition: @transitionAll;

                &:hover {
                  color: @colorBrandPrimaryLight;
                }

                .svg-inline--fa {
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 14px;
                }
              }
            }
          }
        }
      }

      .CountryMapHeader {
        height: 58px;
        padding: 0 40px;
        background-color: @colorWhite;

        .CountryMapTitle {
          width: 100%;
          padding-right: 20px;
          font-size: @fontSizeMedium;
          font-weight: 700;
          .textTruncate();
        }

        .CountryMapFile {
          width: auto;
          font-size: @fontSizeBase;
          text-align: right;
          white-space: nowrap;

          .el-button {
            margin-left: 20px;
            padding: 0;
          }

          // .UploadComp {}
        }
      }

      .CountryMapSettings {
        height: 90px;
        padding: 0 40px;
        background-color: @colorWhite;

        > .el-row {
          height: 100%;
        }

        .PinSwitch {
          padding: 2px 0 6px;

          > span {
            position: relative;
            top: 4px;
            display: inline-block;
            width: 160px;
            font-size: @fontSizeBase;
            font-weight: 700;
            line-height: 16px;
            .textTruncate();
          }

          .el-switch {
            .el-switch__label {
              color: @colorGray;

              &.is-active {
                color: @colorTextPrimary;
              }
            }
          }

          &.CountryCenter {
            .el-switch {
              &.is-checked {
                .el-switch__core {
                  border-color: @colorBrandAccent;
                  background-color: @colorBrandAccent;
                }
              }
            }
          }
        }

        .el-button {
          float: right;
        }
      }

      .MapContainer {
        box-sizing: border-box;
        height: 50vh;
        min-height: 50vh;
        max-height: 500px;
        border: 1px solid @colorGrayLight;
        border-width: 1px 0;
      }

      // vue map custom styling
      .map-container {
        height: 15vh;
        max-height: 500px;

        .country {
          fill: #e3e5ee;
        }

        .first-sub-level {
          fill: #e3e5ee;
          stroke: #9b9da8;
          stroke-width: 2px;
        }

        .second-sub-level {
          fill: #e3e5ee;
          stroke: #283593;
          stroke-width: 1px;
        }

        .label {
          &.hidden {
            display: none;
          }
        }
      }
    }
  }

  [dir="rtl"] {
    .CountryMapCustomizer {
      > .el-col {

        &:last-child {
          border-left: none;
          border-right: 1px solid @colorGrayLight;

          .MapSettingSection {

            .SubLevelList {
              ul {
                li {
                  .svg-inline--fa {
                    left: auto;
                    right: 0;
                  }
                }
              }
            }
          }
        }

        .CountryMapHeader {
          .CountryMapTitle {
            padding-left: 20px;
            padding-right: 0;
          }

          .CountryMapFile {
            .el-button {
              margin-left: 0px;
              margin-right: 20px;
            }
          }
        }

        .CountryMapSettings {
          .el-button {
            float: left;
          }

          .el-switch__label.el-switch__label--left {
            margin-left: 10px;
            margin-right: 0;
          }

          .el-switch__label.el-switch__label--right {
            margin-left: 0;
            margin-right: 10px;
          }
        }
      }
    }
  }
</style>
