<template>
  <div
    v-scroll-class:TopBarMin="180"
    class="TopBar"
  >
    <el-row
      type="flex"
      justify="space-between"
      class="TopBarInner"
    >
      <el-col class="LogoHolder">
        <nuxt-link :to="localePath({name: 'organisation', params: $route.params})">
          <el-row
            type="flex"
            align="middle"
          >
            <el-col class="LogoWHO">
              <img
                :src="customOrganisation ? organisationLogo : '/logo-who-blue.svg'"
                :alt="customOrganisation ? $gettext('Country logo') : $gettext('WHO logo')"
              >
            </el-col>
            <el-col class="Separator">
              <div />
            </el-col>
            <el-col class="LogoDHA">
              <img
                src="/logo-dha.svg"
                alt="Digital Health Atlas"
              >
            </el-col>
          </el-row>
        </nuxt-link>
      </el-col>

      <el-col
        v-if="!errorPage"
        class="RightPart"
      >
        <!-- ANON MODE -->
        <el-row
          :class="{'AnonView': !user, 'LoggedInView': user}"
          type="flex"
          justify="end"
          align="middle"
        >
          <template v-if="!user">
            <el-col>
              <language-selector />
            </el-col>

            <el-col class="AuthLinks">
              <div class="Separator" />
              <div>
                <nuxt-link
                  key="signupBtn"
                  :to="localePath({name: 'organisation-signup', params: $route.params})"
                  class="HeaderBtn HideOnActive"
                >
                  <translate>Signup</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="loginBtn"
                  :to="localePath({name: 'organisation-login', params: $route.params})"
                  class="HeaderBtn HideOnActive"
                >
                  <translate>Login</translate>
                </nuxt-link>
              </div>
            </el-col>
          </template>
          <template v-if="user">
            <el-col class="AuthLinks">
              <!-- <div>
                <nuxt-link
                  key="dashboardBtn"
                  :to="localePath({name: 'organisation-dashboard', params: $route.params, query: {}})"
                  class="HeaderBtn"
                >
                  <translate>Dashboard</translate>
                </nuxt-link>
              </div> -->
              <div>
                <nuxt-link
                  key="myProjectsBtn"
                  :to="localePath({name: 'organisation-projects', params: $route.params})"
                  exact
                  class="HeaderBtn"
                >
                  <translate>My Projects</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="planningAndGuidanceBtn"
                  :to="localePath({name: 'organisation-cms', params: $route.params})"
                  class="HeaderBtn"
                >
                  <translate>Planning and Guidance</translate>
                </nuxt-link>
              </div>
              <div>
                <toolkit-dialog-wrapper />
              </div>
              <div>
                <nuxt-link
                  key="newProjectBtn"
                  :to="localePath({name: 'organisation-projects-create', params: $route.params})"
                  class="HeaderBtn"
                >
                  <fa icon="plus-circle" />
                  <translate>New Project</translate>
                </nuxt-link>
              </div>
              <user-dropdown />
            </el-col>
          </template>

          <el-col
            v-if="countrySpecific"
            class="CountryHolder"
          >
            <el-row type="flex">
              <el-col>
                <div class="Separator" />
              </el-col>
              <el-col>
                <img
                  :src="countryFlag"
                  alt="country flag"
                  class="CountryFlag"
                >
              </el-col>
              <el-col>
                <div class="CountryName">
                  {{ landingData.code }}
                </div>
              </el-col>
            </el-row>
          </el-col>

          <el-col
            v-if="customOrganisation"
            class="CountrySpecificMenu"
          >
            <div class="Separator" />
            <div>
              <nuxt-link
                key="whoLandingBtn"
                :to="localePath({name: 'organisation', params: {organisation: '-'}})"
              >
                <img
                  class="LogoWHOxDHA"
                  alt="WHO logo small"
                  src="/logo-whoxdha.svg"
                >
              </nuxt-link>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import VueScrollClass from 'vue-scroll-class';
import { mapGetters } from 'vuex';

import LanguageSelector from './LanguageSelector';
import UserDropdown from './UserDropdown';
import ToolkitDialogWrapper from './ToolkitDialogWrapper';

export default {
  directives: {
    'scroll-class': VueScrollClass
  },
  components: {
    LanguageSelector,
    UserDropdown,
    ToolkitDialogWrapper
  },
  props: {
    errorPage: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
      landingData: 'landing/getLandingPageData'
    }),
    customOrganisation () {
      return this.landingData !== null;
    },
    countrySpecific () {
      return this.customOrganisation && this.landingData.code.length === 2;
    },
    organisationLogo () {
      if (this.landingData) {
        return this.landingData.logo_url;
      }
      return null;
    },
    countryFlag () {
      if (this.landingData) {
        return `/static/flags/${this.landingData.code.toLowerCase()}.png`;
      }
      return null;
    }

  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .TopBar {
    .TopBarInner {
      .limitPageWidth();
      height: @topBarHeight;
      background-color: @colorWhite;
      align-items: stretch;
    }

    .LogoHolder {
      display: flex;
      align-self: center;
      width: auto;

      .LogoWHO {
        width: 100%;

        img {
          height: 48px;
        }
      }

      .LogoDHA {
        width: 100%;

        img {
          height: 24px;
          transform: translateY(2px);
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
      padding: 15px 0;

      > .el-row > .el-col {
        width: auto;
      }
    }

    .HideOnActive {
      &.nuxt-link-active {
        display: none;
      }
    }

    .HeaderBtn
    // TODO: Remove Angular Material
    // hacking Toolkit md-button :(
    ,.HeaderBtn.md-button
    //
    {
      position: relative;
      height: 24px;
      margin: 0 5px;
      padding: 0 10px;
      font-size: @fontSizeBase;
      font-weight: 700;
      line-height: 24px;
      color: @colorBrandPrimary;
      text-decoration: none;
      transition: @transitionAll;

      // hacking Toolkit md-button :(
      min-height: auto;
      min-width: auto;
      overflow: visible;
      background-color: transparent !important;

      &.md-ink-ripple {
        > span {
          letter-spacing: 0 !important;
        }

        &::before {
          top: -15px !important;
        }
      }

      > .md-ripple-container {
        display: none;
      }
      //

      &::before {
        content: "";
        position: absolute;
        top: -19px;
        left: 0;
        display: inline-block;
        width: 100%;
        height: 4px;
        background-color: @colorWhite;
        transform: translateY(-4px);
        transition: @transitionAll;
      }

      &:hover {
        color: @colorBrandPrimaryLight;

        &::before {
          background-color: @colorBrandPrimaryLight;
          transform: translateY(0);
        }
      }

      &.nuxt-link-active {
        color: @colorBrandAccent;

        &::before {
          background-color: @colorBrandAccent;
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

    .CountryHolder {
      height: 24px;

      .CountryFlag {
        height: 14px;
        margin-right: 6px;
        padding: 5px 0;
      }

      .CountryName {
        font-size: @fontSizeBase;
        font-weight: 700;
        color: @colorTextPrimary;
        line-height: 24px;
      }
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
