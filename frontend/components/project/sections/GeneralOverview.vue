<template>
  <div
    id="general"
    class="GeneralOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('General overview') | translate"
      show-legend
    >
      <custom-required-form-item
        :error="errors.first('name')"
        :draft-rule="draftRules.name"
        :publish-rule="publishRules.name"
      >
        <template slot="label">
          <translate key="project-name">
            Intiative Name
          </translate>
          <form-hint>
            <translate key="project-name-hint">
              If this is your first time uploading a project, a sample data form can be found here for reference.
            </translate>
          </form-hint>
        </template>
        <character-count-input
          v-model="name"
          v-validate="rules.name"
          :rules="rules.name"
          data-as-name="Name"
          data-vv-name="name"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('country')"
        :draft-rule="draftRules.country"
        :publish-rule="publishRules.country"
      >
        <template slot="label">
          <translate key="country">
            Country
          </translate>
        </template>
        <country-select
          v-model="country"
          v-validate="rules.country"
          data-vv-name="country"
          data-vv-as="Country"
        />
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="region">
            Region
          </translate>
        </template>
        {{ selectedRegion }}
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="field-offices">
            Field Office
          </translate>
        </template>
        <FieldOfficeSelector
          v-model="field_office"
          :country="country"
        />
      </custom-required-form-item>

      <custom-required-form-item v-if="modified">
        <template slot="label">
          <translate key="updated">
            Last updated
          </translate>
        </template>
        {{ lastUpdated }}
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('implementation_overview')"
        :draft-rule="draftRules.implementation_overview"
        :publish-rule="publishRules.implementation_overview"
      >
        <template slot="label">
          <translate key="implementation-overview">
            Initiative Description
          </translate>
          <form-hint>
            <translate key="implementation-overview-hint">
              Describe your overall digital health project design.
            </translate>
          </form-hint>
        </template>

        <character-count-input
          v-model="implementation_overview"
          v-validate="rules.implementation_overview"
          :rules="rules.implementation_overview"
          data-vv-name="implementation_overview"
          data-vv-as="Implementation Overview"
          type="textarea"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p><translate>Describe what the technology aims to achieve, detailing the users, the reasons for deploying the system, and current and future phases of deployment.</translate></p>
        </span>
      </custom-required-form-item>
      <el-row
        :gutter="20"
        type="flex"
      >
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('start_date')"
            :draft-rule="draftRules.start_date"
            :publish-rule="publishRules.start_date"
          >
            <template slot="label">
              <translate key="start-date">
                Project start date
              </translate>
              <form-hint>
                <translate key="start-date-hint">
                  When did the overall project, not just the digital health component, start.
                </translate>
              </form-hint>
            </template>

            <SafeDatePicker
              ref="Start date"
              v-model="start_date"
              v-validate="rules.start_date"
              :placeholder="$gettext('Start date') | translate"
              data-vv-name="start_date"
              data-vv-as="Start date"
              class="Date"
              align="left"
            />
          </custom-required-form-item>
        </el-col>

        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('end_date') || endDateError"
            :draft-rule="draftRules.end_date"
            :publish-rule="publishRules.end_date"
          >
            <template slot="label">
              <translate key="end-date">
                Project end date
              </translate>
              <form-hint>
                <translate key="end-date-hint">
                  When will the overall project be completed. If your project is ongoing, leave this field blank.
                </translate>
              </form-hint>
            </template>

            <SafeDatePicker
              v-model="end_date"
              v-validate="rules.end_date"
              :placeholder="$gettext('End date') | translate"
              data-vv-name="end_date"
              data-vv-as="End date"
              class="Date"
              align="left"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>

      <div class="TeamArea">
        <custom-required-form-team-item
          v-model="team"
          :error="errors.first('team')"
          :draft-rule="draftRules.team"
          :publish-rule="publishRules.team"
        >
          <template slot="label">
            <translate key="team">
              Add team members (editors)--can modify entry on Add New Project page
            </translate>
            <form-hint>
              <translate key="team-hint">
                Project editors can change and update all project information.
              </translate>
            </form-hint>
          </template>

          <team-selector
            v-model="team"
            v-validate="rules.team"
            data-vv-name="team"
            data-vv-as="Team"
          />
        </custom-required-form-team-item>
        <custom-required-form-team-item
          v-model="viewers"
          :error="errors.first('viewers')"
          :draft-rule="draftRules.viewers"
          :publish-rule="publishRules.viewers"
        >
          <template slot="label">
            <translate key="viewers">
              Add team members (viewers)--can receive notification that project has been added
            </translate>
            <form-hint>
              <translate key="viewers-hint">
                Project viewers will be able to view the full project details.
              </translate>
            </form-hint>
          </template>

          <team-selector
            v-model="viewers"
            v-validate="rules.viewers"
            data-vv-name="viewers"
            data-vv-as="Viewers"
          />
        </custom-required-form-team-item>
      </div>
    </collapsible-card>
  </div>
</template>

<script>
import { isAfter, format } from 'date-fns';
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js';
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js';
import CollapsibleCard from '../CollapsibleCard';
import TeamSelector from '../TeamSelector';
import FieldOfficeSelector from '../FieldOfficeSelector';
import CountrySelect from '../../common/CountrySelect';
import FormHint from '../FormHint';
import { mapGettersActions } from '../../../utilities/form';
import { mapGetters } from 'vuex';
import CustomRequiredFormTeamItem from '@/components/proxy/CustomRequiredFormTeamItem';

export default {
  components: {
    CollapsibleCard,
    CountrySelect,
    TeamSelector,
    FieldOfficeSelector,
    FormHint,
    CustomRequiredFormTeamItem
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      unicef_regions: 'system/getUnicefRegions',
      getCountryDetails: 'countries/getCountryDetails',
      modified: 'project/getModified'
    }),
    ...mapGettersActions({
      name: ['project', 'getName', 'setName', 0],
      country: ['project', 'getCountry', 'setCountry', 0],
      implementation_overview: ['project', 'getImplementationOverview', 'setImplementationOverview', 0],
      start_date: ['project', 'getStartDate', 'setStartDate', 0],
      end_date: ['project', 'getEndDate', 'setEndDate', 0],
      contact_name: ['project', 'getContactName', 'setContactName', 0],
      contact_email: ['project', 'getContactEmail', 'setContactEmail', 0],
      team: ['project', 'getTeam', 'setTeam', 0],
      viewers: ['project', 'getViewers', 'setViewers', 0],
      field_office: ['project', 'getFieldOffice', 'setFieldOffice', 0]
    }),
    endDateError () {
      if (this.usePublishRules && this.start_date && this.end_date && isAfter(this.start_date, this.end_date)) {
        return this.$gettext('End date must be after Start date');
      }
      return '';
    },
    selectedRegion () {
      const country = this.getCountryDetails(this.country);
      if (country) {
        const result = this.unicef_regions.find(uf => uf.id === country.unicef_region);
        return (result && result.name) || 'N/A';
      }
      return 'N/A';
    },
    lastUpdated () {
      return format(new Date(this.modified), 'DD/MM/YYYY HH:mm');
    }
  },
  methods: {
    async validate () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate(),
        Promise.resolve(this.endDateError === '')
      ]);
      console.log('General overview published validation', validations);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate('name'),
        this.$validator.validate('country'),
        this.$validator.validate('contact_email'),
        this.$validator.validate('team')
      ]);
      console.log('General overview draft validation', validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .GeneralOverview {
    .CountrySelector {
      width: 50%;
    }

    .Date {
      width: 100% !important;
    }
  }
</style>
