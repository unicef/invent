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
        :error="errors.first('his_bucket')"
        :draft-rule="draftRules.his_bucket"
        :publish-rule="publishRules.his_bucket"
      >
        <template slot="label">
          <translate key="his-bucket">
            What health information system(s) in your country does this project support?
          </translate>
        </template>
        <his-bucket-selector
          v-model="his_bucket"
          v-validate="rules.his_bucket"
          data-vv-name="his_bucket"
          data-vv-validate-on="change"
          data-vv-as="Health information system"
        />
      </custom-required-form-item>

      <div class="CoverageArea">
        <custom-required-form-item
          prop="coverageType"
        >
          <template slot="label">
            <translate key="coverage-type">
              What level of coverage does your project have (Sub-national, National)
            </translate>
            <form-hint>
              <translate key="coverage-type-hint">
                Subnational may include district, regional, provincial, county levels.
              </translate>
            </form-hint>
          </template>

          <el-radio-group v-model="coverageType">
            <el-radio :label="1">
              <translate>Sub-national</translate>
            </el-radio>
            <el-radio :label="2">
              <translate>National</translate>
            </el-radio>
          </el-radio-group>
        </custom-required-form-item>

        <sub-national-level-deployment
          v-if="coverageType == 1"
          ref="subNationalLevelDeployment"
          :api-errors="apiErrors"
          :rules="rules"
          :draft-rules="draftRules"
          :publish-rules="publishRules"
        />

        <div
          v-if="coverageType == 2"
          class="NationalLevelDeployment ItemIndent"
        >
          <div class="CoverageSubtitle">
            <fa icon="flag" />
            <translate>National level deployment</translate>
          </div>
          <coverage-fieldset
            ref="nationalLevelDeployment"
            :is-nlc="true"
            :disabled="false"
            :rules="rules.national_level_deployment"
            :api-errors="apiErrors"
            :health-workers.sync="healthWorkers"
            :clients.sync="clients"
            :facilities.sync="facilities"
            :draft-rules="draftRules.national_level_deployment"
            :publish-rules="publishRules.national_level_deployment"
            scope="national_level_deployment"
          />
        </div>
      </div>
      <custom-required-form-item
        :error="errors.first('government_investor')"
        :draft-rule="draftRules.government_investor"
        :publish-rule="publishRules.government_investor"
      >
        <template slot="label">
          <translate key="gobernment-investor">
            Has the government contributed to the project, either financially or in-kind?
          </translate>
        </template>

        <el-radio-group
          v-model="government_investor"
          v-validate="rules.government_investor"
          data-vv-name="government_investor"
          data-vv-as="Government investor"
          class="OnePerRow"
        >
          <el-radio :label="0">
            <translate>No, they have not yet contributed</translate>
          </el-radio>
          <el-radio :label="1">
            <translate>Yes, they are contributing in-kind people or time</translate>
          </el-radio>
          <el-radio :label="2">
            <translate>Yes, there is a financial contribution through MOH budget</translate>
          </el-radio>
        </el-radio-group>
      </custom-required-form-item>

      <custom-required-form-item
        class="ImplementingPartners"
        :draft-rule="draftRules.implementing_partners"
        :publish-rule="publishRules.implementing_partners"
      >
        <template slot="label">
          <translate key="implementing-partners">
            Who are your implementing partners?
          </translate>
        </template>

        <el-row
          v-for="(partner, index) in implementing_partners"
          :key="index"
        >
          <el-col :span="18">
            <custom-required-form-item
              :error="errors.first('implementing_partners_' + index)"
            >
              <el-input
                ref="implementingPartnersInput"
                v-validate="rules.implementing_partners"
                :value="partner"
                :data-vv-name="'implementing_partners_' + index"
                data-vv-validate-on="change"
                data-vv-as="Implementing partners"
                @input="updateImplmeentingPartners($event, index)"
                @keyup.enter.native="addImplementingPartners"
              />
            </custom-required-form-item>
          </el-col>
          <el-col :span="6">
            <add-rm-buttons
              :show-add="isLastAndExist(implementing_partners, index)"
              :show-rm="implementing_partners.length > 1"
              @add="addImplementingPartners"
              @rm="rmImplementingPartners(index)"
            />
          </el-col>
        </el-row>
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
import HisBucketSelector from '../HisBucketSelector';
import PlatformSelector from '../PlatformSelector';
import DigitalHealthInterventionsSelector from '../DigitalHealthInterventionsSelector';
import SubNationalLevelDeployment from '../SubNationalLevelDeployment';
import AddRmButtons from '../AddRmButtons';
import CoverageFieldset from '../CoverageFieldset';
import DonorSelector from '../DonorSelector';
import FormHint from '../FormHint';

import { mapGettersActions } from '../../../utilities/form';

export default {
  components: {
    CollapsibleCard,
    HealthSystemChallengesSelector,
    HisBucketSelector,
    HealthFocusAreasSelector,
    PlatformSelector,
    DigitalHealthInterventionsSelector,
    SubNationalLevelDeployment,
    AddRmButtons,
    CoverageFieldset,
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
      his_bucket: ['project', 'getHisBucket', 'setHisBucket', 0],
      coverageType: ['project', 'getCoverageType', 'setCoverageType', 0],
      national_level_deployment: ['project', 'getNationalLevelDeployment', 'setNationalLevelDeployment', 0],
      government_investor: ['project', 'getGovernmentInvestor', 'setGovernmentInvestor', 0],
      implementing_partners: ['project', 'getImplementingPartners', 'setImplementingPartners', 300, true],
      donors: ['project', 'getDonors', 'setDonors', 0]
    }),
    healthWorkers: {
      get () {
        return this.national_level_deployment ? this.national_level_deployment.health_workers : null;
      },
      set (value) {
        const coverage = { ...this.national_level_deployment, health_workers: value };
        this.national_level_deployment = coverage;
      }
    },
    clients: {
      get () {
        return this.national_level_deployment ? this.national_level_deployment.clients : null;
      },
      set (value) {
        const coverage = { ...this.national_level_deployment, clients: value };
        this.national_level_deployment = coverage;
      }
    },
    facilities: {
      get () {
        return this.national_level_deployment ? this.national_level_deployment.facilities : null;
      },
      set (value) {
        const coverage = { ...this.national_level_deployment, facilities: value };
        this.national_level_deployment = coverage;
      }
    }
  },
  watch: {
    implementing_partners: {
      immediate: false,
      handler (ip, oldIp) {
        if (oldIp && ip && ip.length > oldIp.length) {
          this.$nextTick(() => {
            if (this.$refs.implementingPartnersInput && this.$refs.implementingPartnersInput.length > 0) {
              this.$refs.implementingPartnersInput[this.$refs.implementingPartnersInput.length - 1].focus();
            }
          });
        }
      }
    }
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
    updateImplmeentingPartners (value, index) {
      const ip = [...this.implementing_partners];
      ip[index] = value;
      this.implementing_partners = ip;
    },
    addImplementingPartners () {
      const index = this.implementing_partners.length - 1;
      if (this.isLastAndExist(this.implementing_partners, index)) {
        this.implementing_partners = [...this.implementing_partners, null];
      }
    },
    rmImplementingPartners (index) {
      this.implementing_partners = this.implementing_partners.filter((ip, i) => i !== index);
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

    .ImplementingPartners {
      .el-row {
        margin-top: 20px;

        &:first-child {
          margin: 0;
        }
      }
    }
  }
</style>
