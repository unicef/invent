<template>
  <div v-click-outside="hide" class="SearchComponent">
    <transition name="el-zoom-in-top">
      <div v-show="shown" class="SearchPopper">
        <el-card :body-style="{ padding: '0px' }">
          <el-row type="flex" class="SearchBig">
            <el-col :span="24">
              <el-input
                ref="searchcontrol"
                v-model="localSearchString"
                :placeholder="$gettext('Type something') | translate"
                @keyup.enter.native="search"
              >
                <fa slot="prepend" icon="search" />
                <template slot="append">
                  <transition name="el-fade-in">
                    <div v-if="localSearchString" class="flex">
                      <el-button class="SearchClear" @click="clearSearch">
                        <fa icon="times" />
                      </el-button>
                      <el-button class="SearchSubmit" @click="search">
                        <fa icon="arrow-right" />
                      </el-button>
                    </div>
                  </transition>
                </template>
              </el-input>
            </el-col>
          </el-row>

          <div class="SearchResultsWrapper">
            <div class="SearchResultsHeader">
              <transition name="el-zoom-in-center">
                <translate v-show="hasResults" class="SearchResultsCounter" :parameters="{ num: results.length }">
                  {num} result(s)
                </translate>
              </transition>
              <LinkAction :url="inventoryUrl" chevron="right">
                <translate>Advanced search</translate>
              </LinkAction>
            </div>

            <el-row v-show="!hasResults">
              <el-col class="SearchResultsNope">
                <p class="TipText">
                  <fa icon="info-circle" size="lg" />
                  <span>
                    <translate>
                      You can use filters to further refine your search. Note that these filters can be saved by
                      selecting Filters and naming your filter. These can then be viewed at a later time after you log
                      in.
                    </translate>
                  </span>
                </p>
              </el-col>
            </el-row>
            <div class="SearchResults">
              <ResultCard
                v-for="project in results"
                v-show="hasResults"
                :key="project.id"
                :project="project"
                :found-in="getFoundIn(project.id)"
                class="SearchResultItem"
              />
            </div>
          </div>
        </el-card>
      </div>
    </transition>

    <transition name="el-zoom-in-top">
      <el-button v-show="!shown && !searchString" class="SearchButton" @click="show">
        <fa icon="search" />
        <translate key="st">Quick search</translate>
      </el-button>
    </transition>

    <div v-show="searchString && !shown" class="SearchShadow" @click="show">
      <el-row type="flex" align="middle">
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
            <translate :parameters="{ num: results.length }"> {num} result(s) </translate>
          </span>
        </el-col>
        <el-col>
          <el-button @click.prevent.stop="clearSearch">
            <fa icon="times" />
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import ClickOutside from 'vue-click-outside'
import { mapGetters, mapActions } from 'vuex'
import LinkAction from '@/components/common/LinkAction.vue'
import ResultCard from '@/components/landing/parts/ResultCard.vue'
import { mapGettersActions } from '../../utilities/form.js'

export default {
  directives: {
    ClickOutside,
  },
  components: {
    LinkAction,
    ResultCard,
  },
  data() {
    return {
      localSearchString: '',
      shown: false,
    }
  },
  computed: {
    ...mapGetters({
      searchParameters: 'landing/getSearchParameters',
      results: 'landing/getSearchResult',
      getFoundIn: 'landing/getFoundIn',
    }),
    ...mapGettersActions({
      searchString: ['landing', 'getSearchString', 'setSearchString', 0],
    }),
    inventoryUrl() {
      return this.localePath({
        name: 'organisation-inventory',
        params: this.$route.params,
      })
    },
    hasResults() {
      return this.results.length > 0
    },
  },
  watch: {
    searchParameters: {
      immediate: false,
      handler(params) {
        this.updateSearch()
      },
    },
  },
  methods: {
    ...mapActions({
      doSearch: 'landing/search',
    }),
    async updateSearch() {
      this.$nuxt.$loading.start()
      await this.doSearch()
      this.$nuxt.$loading.finish()
    },
    clearSearch() {
      this.searchString = null
      this.localSearchString = ''
      this.$nextTick(() => {
        this.$refs.searchcontrol.$el.getElementsByTagName('input')[0].focus()
      })
    },
    search() {
      this.searchString = this.localSearchString
    },
    show() {
      this.shown = true
      this.$nextTick(() => {
        this.$refs.searchcontrol.$el.getElementsByTagName('input')[0].focus()
      })
    },
    hide() {
      this.shown = false
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.SearchComponent {
  position: absolute;
  top: 40px;
  right: 100px;
  z-index: 2000;
  .SearchButton {
    background-color: #4fc8f3;
    height: @actionBarHeight;
    padding: 15px 30px;
    margin: 0;
    text-align: center;
    border-radius: 5px;
    span {
      display: flex;
      align-items: center;
      gap: 10px;
      // width: @actionBarHeight;
      color: @colorWhite;
      .svg-inline--fa {
        font-size: 20px;
        color: @colorWhite;
      }
    }
  }
}

.SearchPopper {
  position: absolute;
  right: 0;
  top: 0;
  z-index: 2010;
  width: 520px;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 5px 5px 20px 10px rgba(0, 0, 0, 0.15);

  > .el-card {
    padding: 0;
    border: 0;
    background-color: fade(@colorGrayLightest, 90%);
  }

  .SearchBig {
    height: @actionBarHeight;
    background-color: #ffffff;
    box-shadow: 0 1px 1px 0 #d8d1c9;

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
      background-color: transparent;
      .flex {
        display: flex;
        .el-button {
          width: @actionBarHeight;
          height: @actionBarHeight;
          margin: 0;
          padding: 0;
        }
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
      // background-color: @colorBrandAccent;
      background-color: #4fc8f3;

      .svg-inline--fa {
        font-size: 18px;
        color: @colorWhite;
      }
    }
  }

  .SearchResultsWrapper {
    max-height: calc(@landingMapHeight - 128px);
    overflow-y: auto;

    @media screen and (max-height: 694px) {
      max-height: calc(@landingMapMinHeight - 128px);
    }
  }

  .SearchResultsHeader {
    display: flex;
    align-items: center;
    height: 56px;
    padding: 0 20px;

    .SearchResultsCounter {
      flex: 1;
      font-size: @fontSizeBase;
      font-weight: bold;
      color: #7995a2;
      letter-spacing: 0;
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
      color: #7995a2;

      .svg-inline--fa {
        margin-right: 6px;
        color: #7995a2;
        position: relative;
        top: 3px;
      }
    }
  }
  .SearchResults {
    display: flex;
    flex-direction: column;
    align-items: center;
    .SearchResultItem {
      margin-bottom: 10px;
      &:hover {
        background-color: hsl(0deg 0% 97%);
      }
    }
  }
}

.SearchShadow {
  position: relative;
  width: 520px;
  height: @actionBarHeight;
  background-color: @colorGrayLightest;

  &::after {
    content: '';
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
