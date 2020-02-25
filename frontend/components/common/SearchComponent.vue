<template>
  <div
    v-click-outside="hide"
    class="SearchComponent"
  >
    <transition name="el-fade-in">
      <div
        v-show="shown"
        class="SearchPopper"
      >
        <el-card :body-style="{ padding: '0px' }">
          <el-row
            type="flex"
            class="SearchBig"
          >
            <el-col :span="24">
              <el-input
                v-model="localSearchString"
                :placeholder="$gettext('Create your search here') | translate"
                @keyup.enter.native="search"
              >
                <fa
                  slot="prepend"
                  icon="search"
                />
                <template slot="append">
                  <el-button
                    class="SearchClear"
                    @click="clearSearch"
                  >
                    <fa icon="times" />
                  </el-button>
                  <el-button
                    class="SearchSubmit"
                    @click="search"
                  >
                    <fa icon="arrow-right" />
                  </el-button>
                </template>
              </el-input>
            </el-col>
          </el-row>

          <div class="SearchResultsWrapper">
            <el-row
              type="flex"
              align="middle"
              class="SearchResultsHeader"
            >
              <el-col
                v-show="hasResults"
                class="SearchResultsCounter"
              >
                <translate :parameters="{num: results.length}">
                  {num} result(s):
                </translate>
              </el-col>
              <el-col class="AdvancedSearchLink">
                <nuxt-link
                  :to="localePath({name : 'organisation-dashboard-list', params: $route.params})"
                  class="NuxtLink IconRight"
                >
                  <span><translate>Advanced search</translate></span><fa icon="angle-right" />
                </nuxt-link>
              </el-col>
            </el-row>

            <el-row v-show="!hasResults">
              <el-col class="SearchResultsNope">
                <p class="TipText">
                  <fa
                    icon="info-circle"
                    size="lg"
                  />
                  <span>
                    <translate>
                      You can use filters to further refine your search. Note that these filters can be saved by selecting Filters and naming your filter. These can then be viewed at a later time after you log in.
                    </translate>
                  </span>
                </p>
              </el-col>
            </el-row>

            <el-row
              v-for="project in results"
              v-show="hasResults"
              :key="project.id"
              class="SearchResultItem"
            >
              <el-col>
                <project-card
                  :project="project"
                  :found-in="getFoundIn(project.id)"
                  show-found-in
                  show-country
                  show-organisation
                  show-arrow-on-over
                />
              </el-col>
            </el-row>
          </div>
        </el-card>
      </div>
    </transition>

    <el-button
      v-show="!shown && !searchString"
      class="SearchButton"
      @click="show"
    >
      <fa icon="search" />
    </el-button>

    <div
      v-show="searchString && !shown"
      class="SearchShadow"
      @click="show"
    >
      <el-row
        type="flex"
        align="middle"
      >
        <el-col>
          <fa icon="search" />
        </el-col>
        <el-col>
          <span class="SearchText">
            {{ searchString }}
          </span>
        </el-col>
        <el-col>
          <span class="SearchResultsCounter">
            <translate :parameters="{num: results.length}">
              {num} result(s)
            </translate>
          </span>
        </el-col>
        <el-col>
          <el-button
            @click.prevent.stop="clearSearch"
          >
            <fa icon="times" />
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGettersActions } from '../../utilities/form.js';
import ProjectCard from './ProjectCard';
import ClickOutside from 'vue-click-outside';
import { mapGetters, mapActions } from 'vuex';

export default {
  directives: {
    ClickOutside
  },
  components: {
    ProjectCard
  },
  data () {
    return {
      localSearchString: '',
      shown: false
    };
  },
  computed: {
    ...mapGetters({
      searchParameters: 'landing/getSearchParameters',
      results: 'landing/getSearchResult',
      getFoundIn: 'landing/getFoundIn'
    }),
    ...mapGettersActions({
      searchString: ['landing', 'getSearchString', 'setSearchString', 0]
    }),
    hasResults () {
      return this.results.length > 0;
    }
  },
  watch: {
    searchParameters: {
      immediate: false,
      handler (params) {
        this.updateSearch();
      }
    }
  },
  methods: {
    ...mapActions({
      doSearch: 'landing/search'
    }),
    async updateSearch () {
      this.$nuxt.$loading.start();
      await this.doSearch();
      this.$nuxt.$loading.finish();
    },
    clearSearch () {
      this.searchString = null;
    },
    search () {
      this.searchString = this.localSearchString;
    },
    show () {
      this.shown = true;
    },
    hide () {
      this.shown = false;
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .SearchComponent {
    .SearchButton {
      width: @actionBarHeight;
      height: @actionBarHeight;
      padding: 0;
      margin: 0;
      text-align: center;
      color: @colorWhite;

      .svg-inline--fa {
        font-size: 20px;
        color: @colorWhite;
      }
    }
  }

  .SearchPopper {
    position: absolute;
    right: 40px;
    top: 0;
    z-index: 2010;
    width: 400px;
    box-shadow: 5px 5px 20px 10px rgba(0,0,0,.15);

    > .el-card {
      padding: 0;
      border: 0;
      background-color: fade(@colorGrayLightest, 90%);
    }

    .SearchBig {
      height: @actionBarHeight;

      .el-input,
      .el-input__inner {
        width: 100%;
        height: @actionBarHeight;
        font-size: @fontSizeBase;
        font-weight: 700;
      }

      .el-input__inner,
      .el-input-group__prepend,
      .el-input-group__append {
        border: none !important;
      }

      .el-input-group__prepend {
        width: 38px;
        height: @actionBarHeight;
        padding: 0;
        background-color: @colorWhite;

        .svg-inline--fa {
          float: right;
          font-size: 20px;
          color: @colorTextPrimary;
        }
      }

      .el-input-group__append {
        width: @actionBarHeight * 2;
        height: @actionBarHeight;
        padding: 0;

        .el-button {
          width: @actionBarHeight;
          height: @actionBarHeight;
          margin: 0;
          padding: 0;
        }
      }

      .SearchClear {
        background-color: @colorGrayLightest;

        .svg-inline--fa {
          font-size: 18px;
        }

        &:hover {
          background-color: @colorGrayLighter;
          color: @colorTextPrimary;
        }
      }

      .SearchSubmit {
        border: 0;
        background-color: @colorBrandAccent;

        .svg-inline--fa {
          font-size: 18px;
          color: @colorWhite;
        }

        &:hover {
          background-color: @colorBrandAccentLight;
        }
      }
    }

    .SearchResultsWrapper {
      max-height: calc(@landingMapHeight - 36px);
      overflow-y: auto;

      @media screen and (max-height: 694px) {
        max-height: calc(@landingMapMinHeight - 36px);
      }
    }

    .SearchResultsHeader {
      height: 56px;
      padding: 0 20px;
      border-top: 1px solid @colorTextMuted;

      .SearchResultsCounter {
        width: 100%;
        font-size: @fontSizeSmall;
        font-weight: 700;
        color: @colorTextSecondary;
      }

      .AdvancedSearchLink {
        width: auto;
      }
    }

    .SearchResultsNope {
      padding: 0 20px 30px;

      .TipText {
        display: inline-flex;
        align-items: flex-start;
        margin: 0;
        font-size: @fontSizeSmall;
        line-height: 18px;
        color: @colorTextSecondary;

        .svg-inline--fa {
          margin-right: 6px;
          color: @colorTextMuted;
        }
      }
    }

    .SearchResultItem {
      margin: 0 10px 8px;
    }
  }

  .SearchShadow {
    position: relative;
    width: 400px;
    height: @actionBarHeight;
    background-color: @colorGrayLightest;

    &::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: 0;
      display: block;
      width: 100%;
      height: 1px;
      background-color: @colorGrayLight;
    }

    .el-col {
      height: @actionBarHeight;

      // search icon
      &:nth-child(1) {
        min-width: 38px;
        max-width: 38px;
        height: @actionBarHeight;

        .svg-inline--fa {
          float: right;
          height: @actionBarHeight;
          font-size: 20px;
          color: @colorTextPrimary;
        }
      }

      // search term
      &:nth-child(2) {
        width: 100%;

        .SearchText {
          color: @colorTextPrimary;
          font-size: @fontSizeBase;
          font-weight: 700;
          line-height: @actionBarHeight;
          padding: 0 15px;
        }
      }

      // search results
      &:nth-child(3) {
        width: auto;

        .SearchResultsCounter {
          padding: 0 15px;
          color: @colorTextMuted;
          font-size: @fontSizeBase;
          font-weight: 700;
          line-height: @actionBarHeight;
          white-space: nowrap;
        }
      }

      // search clear
      &:nth-child(4) {
        width: @actionBarHeight;

        .el-button {
          width: @actionBarHeight;
          height: @actionBarHeight;
          padding: 0;
          background-color: @colorGrayLightest;
          color: @colorTextMuted;

          .svg-inline--fa {
            font-size: 18px;
          }

          &:hover {
            color: @colorTextPrimary;
            background-color: @colorGrayLighter;
          }
        }
      }
    }
  }
</style>
