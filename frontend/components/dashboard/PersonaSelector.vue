<template>
  <div v-if="user" class="PersonaSelector">
    <el-popover
      v-model="visible"
      placement="bottom-end"
      popper-class="CustomPopover PersonaSelectorPopover"
      trigger="click"
    >
      <el-button slot="reference" type="text" class="IconRight">
        <translate key="view-as"> View as: </translate>
        <div :class="['PersonaBox', personaClass]">
          <fa :icon="personaIcon" class="PersonaIcon" />
          {{ persona }}
        </div>
        <fa icon="caret-down" />
      </el-button>
      <div class="CustomPopoverList">
        <ul>
          <div class="el-popover__title">
            <fa icon="user" />
            <translate>Normal View</translate>
          </div>
          <li :class="{ Active: meActive }" @click="setPersona('user')">
            <fa icon="check" />
            <translate :parameters="{ name: user.name }">
              {name} (me)
            </translate>
          </li>
          <template v-if="showDonor">
            <div class="el-popover__title">
              <fa icon="handshake" />
              <translate>Investor View</translate>
            </div>
            <li :class="{ Active: donorActive }" @click="setPersona('donor')">
              <fa icon="check" />
              {{ donor }}
            </li>
          </template>
          <template v-if="showCountry">
            <div class="el-popover__title">
              <fa icon="globe-africa" />
              <translate>Country View</translate>
            </div>
            <li
              :class="{ Active: countryActive }"
              @click="setPersona('country')"
            >
              <fa icon="check" />
              <translate :parameters="{ country }"> {country} MoH </translate>
            </li>
          </template>
        </ul>
      </div>
    </el-popover>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      visible: false,
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/getProfile',
      getDonorDetails: 'system/getDonorDetails',
      getCountryDetails: 'countries/getCountryDetails',
      dashBoardType: 'dashboard/getDashboardType',
    }),
    meActive() {
      return this.dashBoardType === 'user'
    },
    donorActive() {
      return this.dashBoardType === 'donor'
    },
    countryActive() {
      return this.dashBoardType === 'country'
    },
    persona() {
      const me = this.$gettext('Me')
      return this.meActive ? me : this.countryActive ? this.country : this.donor
    },
    personaClass() {
      return this.meActive ? 'Me' : this.countryActive ? 'Country' : 'Donor'
    },
    personaIcon() {
      return this.meActive
        ? 'user-circle'
        : this.countryActive
        ? 'globe-africa'
        : 'handshake'
    },
    donor() {
      if (this.user && this.user.donor) {
        const donor = this.getDonorDetails(this.user.donor)
        return donor ? donor.name : null
      }
      return null
    },
    country() {
      if (this.user && this.user.country) {
        const country = this.getCountryDetails(this.user.country)
        return country ? country.name : null
      }
      return null
    },
    showDonor() {
      const donorTypes = ['D', 'DA', 'SDA']
      if (this.user) {
        return (
          donorTypes.includes(this.user.account_type) || this.user.is_superuser
        )
      }
      return null
    },
    showCountry() {
      const countryTypes = ['G', 'CA', 'SCA']
      if (this.user) {
        return (
          countryTypes.includes(this.user.account_type) ||
          this.user.is_superuser
        )
      }
      return null
    },
  },
  methods: {
    ...mapActions({
      setDashboardType: 'dashboard/setDashboardType',
    }),
    setPersona(type) {
      const id =
        type === 'user'
          ? null
          : type === 'country'
          ? this.user.country
          : this.user.donor
      this.setDashboardType({ type, id })
      this.visible = false
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.PersonaSelector {
  text-align: right;

  .PersonaBox {
    display: inline;
    line-height: @actionBarHeight;

    .PersonaIcon {
      margin: 0 2px 0 8px;
    }
  }

  .el-button--text {
    padding: 0;
    color: @colorWhite;
  }
}

.PersonaSelectorPopover {
  transform: translate(10px, -35px);
}
</style>
