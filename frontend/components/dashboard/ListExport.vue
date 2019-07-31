<script>
import { mapGetters } from 'vuex';

export default {
  props: {
    projects: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails',
      getOrganisationDetails: 'system/getOrganisationDetails',
      getHealthFocusAreas: 'projects/getHealthFocusAreas',
      dashboardType: 'dashboard/getDashboardType',
      countryColumns: 'dashboard/getCountryColumns',
      donorColumns: 'dashboard/getDonorColumns'
    }),
    parsed () {
      if (!this.projects || !this.projects[0] || typeof this.projects !== 'object') {
        return null;
      }
      return this.projects.map(s => {
        return {
          ...s,
          country: this.parseCountry(s.country),
          investors: this.parseDonors(s.donors),
          health_focus_areas: this.parseHealthFocusAreas(s.health_focus_areas)
        };
      });
    }
  },
  methods: {
    parseCountry (countryId) {
      const country = this.getCountryDetails(countryId);
      return country && country.name ? country.name.toUpperCase() : '';
    },
    parseDonors (donors) {
      try {
        return donors.map(d => this.getDonorDetails(d)).filter(d => d).map(d => d.name).join(',');
      } catch (e) {
        console.log(e);
        return '';
      }
    },
    parseHealthFocusAreas (health_focus_areas) {
      try {
        return this.getHealthFocusAreas.filter(hfa => hfa.health_focus_areas.some(h => health_focus_areas.includes(h.id))).map(hf => hf.name).join(',');
      } catch (e) {
        console.log(e);
        return '';
      }
    },
    parseCustomQuestions (donor_answers, country_answers) {
      let custom = [];
      if (this.dashboardType === 'donor') {
        try {
          custom = this.donorColumns.map(dc => {
            const value = donor_answers && donor_answers[dc.donorId] ? donor_answers[dc.donorId][dc.originalId] : '';
            return {
              text: dc.label,
              value,
              donor: dc.donorId
            };
          });
        } catch (e) {
          console.error('failed to print custom donor answers', e);
        }
      }
      if (this.dashboardType === 'country') {
        try {
          custom = this.countryColumns.map(cc => {
            const value = country_answers ? country_answers[cc.originalId] : '';
            return {
              text: cc.label,
              value
            };
          });
        } catch (e) {
          console.error('failed to print custom country answers', e);
        }
      }
      return custom;
    }
  },
  render () {
    return this.$scopedSlots.default({
      parsed: this.parsed
    });
  }
};
</script>

<style>

</style>
