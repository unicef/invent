<template>
  <div
    id="implementation"
    class="ImplementationOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Implementation overview') | translate"
      show-legend
    >
      <custom-required-form-item
        :error="errors.first('health_focus_areas')"
        :draft-rule="draftRules.health_focus_areas"
        :publish-rule="publishRules.health_focus_areas"
      >
        <template slot="label">
          <translate key="health-focus-areas">
            What is the health focus area(s) addressed by the DHI?
          </translate>
        </template>

        <health-focus-areas-selector
          v-model="health_focus_areas"
          v-validate="rules.health_focus_areas"
          data-vv-name="health_focus_areas"
          data-vv-validate-on="change"
          data-vv-as="Health focus areas"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('hsc_challenges')"
        :draft-rule="draftRules.hsc_challenges"
        :publish-rule="publishRules.hsc_challenges"
      >
        <template slot="label">
          <translate key="hsc-challenges">
            What are the Health System Challenges addressed by the Digital Health Intervention?
          </translate>
        </template>
        <health-system-challenges-selector
          v-model="hsc_challenges"
          v-validate="rules.hsc_challenges"
          data-vv-name="hsc_challenges"
          data-vv-validate-on="change"
          data-vv-as="Health system challenges"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('platforms')"
      >
        <template slot="label">
          <translate key="platforms">
            Add information about your Digital Health program activies
          </translate>
          <form-hint>
            <translate key="platforms-hint">
              Include all software that is part of your project. If you cannot find your software listed in the options, send an email to digitalhealthatlas@gmail.com with the software name.
            </translate>
          </form-hint>
        </template>

        <custom-required-form-item
          v-for="(platform, index) in platforms"
          :key="platform"
          :error="errors.first('id', 'platform_' + index)"
          :draft-rule="draftRules.platforms"
          :publish-rule="publishRules.platforms"
          class="ItemIndent"
        >
          <template slot="label">
            <translate key="platform-label">
              What are the names of the software included in the deployment?
            </translate>
          </template>

          <el-col :span="16">
            <platform-selector
              :key="platform"
              v-model="platforms"
              v-validate="rules.platforms"
              :data-vv-scope="'platform_' + index"
              :index="index"
              data-vv-name="id"
              data-vv-as="Software"
            />
            <custom-required-form-item
              v-show="platform"
              :error="errors.first('strategies', 'platform_' + index)"
              :draft-rule="draftRules.strategies"
              :publish-rule="publishRules.strategies"
              class="DigitalHealthIntervention"
            >
              <template slot="label">
                <translate key="strategies">
                  What Digital Health Intervention(s) are included in this software?
                </translate>
                <form-hint>
                  <!-- This is going to be a link to a pdf / webpage -->
                </form-hint>
              </template>
              <digital-health-interventions-selector
                v-validate="rules.strategies"
                :platform-id="platform"
                :data-vv-scope="'platform_' + index"
                data-vv-name="strategies"
                data-vv-as="Digital health interventions"
              />
            </custom-required-form-item>
          </el-col>
          <el-col :span="8">
            <add-rm-buttons
              :show-add="isLastAndExist(platforms, index)"
              :show-rm="platforms.length > 1"
              @add="addDhi"
              @rm="rmDhi(index, platform)"
            />
          </el-col>
        </custom-required-form-item>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('donors')"
        :draft-rule="draftRules.donors"
        :publish-rule="publishRules.donors"
      >
        <template slot="label">
          <translate key="donors">
            Who are your investment partners?
          </translate>
          <form-hint>
            <translate key="donors-hint">
              Investment partners can include those contributing funds, human resources or in-kind support.
            </translate>
          </form-hint>
        </template>

        <donor-selector
          v-model="donors"
          v-validate="rules.donors"
          data-vv-name="donors"
          data-vv-as="Investors"
        />
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js';
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js';

import CollapsibleCard from '../CollapsibleCard';
import HealthSystemChallengesSelector from '../HealthSystemChallengesSelector';
import HealthFocusAreasSelector from '../HealthFocusAreasSelector';
import PlatformSelector from '../PlatformSelector';
import DigitalHealthInterventionsSelector from '../DigitalHealthInterventionsSelector';
import AddRmButtons from '../AddRmButtons';
import DonorSelector from '../DonorSelector';
import FormHint from '../FormHint';

import { mapGettersActions } from '../../../utilities/form';

export default {
  components: {
    CollapsibleCard,
    HealthSystemChallengesSelector,
    HealthFocusAreasSelector,
    PlatformSelector,
    DigitalHealthInterventionsSelector,
    AddRmButtons,
    DonorSelector,
    FormHint
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],

  computed: {
    ...mapGettersActions({
      platforms: ['project', 'getPlatforms', 'setPlatforms', 0],
      digitalHealthInterventions: ['project', 'getDigitalHealthInterventions', 'setDigitalHealthInterventions', 0],
      health_focus_areas: ['project', 'getHealthFocusAreas', 'setHealthFocusAreas', 0],
      hsc_challenges: ['project', 'getHscChallenges', 'setHscChallenges', 0],
      donors: ['project', 'getDonors', 'setDonors', 0]
    })
  },
  methods: {
    isLastAndExist (collection, index) {
      return !!(collection.length - 1 === index && collection[index]);
    },
    addDhi () {
      this.platforms = [...this.platforms, null];
    },
    rmDhi (index, platformId) {
      if (platformId) {
        const filtered = this.digitalHealthInterventions.filter(dhi => dhi.platform !== platformId);
        this.digitalHealthInterventions = filtered;
      }
      this.platforms = this.platforms.filter((p, i) => i !== index);
    },
    async validate () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate(),
        this.coverageType === 2
          ? this.$refs.nationalLevelDeployment.validate()
          : this.$refs.subNationalLevelDeployment.validate()
      ]);
      console.log('Implementation overview validations', validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .ImplementationOverview {
    .DigitalHealthIntervention {
      margin-top: 30px;
    }

    .CoverageArea {
      .CoverageSubtitle {
        position: relative;
        display: block;
        margin: 0 0 20px;
        padding: 10px 0 0 20px;
        font-size: @fontSizeSmall;
        font-weight: 700;
        color: @colorGray;
        text-transform: uppercase;

        .svg-inline--fa {
          position: absolute;
          top: 10px;
          left: 0;
        }
      }
    }
  }
</style>
