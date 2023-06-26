<template>
  <div v-scroll-class:TopBarMin="180" class="TopBar">
    <el-row type="flex" justify="space-between" :class="{ TopBarInner: true, IsAuth: auth }">
      <el-col class="LogoHolder">
        <nuxt-link :to="localePath({ name: 'organisation', params: $route.params })">
          <el-row type="flex" align="middle">
            <el-col class="LogoUnicef">
              <!-- <img class="UnicefLogoNormal" src="/unicef-logo-banner.svg" alt="Unicef" /> -->
              <img class="UnicefLogoLong" src="/unicef-logo-horizontal.svg" alt="Unicef" loading="lazy" />
            </el-col>
          </el-row>
        </nuxt-link>
      </el-col>

      <el-col v-if="!errorPage" class="RightPart">
        <!-- ANON MODE -->
        <el-row :class="{ AnonView: !user, LoggedInView: user }" type="flex" justify="end" align="middle">
          <template v-if="!user">
            <el-col>
              <language-selector />
            </el-col>
          </template>
          <template v-if="user">
            <el-col class="AuthLinks">
              <div>
                <nuxt-link
                  key="inventoryBtn"
                  :to="localePath({ name: 'organisation-inventory-list' })"
                  class="HeaderBtn"
                >
                  <translate>Inventory</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="portfolioBtn"
                  :to="localePath({ name: 'organisation-portfolio-innovation' })"
                  class="HeaderBtn"
                  data-test="menu-portfolio-link"
                >
                  <translate>Innovation Portfolios</translate>
                </nuxt-link>
              </div>
              <div v-if="false">
                <nuxt-link
                  key="managerBtn"
                  :to="localePath({ name: 'organisation-portfolio-management' })"
                  class="HeaderBtn"
                >
                  <translate>Portfolio Manager</translate>
                </nuxt-link>
              </div>
              <div v-if="innovationPerformanceTitle">
                <nuxt-link
                  key="kpiBtn"
                  :to="localePath({ name: 'organisation-innovation-performance' })"
                  class="HeaderBtn"
                >
                  {{ innovationPerformanceTitle }}
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="myInitiativesBtn"
                  :to="localePath({ name: 'organisation-initiatives' })"
                  exact
                  class="HeaderBtn"
                >
                  <translate>My Initiatives</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="newInitiativeBtn"
                  :to="localePath({ name: 'organisation-initiatives-create' })"
                  class="HeaderBtn"
                >
                  <fa icon="plus-circle" size="lg" />
                  <translate>New initiative</translate>
                </nuxt-link>
              </div>
              <div>
                <a key="documentationBtn" :href="docUrl" class="HeaderBtn" target="_blank">
                  <translate>Documentation</translate>
                </a>
              </div>
              <UserDropdown />
            </el-col>
          </template>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import VueScrollClass from 'vue-scroll-class'
import { mapGetters } from 'vuex'

import LanguageSelector from './LanguageSelector'
import UserDropdown from './UserDropdown'

export default {
  directives: {
    'scroll-class': VueScrollClass,
  },
  components: {
    LanguageSelector,
    UserDropdown,
  },
  props: {
    errorPage: {
      type: Boolean,
      default: false,
    },
    auth: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      docUrl: this.$gettext('https://uni.cf/invent-help'),
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
      landingData: 'landing/getLandingPageData',
    }),
    customOrganisation() {
      return this.landingData !== null
    },
    countrySpecific() {
      return this.customOrganisation && this.landingData.code.length === 2
    },
    organisationLogo() {
      if (this.landingData) {
        return this.landingData.logo_url
      }
      return null
    },
    isSuperUser() {
      return this.user && this.user.is_superuser
    },
    displayManager() {
      return (
        (this.user && this.user.is_superuser) ||
        (this.user && this.user.global_portfolio_owner) ||
        (this.user && this.user.manager.length > 0)
      )
    },
    innovationPerformanceTitle() {
      const titleTranslation = this.$gettext('innovation_performance_title')
      return titleTranslation === 'innovation_performance_title' || '' ? '' : titleTranslation
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.TopBar {
  .TopBarInner {
    .limitPageWidth();
    background-color: @colorWhite;
    align-items: stretch;
    height: 56px;

    &.IsAuth {
      // height: @topBarHeightSubpage;
    }
  }

  .LogoHolder {
    display: flex;
    align-self: center;
    width: auto;

    .LogoWHO {
      width: 100%;

      img {
        height: 56px;
      }
    }

    .LogoDHA {
      width: 100%;

      img {
        height: 24px;
        transform: translateY(2px);
      }
    }

    .LogoUnicef {
      width: 100%;
      display: flex;
      position: relative;
      top: 2px;

      img.UnicefLogoNormal {
        display: none;
      }
      img.UnicefLogoLong {
      }
    }

    .Separator {
      width: auto;
      height: 36px;
      margin: 0 15px;

      > div {
        .SeparatorStyle();
      }
    }
  }

  .RightPart {
    padding: 9px 0;

    > .el-row > .el-col {
      width: auto;
      height: 34px;
      line-height: 34px;
    }
  }

  .HideOnActive {
    &.nuxt-link-active {
      display: none;
    }
  }

  .HeaderBtn.nuxt-link-active {
    color: @colorTextPrimary !important;
    font-weight: 700;
  }

  .HeaderBtn {
    position: relative;
    height: 24px;
    margin: 0 5px;
    padding: 0 10px;
    font-size: @fontSizeBase;
    font-weight: 100;
    line-height: 24px;
    color: @colorTextPrimary;
    text-decoration: none;
    transition: @transitionAll;

    &::before {
      content: '';
      position: absolute;
      top: -17px;
      left: 0;
      display: inline-block;
      width: 100%;
      height: 4px;
      background-color: @colorWhite;
      transform: translateY(-4px);
      transition: @transitionAll;
    }

    &:hover {
      color: @colorTextSecondary;

      &::before {
        background-color: @colorGray;
        transform: translateY(0);
      }
    }

    &.nuxt-link-active {
      color: @colorBrandPrimary;

      &::before {
        background-color: @colorBrandPrimary;
        transform: translateY(0);
      }
    }

    .svg-inline--fa {
      margin-right: 6px;
    }
  }

  .Separator {
    .SeparatorStyle();
    display: inline-block;
    margin: 0 20px;
  }

  .AuthLinks,
  .CountrySpecificMenu {
    .clearfix();

    > div {
      float: left;
      height: 24px;
    }
  }

  .CountrySpecificMenu {
    .LogoWHOxDHA {
      height: 24px;
    }
  }
}
</style>
