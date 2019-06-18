<template>
  <div class="PlatformList">
    <ul>
      <li
        v-for="p in selected"
        :key="p.id"
      >
        <simple-field :header="$gettext('Software') | translate">
          <div>
            <span>
              {{ p.name }}
            </span>
            <simple-field :header="$gettext('Digital Health Intervention') | translate">
              <digital-health-interventions-list
                :value="dhi"
                :platform="p.id"
              />
            </simple-field>
          </div>
        </simple-field>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import DigitalHealthInterventionsList from '../common/list/DigitalHealthInterventionsList';
import SimpleField from './SimpleField';

export default {
  components: {
    SimpleField,
    DigitalHealthInterventionsList
  },
  props: {
    dhi: {
      type: Array,
      default: () => []
    },
    platforms: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    ...mapGetters({
      technologyPlatforms: 'projects/getTechnologyPlatforms'
    }),
    selected () {
      return this.technologyPlatforms.filter(tp => this.platforms.includes(tp.id));
    },
    availablePlatforms () {
      return this.technologyPlatforms.filter(tp => !this.platforms.some(s => s === tp.id) || tp.id === this.platform);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .PlatformList {
    width: 100%;
  }
</style>
