<template>
  <div id="general" class="GeneralOverview">
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
          <translate key="project-name"> Initiative Name </translate>
          <form-hint>
            <translate key="project-name-hint">
              If this is your first time uploading a project, a sample data form
              can be found here for reference.
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
        :error="
          errors.first('country_office')
            ? errors.first('country_office').replace('_', ' ')
            : undefined
        "
        :draft-rule="draftRules.country_office"
        :publish-rule="publishRules.country_office"
      >
        <template slot="label">
          <translate key="country_office"> Unicef Office </translate>
        </template>
        <country-office-select
          v-model="country_office"
          v-validate="rules.country_office"
          data-vv-name="country_office"
          data-vv-as="country_office"
        />
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="field-offices"> City </translate>
        </template>
        {{ city }}
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="country"> Country </translate>
        </template>
        {{ countryOfOffice }}
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="region"> Region </translate>
        </template>
        {{ selectedRegion }}
      </custom-required-form-item>

      <custom-required-form-item>
        <template slot="label">
          <translate key="multi-or-regional-office">
            Multicountry or Regional Office
          </translate>
        </template>
        {{ regionalOffice }}
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('overview')"
        :draft-rule="draftRules.overview"
        :publish-rule="publishRules.overview"
      >
        <template slot="label">
          <translate key="overview">
            Please provide a brief overview of the initiative.
          </translate>
          <form-hint>
            <translate key="overview-hint"> - </translate>
          </form-hint>
        </template>

        <character-count-input
          v-model="overview"
          v-validate="rules.overview"
          :rules="rules.overview"
          data-vv-name="overview"
          data-vv-as="Overview"
          type="textarea"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate
              >The short description provides a clear understanding of the
              purpose and target group to a reader who does not know anything
              about the initiative. It should include the technology or
              innovation, programme function and target beneficiary. eg.
              Text-based behaviour change communication messages on maternal
              health for midwives.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('implementation_overview')"
        :draft-rule="draftRules.implementation_overview"
        :publish-rule="publishRules.implementation_overview"
      >
        <template slot="label">
          <translate key="implementation-overview"> Description </translate>
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
          <p>
            <translate
              >Describe what the technology aims to achieve, detailing the
              users, the reasons for deploying the system, and current and
              future phases of deployment.</translate
            >
          </p>
        </span>
      </custom-required-form-item>
      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('contact_name')"
            :draft-rule="draftRules.contact_name"
            :publish-rule="publishRules.contact_name"
          >
            <template slot="label">
              <translate key="contact-name">Contact Name</translate>
              <form-hint>
                <translate key="contact-name-hint">
                  This is the individual who will be the lead point of contact
                  for any queries through the DHA.
                </translate>
              </form-hint>
            </template>

            <character-count-input
              v-model="contact_name"
              v-validate="rules.contact_name"
              :rules="rules.contact_name"
              data-vv-name="contact_name"
              data-vv-as="Contact name"
            />
          </custom-required-form-item>
        </el-col>
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('contact_email')"
            :draft-rule="draftRules.contact_email"
            :publish-rule="publishRules.contact_email"
          >
            <template slot="label">
              <translate key="contact-email">Contact Email</translate>
            </template>

            <character-count-input
              v-model="contact_email"
              v-validate="rules.contact_email"
              :rules="rules.contact_email"
              data-vv-name="contact_email"
              data-vv-as="Contact email"
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
            <translate key="team"> Add team members (editors) </translate>
            <form-hint>
              <translate key="team-hint">
                Editors can edit and publish initiatives
              </translate>
            </form-hint>
          </template>

          <team-selector
            v-model="team"
            v-validate="rules.team"
            data-vv-name="team"
            data-vv-as="Team"
          />

          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>Editors can edit and publish initiatives</translate>
            </p>
          </span>
        </custom-required-form-team-item>
        <custom-required-form-team-item
          v-model="viewers"
          :error="errors.first('viewers')"
          :draft-rule="draftRules.viewers"
          :publish-rule="publishRules.viewers"
        >
          <template slot="label">
            <translate key="viewers"> Add team members (viewers) </translate>
            <form-hint>
              <translate key="viewers-hint">
                Viewers can view initiative drafts
              </translate>
            </form-hint>
          </template>

          <team-selector
            v-model="viewers"
            v-validate="rules.viewers"
            data-vv-name="viewers"
            data-vv-as="Viewers"
          />

          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>Viewers can view initiative drafts</translate>
            </p>
          </span>
        </custom-required-form-team-item>
      </div>

      <custom-required-form-item v-if="modified">
        <template slot="label">
          <translate key="updated"> Last updated </translate>
        </template>
        {{ lastUpdated }}
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import { format } from 'date-fns'
import { mapGetters, mapState } from 'vuex'
import CustomRequiredFormTeamItem from '@/components/proxy/CustomRequiredFormTeamItem'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import TeamSelector from '../TeamSelector'
import CountryOfficeSelect from '../../common/CountryOfficeSelect'
import FormHint from '../FormHint'
import { mapGettersActions } from '../../../utilities/form'

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect,
    TeamSelector,
    FormHint,
    CustomRequiredFormTeamItem,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
      office: (state) => state.offices.office,
    }),
    ...mapGetters({
      unicef_regions: 'system/getUnicefRegions',
      getCountryDetails: 'countries/getCountryDetails',
      modified: 'project/getModified',
      regionalOffices: 'projects/getRegionalOffices',
    }),
    ...mapGettersActions({
      name: ['project', 'getName', 'setName', 0],
      country: ['project', 'getCountry', 'setCountry', 0],
      country_office: ['project', 'getCountryOffice', 'setCountryOffice', 0],
      overview: ['project', 'getOverview', 'setOverview', 0],
      implementation_overview: [
        'project',
        'getImplementationOverview',
        'setImplementationOverview',
        0,
      ],
      contact_name: ['project', 'getContactName', 'setContactName', 0],
      contact_email: ['project', 'getContactEmail', 'setContactEmail', 0],
      team: ['project', 'getTeam', 'setTeam', 0],
      viewers: ['project', 'getViewers', 'setViewers', 0],
    }),
    selectedRegion() {
      const office = this.offices.find((obj) => obj.id === this.country_office)
      if (office) {
        const result = this.unicef_regions.find((uf) => uf.id === office.region)
        return (result && result.name) || ' ' // N/A
      }
      return ' ' // N/A
    },
    countryOfOffice() {
      const office = this.offices.find((obj) => obj.id === this.country_office)
      return office ? this.getCountryDetails(office.country).name : ' ' // N/A
    },
    city() {
      const office = this.offices.find((obj) => obj.id === this.country_office)
      return office ? office.city : ' ' // N/A
    },
    regionalOffice() {
      const office = this.regionalOffices.find(
        (obj) => obj.id === this.office.regional_office
      )
      return office ? office.name : ''
    },
    lastUpdated() {
      return format(new Date(this.modified), 'DD/MM/YYYY HH:mm')
    },
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      console.log('General overview published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('name'),
        this.$validator.validate('country_office'),
        this.$validator.validate('contact_email'),
        this.$validator.validate('team'),
      ])
      console.log('General overview draft validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.GeneralOverview {
  .CountrySelector,
  .select-office {
    width: 50%;
  }

  .Date {
    width: 100% !important;
  }
}

.TeamArea {
  position: relative;
}
</style>
