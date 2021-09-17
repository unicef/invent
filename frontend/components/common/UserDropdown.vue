<template>
  <div class="UserDropdown">
    <el-popover
      v-model="shown"
      placement="bottom-end"
      :visible-arrow="false"
      popper-class="CustomPopover UserDropdownPopper"
    >
      <Avatar slot="reference" data-test="user-dropdown" :user="profile" :show-hint="false" />

      <div class="DropdownContent">
        <!-- User info block -->
        <div class="UserInfoSection">
          <div class="Item">
            <Profile :user="profile" />
          </div>
        </div>
        <div class="Divider" />

        <div class="UserInfoSection">
          <div class="Item">
            <div class="ItemTitle">
              <translate>Country</translate>
            </div>
            <country-item v-if="user.country" :id="user.country" />
          </div>

          <div class="Item">
            <div class="ItemTitle">
              <translate> Site Language</translate>
            </div>

            <language-select v-model="currentLanguage" size="small" />
          </div>
        </div>

        <!-- User links block -->
        <div class="Divider" />
        <div class="DropdownLink">
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-edit-profile',
                params: $route.params,
              })
            "
            @click.native="closePopover"
          >
            <span class="MenuIcon">
              <fa icon="user-edit" />
            </span>
            <translate>My profile</translate>
          </nuxt-link>
        </div>

        <div v-if="isUserCA" class="DropdownLink">
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-admin-country',
                params: $route.params,
              })
            "
            @click.native="closePopover"
          >
            <span class="MenuIcon">
              <fa icon="globe-africa" />
            </span>
            <translate>Country admin</translate>
          </nuxt-link>
        </div>

        <div v-if="isUserDA" class="DropdownLink">
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-admin-donor',
                params: $route.params,
              })
            "
            @click.native="closePopover"
          >
            <span class="MenuIcon">
              <fa icon="hand-holding-usd" />
            </span>
            <translate>Investor admin</translate>
          </nuxt-link>
        </div>

        <div v-if="isUserDA" class="DropdownLink">
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-admin-import',
                params: $route.params,
              })
            "
            @click.native="closePopover"
          >
            <span class="MenuIcon">
              <fa icon="file-import" />
            </span>
            <translate>Import interface</translate>
          </nuxt-link>
        </div>

        <div class="DropdownLink" @click="logout">
          <el-button type="text" data-test="logout-submit">
            <span class="MenuIcon">
              <fa icon="power-off" />
            </span>
            <translate>Logout</translate>
          </el-button>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Avatar from '@/components/common/Avatar.vue'
import Profile from '@/components/common/Profile.vue'
import LanguageSelect from './LanguageSelect'
import CountryItem from './CountryItem'

export default {
  components: {
    LanguageSelect,
    CountryItem,
    Avatar,
    Profile,
  },
  data() {
    return {
      shown: false,
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
    }),
    isSuperUser() {
      return this.user && this.user.is_superuser
    },
    isUserCA() {
      return (this.user.account_type_approved && ['CA', 'SCA'].includes(this.user.account_type)) || this.isSuperUser
    },
    isUserDA() {
      return (this.user.account_type_approved && ['DA', 'SDA'].includes(this.user.account_type)) || this.isSuperUser
    },
    currentLanguage: {
      get() {
        return this.$i18n.locale
      },
      set(value) {
        // for now on language switch we need a full page change
        const path = this.switchLocalePath(value)
        window.location.href = path
        this.shown = false
      },
    },
    profile() {
      return {
        name: this.user.name,
        email: this.user.email,
        colorScheme: {
          text: '#FFFFFF',
          background: '#CB7918',
          border: 'none',
        },
      }
    },
  },
  methods: {
    ...mapActions({
      doLogout: 'user/doLogout',
    }),
    closePopover() {
      this.shown = false
    },
    logout() {
      this.closePopover()
      this.doLogout()
      this.$router.push(this.localePath({ name: 'auth' }))
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.UserDropdown {
  margin-left: 18px;
}

.UserDropdownPopper {
  transform: translate(10px, -46px);
  border-radius: 5px;
  border: none;
}

.ButtonPopper {
  height: 24px;
  margin: 0 5px 0 5px;
  padding: 0 0 0 10px;
  border: 0;
  font-size: @fontSizeBase;
  font-weight: 100;
  line-height: 24px;
  color: @colorTextPrimary;
  text-decoration: none;

  &:hover {
    color: @colorTextSecondary;
  }

  .svg-inline--fa {
    margin-right: 6px;

    &.fa-caret-down {
      margin: 0 0 0 10px;
    }
  }
}

.UserDropdownPopper {
  padding: 0;
}

.DropdownContent {
  padding: 0 0 10px 0;

  .UserInfoSection {
    padding: 16px 20px 0px;
    font-size: @fontSizeBase;

    .Item {
      margin-bottom: 12px;
      padding-right: 5px;

      .ItemTitle {
        margin-bottom: 6px;
        font-size: @fontSizeSmall - 1;
        font-weight: 700;
        text-transform: uppercase;
        color: @colorGray;
      }

      .CountryName,
      .LanguageName {
        margin-top: 1px;
        margin-left: 8px;
        font-size: @fontSizeBase;
        font-weight: 400;
      }

      .CountryFlag,
      .LanguageFlag {
        img {
          margin-top: 2px;
        }
      }
    }
  }

  .Divider {
    .SeparatorStyleHorizontal();
    // margin: 0 0 10px;
  }

  .DropdownLink {
    display: block;
    min-height: 36px;
    padding: 0 25px 0 20px;
    line-height: 36px;
    cursor: pointer;
    transition: @transitionAll;

    &:hover {
      /* $--color-primary-light-9 */
      background-color: mix(@colorWhite, @colorBrandPrimary, 90%);
    }

    a,
    .el-button {
      color: @colorBrandPrimary !important;
      font-weight: 700;
      text-decoration: none;
      white-space: nowrap;
    }

    a,
    .el-button > span {
      display: flex;
    }

    .el-button {
      width: 100%;
    }

    .MenuIcon {
      display: inline-block;
      width: 32px;
      height: 100%;
      text-align: left;
    }
  }
}
</style>
