<template>
  <div v-scroll-class:TopBarMin="180" class="TopBar">
    <el-row
      type="flex"
      justify="space-between"
      :class="{ TopBarInner: true, IsAuth: auth }"
    >
      <el-col class="LogoHolder">
        <nuxt-link
          :to="localePath({ name: 'organisation', params: $route.params })"
        >
          <el-row type="flex" align="middle">
            <!-- <el-col class="LogoWHO">
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
            </el-col> -->
            <el-col class="LogoUnicef">
              <img
                class="UnicefLogoNormal"
                src="/unicef-logo-banner.svg"
                alt="Unicef"
              />
              <img
                class="UnicefLogoLong"
                src="/unicef-logo-horizontal.svg"
                alt="Unicef"
              />
            </el-col>
          </el-row>
        </nuxt-link>
      </el-col>

      <el-col v-if="!errorPage" class="RightPart">
        <!-- ANON MODE -->
        <el-row
          :class="{ AnonView: !user, LoggedInView: user }"
          type="flex"
          justify="end"
          align="middle"
        >
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
                  :to="
                    localePath({
                      name: 'organisation-inventory',
                      params: $route.params,
                      query: {}
                    })
                  "
                  class="HeaderBtn"
                >
                  <translate>TIIP Inventory</translate>
                </nuxt-link>
              </div>
              <!-- organisation-dashboard-list -->
              <div>
                <nuxt-link
                  key="portfolioBtn"
                  :to="
                    localePath({
                      name: 'organisation-portfolio-innovation',
                      params: $route.params,
                      query: {}
                    })
                  "
                  class="HeaderBtn"
                >
                  <translate>Innovation Portfolio</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="myProjectsBtn"
                  :to="
                    localePath({
                      name: 'organisation-projects',
                      params: $route.params
                    })
                  "
                  exact
                  class="HeaderBtn"
                >
                  <translate>My Projects</translate>
                </nuxt-link>
              </div>
              <div>
                <nuxt-link
                  key="managerBtn"
                  :to="
                    localePath({
                      name: 'organisation-portfolio-management',
                      params: $route.params,
                      query: {}
                    })
                  "
                  class="HeaderBtn"
                >
                  <translate>Portfolio Manager</translate>
                </nuxt-link>
              </div>
              <!-- <div>
                <nuxt-link
                  v-if="isSuperUser"
                  key="planningAndGuidanceBtn"
                  :to="localePath({name: 'organisation-cms', params: $route.params})"
                  class="HeaderBtn"
                >
                  <translate>Planning and Guidance</translate>
                </nuxt-link>
              </div> -->
              <!-- <div>
                <toolkit-dialog-wrapper v-if="isSuperUser" />
              </div> -->
              <div>
                <nuxt-link
                  key="newProjectBtn"
                  :to="
                    localePath({
                      name: 'organisation-projects-create',
                      params: $route.params
                    })
                  "
                  class="HeaderBtn"
                >
                  <fa icon="plus-circle" size="lg" />
                  <translate>New Project</translate>
                </nuxt-link>
              </div>
              <user-dropdown />
            </el-col>
          </template>

          <el-col v-if="countrySpecific" class="CountryHolder">
            <el-row type="flex">
              <el-col>
                <div class="Separator" />
              </el-col>
              <el-col>
                <img
                  :src="countryFlag"
                  alt="country flag"
                  class="CountryFlag"
                />
              </el-col>
              <el-col>
                <div class="CountryName">
                  {{ landingData.code }}
                </div>
              </el-col>
            </el-row>
          </el-col>

          <el-col v-if="customOrganisation" class="CountrySpecificMenu">
            <div class="Separator" />
            <div>
              <nuxt-link
                key="whoLandingBtn"
                :to="
                  localePath({
                    name: 'organisation',
                    params: { organisation: '-' }
                  })
                "
              >
                <img
                  class="LogoWHOxDHA"
                  alt="WHO logo small"
                  src="/logo-whoxdha.svg"
                />
              </nuxt-link>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import VueScrollClass from "vue-scroll-class";
import { mapGetters } from "vuex";

import LanguageSelector from "./LanguageSelector";
import UserDropdown from "./UserDropdown";
import ToolkitDialogWrapper from "./ToolkitDialogWrapper";

export default {
  directives: {
    "scroll-class": VueScrollClass
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
    },
    auth: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      user: "user/getProfile",
      landingData: "landing/getLandingPageData"
    }),
    customOrganisation() {
      return this.landingData !== null;
    },
    countrySpecific() {
      return this.customOrganisation && this.landingData.code.length === 2;
    },
    organisationLogo() {
      if (this.landingData) {
        return this.landingData.logo_url;
      }
      return null;
    },
    countryFlag() {
      if (this.landingData) {
        return `/static/flags/${this.landingData.code.toLowerCase()}.png`;
      }
      return null;
    },
    isSuperUser() {
      return this.user && this.user.is_superuser;
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
    background-color: @colorWhite;
    align-items: stretch;

    &.IsAuth {
      height: @topBarHeight !important;
    }
  }

  .LogoHolder {
    display: flex;
    align-self: flex-start;
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

    .LogoUnicef {
      width: 100%;

      img.UnicefLogoNormal {
        padding-bottom: 10px;
      }
      img.UnicefLogoLong {
        display: none;
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
    padding: 14px 0;

    > .el-row > .el-col {
      width: auto;
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
    font-weight: 100;
    line-height: 24px;
    color: @colorTextPrimary;
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

  .HeaderBtn.md-button {
    transform: translateY(-1px);
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
