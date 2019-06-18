<template>
  <div
    v-if="countryQuestions && countryQuestions.length >0"
    id="countrycustom"
    class="CountryCustom"
  >
    <collapsible-card
      ref="collapsible"
      :title="customFieldsName(country.name)"
    >
      <custom-field
        v-for="(field, index) in countryQuestions"
        :id="field.id"
        ref="customQuestion"
        :key="field.id"
        :index="index"
        :api-errors="apiErrors"
        :type="field.type"
        :question="field.question"
        :is-required="field.required"
        :is-private="field.private"
        :options="field.options"
        :do-validation="usePublishRules"
      />
    </collapsible-card>
  </div>
</template>

<script>
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js';
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js';
import { mapGetters } from 'vuex';
import CollapsibleCard from '../CollapsibleCard';
import CustomField from '../CustomField';

export default {
  components: {
    CollapsibleCard,
    CustomField
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      projectCountry: 'project/getCountry'
    }),
    country () {
      if (this.projectCountry) {
        return this.getCountryDetails(this.projectCountry);
      }
      return null;
    },
    countryQuestions () {
      if (this.country) {
        return this.country.country_questions;
      }
      return [];
    }
  },
  methods: {
    customFieldsName (name) {
      return this.$gettext('{name} custom fields', { name });
    },
    async validate () {
      if (this.$refs.collapsible) {
        this.$refs.collapsible.expandCard();
      }
      if (this.$refs.customQuestion) {
        const validations = await Promise.all(this.$refs.customQuestion.map(r => r.validate()));
        console.log('Custom country questions validators', validations);
        return validations.reduce((a, c) => a && c, true);
      }
      return true;
    }
  }
};
</script>

<style lang="less">
 @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .CountryCustom {}

</style>
