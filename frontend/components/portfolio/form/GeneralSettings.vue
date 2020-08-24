<template>
  <div id="general" class="GeneralSettings">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('General settings') | translate"
    >
      <custom-required-form-item
        :error="errors.first('name')"
        :draft-rule="draftRules.name"
        :publish-rule="publishRules.name"
        row
      >
        <template slot="label">
          <translate key="project-name">
            Portfolio name
          </translate>
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
        :error="errors.first('description')"
        :draft-rule="draftRules.implementation_overview"
        :publish-rule="publishRules.implementation_overview"
        row
      >
        <template slot="label">
          <translate key="implementation-overview">
            Description
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
          <p>
            <translate
              >Describe what the technology aims to achieve, detailing the
              users, the reasons for deploying the system, and current and
              future phases of deployment.</translate
            >
          </p>
        </span>
      </custom-required-form-item>

      <custom-required-form-item
        :error="
          errors.first('country_office')
            ? errors.first('country_office').replace('_', ' ')
            : undefined
        "
        :draft-rule="draftRules.country_office"
        :publish-rule="publishRules.country_office"
        row
      >
        <template slot="label">
          <translate key="country_office">
            Status
          </translate>
        </template>
        <country-office-select
          v-model="country_office"
          v-validate="rules.country_office"
          data-vv-name="country_office"
          data-vv-as="country_office"
        />
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import { isAfter, format } from "date-fns";
import VeeValidationMixin from "@/components/mixins/VeeValidationMixin";
import ProjectFieldsetMixin from "@/components/mixins/ProjectFieldsetMixin";
import CollapsibleCard from "@/components/portfolio/CollapsibleCard";
import TeamSelector from "@/components/project/TeamSelector";
import FieldOfficeSelector from "@/components/project/FieldOfficeSelector";
import CountryOfficeSelect from "@/components/common/CountryOfficeSelect";
import FormHint from "@/components/project/FormHint";
import { mapGettersActions } from "@/utilities/form";
import { mapGetters, mapState } from "vuex";
import CustomRequiredFormTeamItem from "@/components/proxy/CustomRequiredFormTeamItem";

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect,
    TeamSelector,
    FieldOfficeSelector,
    FormHint,
    CustomRequiredFormTeamItem
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapState({
      offices: state => state.offices.offices
    }),
    ...mapGetters({
      unicef_regions: "system/getUnicefRegions",
      getCountryDetails: "countries/getCountryDetails",
      modified: "project/getModified"
    }),
    ...mapGettersActions({
      name: ["project", "getName", "setName", 0],
      country: ["project", "getCountry", "setCountry", 0],
      country_office: ["project", "getCountryOffice", "setCountryOffice", 0],
      implementation_overview: [
        "project",
        "getImplementationOverview",
        "setImplementationOverview",
        0
      ],
      start_date: ["project", "getStartDate", "setStartDate", 0],
      end_date: ["project", "getEndDate", "setEndDate", 0],
      contact_name: ["project", "getContactName", "setContactName", 0],
      contact_email: ["project", "getContactEmail", "setContactEmail", 0],
      team: ["project", "getTeam", "setTeam", 0],
      viewers: ["project", "getViewers", "setViewers", 0],
      field_office: ["project", "getFieldOffice", "setFieldOffice", 0]
    }),
    endDateError() {
      if (
        this.usePublishRules &&
        this.start_date &&
        this.end_date &&
        isAfter(this.start_date, this.end_date)
      ) {
        return this.$gettext("End date must be after Start date");
      }
      return "";
    },
    selectedRegion() {
      const office = this.offices.find(obj => obj.id === this.country_office);
      if (office) {
        const result = this.unicef_regions.find(uf => uf.id === office.region);
        return (result && result.name) || "N/A";
      }
      return "N/A";
    },
    countryOfOffice() {
      const office = this.offices.find(obj => obj.id === this.country_office);
      return office ? this.getCountryDetails(office.country).name : "N/A";
    },
    lastUpdated() {
      return format(new Date(this.modified), "DD/MM/YYYY HH:mm");
    }
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate(),
        Promise.resolve(this.endDateError === "")
      ]);
      console.log("General settings published validation", validations);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate("name"),
        this.$validator.validate("country_office"),
        this.$validator.validate("contact_email"),
        this.$validator.validate("team")
      ]);
      console.log("General settings draft validation", validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.GeneralSettings {
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
