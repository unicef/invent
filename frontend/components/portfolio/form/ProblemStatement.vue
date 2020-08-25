<template>
  <div id="general" class="ProblemStatement">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Problem Statements') | translate"
    >
      <custom-required-form-item
        :error="errors.first('statements')"
        :draft-rule="draftRules.statements"
        :publish-rule="publishRules.statements"
        row
      >
        <template slot="label">
          <translate key="portfolio-statements">
            Portfolio statements
          </translate>
        </template>
        <character-count-input
          v-model="statements"
          v-validate="rules.statements"
          :rules="rules.statements"
          data-as-name="Statements"
          data-vv-name="statements"
        />
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import { mapGettersActions } from "@/utilities/form";
import { mapGetters, mapState } from "vuex";
import VeeValidationMixin from "@/components/mixins/VeeValidationMixin";
import PortfolioFieldsetMixin from "@/components/mixins/PortfolioFieldsetMixin";
import CollapsibleCard from "@/components/portfolio/CollapsibleCard";
import CountryOfficeSelect from "@/components/common/CountryOfficeSelect";

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect
  },
  mixins: [VeeValidationMixin, PortfolioFieldsetMixin],
  computed: {
    ...mapState({
      offices: state => state.offices.offices
    }),
    ...mapGetters({
      getCountryDetails: "countries/getCountryDetails"
    }),
    ...mapGettersActions({
      statements: ["portfolio", "getStatements", "setStatements", 0]
    })
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([this.$validator.validate()]);
      console.log("General settings published validation", validations);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate("statements")
      ]);
      console.log("General settings draft validation", validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";
</style>
