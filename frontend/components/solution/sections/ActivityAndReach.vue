<template>
  <div id="activity-and-reach" class="GeneralOverview">
    <collapsible-card ref="collapsible" key="general" :title="$gettext('Activity and Reach') | translate" show-legend>
      <custom-required-form-item
        :error="errors.first('name')"
        :draft-rule="draftRules.name"
        :publish-rule="publishRules.name"
      >
        <template slot="label">
          <translate key="solution-name"> What is the name of the solution? </translate>
        </template>
        <template slot="tooltip">
          <el-tooltip
            class="item"
            content="Suggested format for the solution name: Prefix (RO or CO) -
              (Sector or Function) - Name of Initiative (Identifier). Example: PHL - T4D -
              Knowledge, Innovation and Data System (KIDS)"
            placement="right"
          >
            <i class="el-icon-warning warning" />
          </el-tooltip>
        </template>

        <character-count-input
          v-model="name"
          v-validate="rules.name"
          :rules="rules.name"
          data-as-name="Name"
          data-vv-name="name"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              A short and memorable name for this solution. This name will be used across all implementing countries,
              and will allow colleagues to find and remember the solution. This should match any public-facing name for
              this solution.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('country_office') ? errors.first('country_office').replace('_', ' ') : undefined"
        :draft-rule="draftRules.country_office"
        :publish-rule="publishRules.country_office"
      >
        <template slot="label">
          <translate key="country_office"> Which UNICEF Office supports the initiative? </translate>
        </template>

        <country-office-select
          v-model="country_office"
          v-validate="rules.country_office"
          data-vv-name="country_office"
          data-vv-as="country_office"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              The name of the country or field office location. Start typing the name of the UNICEF country office to
              show all the field locations.
            </translate>
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
              <translate key="contact-name">Who is the focal point of contact for this initiative?</translate>
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
              <translate key="contact-email"> Focal Point Email </translate>
            </template>

            <character-count-input
              v-model="contact_email"
              v-validate="rules.contact_email"
              :rules="rules.contact_email"
              data-vv-name="contact_email"
              data-vv-as="Contact email"
              @blur="addContactToTeam"
              @keyup.enter.native="addContactToTeam"
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
            <translate key="team">Who else should be able to modify this initiative's entry?</translate>
          </template>

          <team-selector v-model="team" v-validate="rules.team" data-vv-name="team" data-vv-as="Team" />

          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>These team members can modify entries on "+ New Initiative" page.</translate>
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
            <translate key="viewers">
              Who should receive updates that this initiative has been added or modified?
            </translate>
          </template>

          <team-selector v-model="viewers" v-validate="rules.viewers" data-vv-name="viewers" data-vv-as="Viewers" />

          <span class="Hint">
            <fa icon="info-circle" />
            <p>
              <translate>These team members will receive a notification when an initiative has been added.</translate>
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
import FileUpload from '@/components/common/FileUpload'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '@/components/project/CollapsibleCard'
import TeamSelector from '@/components/project/TeamSelector'
import CountryOfficeSelect from '@/components/common/CountryOfficeSelect'
import { mapGettersActions } from '@/utilities/form'

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect,
    TeamSelector,
    CustomRequiredFormTeamItem,
    FileUpload,
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
      userProfiles: 'system/getUserProfilesNoFilter',
    }),
    ...mapGettersActions({
      name: ['project', 'getName', 'setName', 0],
      country: ['project', 'getCountry', 'setCountry', 0],
      country_office: ['project', 'getCountryOffice', 'setCountryOffice', 0],
      overview: ['project', 'getOverview', 'setOverview', 0],
      coverImage: ['project', 'getCoverImage', 'setCoverImage', 0],
      implementation_overview: ['project', 'getImplementationOverview', 'setImplementationOverview', 0],
      contact_name: ['project', 'getContactName', 'setContactName', 0],
      contact_email: ['project', 'getContactEmail', 'setContactEmail', 0],
      team: ['project', 'getTeam', 'setTeam', 0],
      viewers: ['project', 'getViewers', 'setViewers', 0],
    }),
    officeData() {
      return this.offices.find((obj) => obj.id === this.country_office)
    },
    selectedRegion() {
      if (this.officeData) {
        const result = this.unicef_regions.find((uf) => uf.id === this.officeData.region)
        return (result && result.name) || '-' // N/A
      }
      return ' ' // N/A
    },
    countryOfOffice() {
      return this.officeData ? this.getCountryDetails(this.officeData.country).name : '-' // N/A
    },
    countryManagers() {
      return this.officeData?.managers.length > 0 ? this.officeData?.managers : []
    },
    city() {
      return this.officeData ? this.officeData.city : '-' // N/A
    },
    regionalOffice() {
      const office = this.regionalOffices.find((obj) => obj.id === this.office.regional_office)
      return office ? office.name : ''
    },
    lastUpdated() {
      return this.modified ? format(new Date(this.modified), 'DD/MM/YYYY HH:mm') : ''
    },
  },
  watch: {
    async country_office() {
      if (this.officeData) {
        await this.$store.dispatch('countries/loadCountryDetails', this.officeData.country)
        this.country = this.officeData.country
      }
    },
  },
  methods: {
    async addContactToTeam() {
      const validEmail = await this.$validator.validate('contact_email')
      if (!validEmail || this.contact_email === '') return
      const teamMember = this.userProfiles.find((user) => {
        return user.email === this.contact_email
      })
      if (teamMember !== undefined) {
        if (!this.team.includes(teamMember.id)) {
          const team = this.team.concat(teamMember.id)
          this.team = team
        }
      } else {
        const addToTeam =
          validEmail &&
          (this.contact_email.endsWith('unicef.org') || this.contact_email.endsWith('pulilab.com')) &&
          !this.team.includes(this.contact_email)
        if (addToTeam) {
          const team = this.team.concat(this.contact_email)
          this.team = team
        }
      }
    },
    openFeedback() {
      this.$store.commit('user/SET_FEEDBACK', {
        feedbackOn: true,
        feedbackForm: {
          subject: this.$gettext('UNICEF Office Issue'),
          message: this.$gettext('Please provide an email address: '),
        },
      })
    },
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

  .no-padding {
    padding-top: 0;
    padding-bottom: 0;
  }
  .ma-0 {
    margin: 0;
  }
}

.TeamArea {
  position: relative;
}
</style>
