<template>
  <div class="ProjectLegend">
    <project-legend-content
      v-if="!compactMode"
      :id="id"
      :donors="donors"
      :country="country"
      :force-star="forceStar"
      :force-eye="forceEye"
      :force-handshake="forceHandshake"
      :force-globe="forceGlobe"
      :show-label="showLabel"
    />
    <el-popover
      v-if="compactMode"
      placement="bottom-end"
      trigger="hover"
      title="Table legend"
      popper-class="CustomPopover TableLegendDropdown"
    >
      <project-legend-content
        :id="id"
        :donors="donors"
        :country="country"
        :force-star="forceStar"
        :force-eye="forceEye"
        :force-handshake="forceHandshake"
        :force-globe="forceGlobe"
        :show-label="showLabel"
      />
      <el-button
        slot="reference"
        type="text"
        size="small"
        class="ShowLegendButton"
      >
        <fa icon="question-circle" />
        <translate>Show legend</translate>
      </el-button>
    </el-popover>
  </div>
</template>

<script>
import ProjectLegendContent from './ProjectLegendContent'

export default {
  components: {
    ProjectLegendContent,
  },
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
    forceHandshake: {
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
  },
  computed: {},
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.ProjectLegend {
  opacity: 1;
  transition: @transitionFade;
  padding-top: 7px;
  width: 67px;
  display: flex;
  justify-content: flex-end;

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
