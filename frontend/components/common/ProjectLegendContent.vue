<template>
  <div class="ProjectLegendContent">
    <template v-if="showStar">
      <p>
        <el-tooltip :content="member" placement="top">
          <fa icon="star" class="OwnerIcon" />
        </el-tooltip>
        <span v-show="showLabel">
          <translate>Team Member</translate>
        </span>
      </p>
    </template>
    <template v-if="showEye">
      <p>
        <fa icon="eye" class="ViewerIcon" />
        <span v-show="showLabel">
          <translate>Viewer</translate>
        </span>
      </p>
    </template>
    <template v-if="showGlobe">
      <p>
        <fa icon="globe-africa" class="CountryAdminIcon" />
        <span v-show="showLabel">
          <translate>Country focal point</translate>
        </span>
      </p>
    </template>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    id: {
      type: Number,
      default: null,
    },
    donors: {
      type: Array,
      default: () => [],
    },
    country: {
      type: Number,
      default: null,
    },
    forceStar: {
      type: Boolean,
      default: false,
    },
    forceEye: {
      type: Boolean,
      default: false,
    },
    forceGlobe: {
      type: Boolean,
      default: false,
    },
    showLabel: {
      type: Boolean,
      default: false,
    },
    compactMode: {
      type: Boolean,
      default: false,
    },
    countryOffice: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      member: this.$gettext('Team member'),
    }
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/getProfile',
    }),
    isMember() {
      if (this.id && this.userProfile) {
        return this.userProfile.member.includes(this.id)
      }
      return false
    },
    isViewer() {
      if (this.id && this.userProfile) {
        return this.userProfile.viewer.includes(this.id)
      }
      return false
    },
    isTeam() {
      return this.isMember || this.isViewer
    },
    isDonor() {
      const donorPersonas = ['D', 'DA', 'SDA']
      if (this.donors && Array.isArray(this.donors) && this.userProfile) {
        return (
          donorPersonas.includes(this.userProfile.account_type) &&
          this.donors.includes(this.userProfile.donor)
        )
      }
      return false
    },
    isCountry() {
      const countryPersonas = ['G', 'CA', 'SCA']
      if (this.country && this.userProfile) {
        return (
          countryPersonas.includes(this.userProfile.account_type) &&
          this.country === this.userProfile.country
        )
      }
      return false
    },
    isFocalPoint(){
      return this.userProfile.manager_of.includes(this.countryOffice)
    },
    showStar() {
      return this.forceStar || (this.isMember && !this.isFocalPoint)
    },
    showEye() {
      return this.forceEye || (!this.isMember && this.isViewer)
    },
    showGlobe() {
      return this.forceGlobe || this.isFocalPoint
    },
  }
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ProjectLegendContent {
  p {
    margin: 0 0 0 0;
    font-size: 12px;
    display: inline;
  }
  svg {
    font-size: 16px;
    min-width: 16px;
  }
  .OwnerIcon {
    color: @colorOwner;
  }
  .ViewerIcon {
    color: @colorViewer;
  }
  .DonorIcon {
    color: @colorDonor;
  }
  .CountryAdminIcon {
    color: @colorCountryAdmin;
  }
}
</style>
