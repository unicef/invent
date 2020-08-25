<template>
  <div id="general" class="PortfolioManagers">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Add/remove manager(s)') | translate"
    >
      <custom-required-form-item
        v-model="managers"
        :error="errors.first('managers')"
        :draft-rule="draftRules.managers"
        :publish-rule="publishRules.managers"
        row
      >
        <template slot="label">
          <translate key="managers">
            Add/remove manager(s)
          </translate>
        </template>

        <country-office-select
          v-model="managers"
          v-validate="rules.managers"
          data-vv-name="managers"
          data-vv-as="managers"
          multiple
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
      managers: ["portfolio", "getManagers", "setManagers", 0]
    })
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([this.$validator.validate()]);
      console.log("Add/remove manager(s) published validation", validations);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate("managers")
      ]);
      console.log("Add/remove manager(s) draft validation", validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.PortfolioManagers {
}
</style>
