<template>
  <div id="general" class="GeneralOverview">
    <collapsible-card ref="collapsible" key="general" :title="$gettext('General overview') | translate" show-legend>
      <custom-required-form-item
        :error="errors.first('name')"
        :draft-rule="draftRules.name"
        :publish-rule="publishRules.name"
      >
        <template slot="label">
          <translate key="project-name"> What is the name of the initiative? </translate>
        </template>
        <template slot="tooltip">
          <el-tooltip
            class="item"
            content="Suggested format for the initiative name: Prefix (RO or CO) -
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
              An easy to understand name for your initiative. We recommend using descriptive names that describe what
              your initiative does. Please avoid acronyms, clever names/puns as well as the name of a specific
              technology or platform (e.g. RapidPro) as those can make it hard to search for an initiative. For large,
              potentially public initiatives, please do a quick search on the web for your initiative's name to make
              sure that name isn't already being used, as it can cause confusion.
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
        <span class="Hint">
          <br />
          <fa icon="info-circle" />
          <translate>
            If you encounter an error and/or cannot find the correct Unicef office, please let us know
          </translate>
          &nbsp;
          <el-button class="no-padding" type="text" size="mini" @click="openFeedback">
            <translate>HERE</translate>
          </el-button>
        </span>
      </custom-required-form-item>

      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <custom-required-form-item>
            <template slot="label">
              <translate key="field-offices"> City </translate>
            </template>
            {{ city }}
          </custom-required-form-item>
        </el-col>
        <el-col :span="12">
          <custom-required-form-item>
            <template slot="label">
              <translate key="country"> Country </translate>
            </template>
            {{ countryOfOffice }}
          </custom-required-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <custom-required-form-item>
            <template slot="label">
              <translate key="region">Region</translate>
            </template>
            {{ selectedRegion }}
          </custom-required-form-item>
        </el-col>
        <el-col :span="12">
          <custom-required-form-item>
            <template slot="label">
              <translate key="multi-or-regional-office">Multicountry or Regional Office</translate>
            </template>
            {{ regionalOffice }}
          </custom-required-form-item>
        </el-col>
      </el-row>

      <custom-required-form-item v-if="countryManagers.length > 0">
        <template #label>
          <translate>INVENT country focal point(s)</translate>
        </template>
        <ul class="ma-0">
          <li v-for="manager in countryManagers" :key="manager.id">{{ manager.name }} ({{ manager.email }})</li>
        </ul>
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('overview')"
        :draft-rule="draftRules.overview"
        :publish-rule="publishRules.overview"
      >
        <template slot="label">
          <translate key="overview">Please provide a brief overview of the initiative.</translate>
        </template>
        <template slot="tooltip">
          <el-tooltip
            class="item"
            content="Suggested format for the brief overview is to include the
            What, How, Who and Where. Example: Text-based behaviour change
            communication messages on maternal health for midwives in rural Philippines."
            placement="right"
          >
            <i class="el-icon-warning warning" />
          </el-tooltip>
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
              >This short description provides a clear understanding of the purpose and target group to a reader who
              does not know anything about the initiative. It should be 10-15 words or less and include the technology
              the technology or innovation, programme function and target beneficiary.
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
          <translate key="implementation-overview"> Please provide a detailed narrative of the initiative. </translate>
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
            <translate>
              What the initiative aims to achieve, detailing the purpose, summarizing the approach, solution and
              intended impact, and specifying current and planned activities during deployment.
            </translate>
          </p>
        </span>
      </custom-required-form-item>

      <el-form-item>
        <template slot="label">
          <translate key="cover">Upload initiative’s cover image</translate>
        </template>
        <file-upload
          :files.sync="coverImage"
          accept=".jpg,.jpeg,.png"
          preview-title="Cover image"
          @clear="coverImage = []"
        />
        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate>
              Upload the best quality image you have for the initiative. Uploaded image will be formatted to match the
              pages in the future, and the better quality the original image, the better result it will have displayed
              on invent. Image should be .png or .jpg and minimum height: 520px.
            </translate>
          </p>
        </span>
      </el-form-item>

      <custom-required-form-team-item
        :error="errors.first('contact_email')"
        :draft-rule="draftRules.contact_email"
        :publish-rule="publishRules.contact_email"
      >
        <template slot="label">
          <translate key="contact-email">Who is the focal point for this initiative?</translate>
        </template>

        <FocalProfileSelector
          v-model="contact_email"
          v-validate="rules.contact_email"
          data-vv-name="contact_email"
          data-vv-as="Contact email"
          :multiple="false"
        />

        <span class="Hint">
          <fa icon="info-circle" />
          <p>
            <translate
              >The focal point is the team member who is leading this work, and will act as the point of contact for
              anyone wishing to connect with the team.</translate
            >
          </p>
        </span>
      </custom-required-form-team-item>

      <div class="TeamArea">
        <custom-required-form-team-item
          v-model="team"
          :error="errors.first('team')"
          :draft-rule="draftRules.team"
          :publish-rule="publishRules.team"
        >
          <template slot="label">
            <translate key="team">Who are the team members for this initiative?</translate>
          </template>
          <UserProfileSelector
            v-model="team"
            :omit="contact_email"
            v-validate="rules.team"
            data-vv-name="team"
            data-vv-as="Team"
          />
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
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import TeamSelector from '../TeamSelector'
import CountryOfficeSelect from '../../common/CountryOfficeSelect'
import { mapGettersActions } from '../../../utilities/form'
import UserProfileSelector from '../UserProfileSelector.vue'
import FocalProfileSelector from '../FocalProfileSelector.vue'

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect,
    TeamSelector,
    CustomRequiredFormTeamItem,
    FileUpload,
    UserProfileSelector,
    FocalProfileSelector,
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
      getContactEmail: 'project/getContactEmail',
    }),

    ...mapGettersActions({
      name: ['project', 'getName', 'setName', 0],
      country: ['project', 'getCountry', 'setCountry', 0],
      country_office: ['project', 'getCountryOffice', 'setCountryOffice', 0],
      overview: ['project', 'getOverview', 'setOverview', 0],
      coverImage: ['project', 'getCoverImage', 'setCoverImage', 0],
      implementation_overview: ['project', 'getImplementationOverview', 'setImplementationOverview', 0],
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
