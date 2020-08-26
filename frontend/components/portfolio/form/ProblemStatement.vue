<template>
  <div id="general" class="ProblemStatement">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Problem Statements') | translate"
    >
      <statements
        v-model="statements"
        v-validate="rules"
        :rules="rules"
        data-as-name="Statements"
        data-vv-name="statements"
      />
    </collapsible-card>
  </div>
</template>

<script>
import { mapGettersActions } from "@/utilities/form";
import VeeValidationMixin from "@/components/mixins/VeeValidationMixin";
import PortfolioFieldsetMixin from "@/components/mixins/PortfolioFieldsetMixin";
import CollapsibleCard from "@/components/portfolio/CollapsibleCard";
import Statements from "@/components/portfolio/form/inputs/Statements";

export default {
  components: {
    CollapsibleCard,
    Statements
  },
  mixins: [VeeValidationMixin, PortfolioFieldsetMixin],
  computed: {
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
