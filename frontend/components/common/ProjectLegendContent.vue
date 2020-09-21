<template>
  <div class="ProjectLegendContent">
    <template v-if="showStar">
      <span>
        <el-tooltip :content="member" placement="top">
          <fa icon="star" class="OwnerIcon" />
        </el-tooltip>
        <span v-show="showLabel">
          <translate>Team Member</translate>
        </span>
      </span>
    </template>
    <template v-if="showEye">
      <span>
        <fa icon="eye" class="ViewerIcon" />
        <span v-show="showLabel">
          <translate>Viewer</translate>
        </span>
      </span>
    </template>
    <template v-if="showHandshake">
      <span>
        <fa icon="handshake" class="DonorIcon" />
        <span v-show="showLabel">
          <translate>Investor</translate>
        </span>
      </span>
    </template>
    <template v-if="showGlobe">
      <span>
        <fa icon="globe-africa" class="CountryAdminIcon" />
        <span v-show="showLabel">
          <translate>Country admin</translate>
        </span>
      </span>
    </template>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    id: {
      type: Number,
      default: null
    },
    donors: {
      type: Array,
      default: () => []
    },
    country: {
      type: Number,
      default: null
    },
    forceStar: {
      type: Boolean,
      default: false
    },
    forceEye: {
      type: Boolean,
      default: false
    },
    forceHandshake: {
      type: Boolean,
      default: false
    },
    forceGlobe: {
      type: Boolean,
      default: false
    },
    showLabel: {
      type: Boolean,
      default: false
    },
    compactMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      member: this.$gettext("Team member")
    };
  },

  computed: {
    ...mapGetters({
      userProfile: "user/getProfile"
    }),
    isMember() {
      if (this.id && this.userProfile) {
        return this.userProfile.member.includes(this.id);
      }
      return false;
    },
    isViewer() {
      if (this.id && this.userProfile) {
        return this.userProfile.viewer.includes(this.id);
      }
      return false;
    },
    isTeam() {
      return this.isMember || this.isViewer;
    },
    isDonor() {
      const donorPersonas = ["D", "DA", "SDA"];
      if (this.donors && Array.isArray(this.donors) && this.userProfile) {
        return (
          donorPersonas.includes(this.userProfile.account_type) &&
          this.donors.includes(this.userProfile.donor)
        );
      }
      return false;
    },
    isCountry() {
      const countryPersonas = ["G", "CA", "SCA"];
      if (this.country && this.userProfile) {
        return (
          countryPersonas.includes(this.userProfile.account_type) &&
          this.country === this.userProfile.country
        );
      }
      return false;
    },
    showStar() {
      return this.forceStar || this.isMember;
    },
    showEye() {
      return this.forceEye || (!this.isMember && this.isViewer);
    },
    showHandshake() {
      return this.forceHandshake || (this.isDonor && !this.isTeam);
    },
    showGlobe() {
      return this.forceGlobe || (this.isCountry && !this.isTeam);
    }
  }
};
</script>

<style lang="less">
@import "../../assets/style/variables.less";
@import "../../assets/style/mixins.less";

.ProjectLegendContent {
  svg {
    font-size: 13px !important;
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
