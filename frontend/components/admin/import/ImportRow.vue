<template>
  <div>
    <slot
      :errors="errors"
      :valid="valid"
      :data="data"
      :original="original"
      :handleValidation="handleValidation"
      :rowSave="save"
      :scrollToError="scrollToError"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { projectFields } from '@/utilities/projects';
import { apiWriteParser } from '@/utilities/api';

export default {
  props: {
    row: {
      type: Object,
      default: () => ({})
    },
    customFieldsLib: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      errors: []
    };
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/getProfile',
      dhi: 'projects/getDigitalHealthInterventions'
    }),
    firstDHI () {
      if (this.dhi && this.dhi[0].subGroups[0] && this.dhi[0].subGroups[0].strategies) {
        return this.dhi[0].subGroups[0].strategies[0].id;
      }
      return null;
    },
    valid () {
      return this.errors.length === 0;
    },
    data () {
      if (this.row && this.row.data) {
        return this.row.data;
      }
      return {};
    },
    original () {
      if (this.row && this.row.original_data) {
        return this.row.original_data;
      }
      return {};
    }
  },
  methods: {
    handleValidation (valid, msg, field) {
      if (valid) {
        this.errors = this.errors.filter(e => e.field !== field);
      } else {
        this.errors.push({
          field,
          msg
        });
      }
    },
    scrollToError () {
      if (!this.valid) {
        const container = window.document.querySelector('.ExportDataTable .Container');
        const header = container.querySelector('.Headers');
        const elm = this.$el.querySelector('.ValidationError, .ParsingError');
        elm.scrollIntoView(true);
        if (container.scrollTop) {
          container.scroll(container.scrollLeft, container.scrollTop - header.clientHeight);
        }
      }
    },
    async save (country, donor, publish, office) {
      const filled = this.$children.filter(sc => sc.column && !['custom_fields'].includes(sc.column));

      const countryCustom = this.$children.filter(sc => sc.type && sc.type.startsWith('MOH')).map(c => ({
        question_id: this.customFieldsLib[c.type].id,
        answer: c.apiValue()
      })).filter(a => a.answer);

      const donorCustom = this.$children.filter(sc => sc.type && sc.type.startsWith('INV')).map(c => ({
        donor_id: donor,
        question_id: this.customFieldsLib[c.type].id,
        answer: c.apiValue()
      })).filter(a => a.answer);

      const result = filled.reduce((a, c) => {
        a[c.column] = c.apiValue();
        return a;
      }, projectFields());
      result.team = [this.userProfile.id];
      result.country = country;
      result.country_office = office
      result.donors = [donor];
      const parsed = apiWriteParser(result, countryCustom, donorCustom);
      const { data } = await this.$axios.post(`api/projects/draft/${office}/`, parsed);
      if (publish) {
        await this.$axios.put(`api/projects/publish/${data.id}/${office}/`, parsed);
      }
      const dataRow = this.row;
      dataRow.project = data.id;
      this.$emit('update:row', dataRow);
      return dataRow;
    }
  }
};
</script>

<style>

</style>
