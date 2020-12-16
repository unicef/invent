<script>
import { mapGetters, mapState } from 'vuex'
import pickBy from 'lodash/pickBy'
import pick from 'lodash/pick'
import flatten from 'lodash/flatten'

export default {
  props: {
    projects: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
      mapColKeys: (state) => state.dashboard.mapColKeys,
    }),
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails',
      getHealthFocusAreas: 'projects/getHealthFocusAreas',
      dashboardType: 'dashboard/getDashboardType',
      countryColumns: 'dashboard/getCountryColumns',
      donorColumns: 'dashboard/getDonorColumns',
      goalAreas: 'projects/getGoalAreas',
      resultAreas: 'projects/getResultAreas',
      capabilityLevels: 'projects/getCapabilityLevels',
      capabilityCategories: 'projects/getCapabilityCategories',
      capabilitySubcategories: 'projects/getCapabilitySubcategories',
      regions: 'system/getUnicefRegions',
      platforms: 'projects/getTechnologyPlatforms',
      hscChallenges: 'projects/getHscChallenges',
      selectedCol: 'dashboard/getSelectedColumns',
      // new fields
      getSectors: 'projects/getSectors',
      getRegionalPriorities: 'projects/getRegionalPriorities',
      getInnovationWays: 'projects/getInnovationWays',
      getInnovationCategories: 'projects/getInnovationCategories',
      getStages: 'projects/getStages',
      getHardware: 'projects/getHardware',
      getNontech: 'projects/getNontech',
      getFunctions: 'projects/getFunctions',
      // single new field
      getRegionalOffices: 'projects/getRegionalOffices',
      getInfoSec: 'projects/getInfoSec',
    }),
    parsed() {
      if (
        !this.projects ||
        !this.projects[0] ||
        typeof this.projects !== 'object'
      ) {
        return null
      }
      return this.projects.map((s) => {
        const parsed = {
          ...s,
          country: this.parseCountry(s.country),
          country_office: s.country_office
            ? this.offices.find((obj) => obj.id === s.country_office).name || ''
            : '',
          // investors: this.parseDonors(s.donors),
          health_focus_areas: this.parseHealthFocusAreas(s.health_focus_areas),
          hsc_challenges: this.parseHscChallenges(s.hsc_challenges),
          capability_levels: this.parseFlatList(
            s.capability_levels,
            'capabilityLevels'
          ),
          capability_categories: this.parseFlatList(
            s.capability_categories,
            'capabilityCategories'
          ),
          capability_subcategories: this.parseFlatList(
            s.capability_categories,
            'capabilitySubcategories'
          ),
          goal_area: this.parseSingleSelection(s.goal_area, 'goalAreas'),
          result_area: this.parseSingleSelection(s.result_area, 'resultAreas'),
          region: this.parseSingleSelection(s.region, 'regions'),
          // software: this.parseFlatList(s.platforms, 'platforms'),
          approved: this.parseBoolean(s.approved),
          ...this.parseCustomQuestions(s.donor_answers),
          donors: undefined,
          organisation: undefined,
          platforms: this.parseFlatList(s.platforms, 'platforms'),
          country_answers: undefined,
          donor_answers: undefined,
          // new fields
          regional_office: this.parseList(this.getRegionalOffices, [
            s.regional_office,
          ]),
          unicef_sector: this.parseList(this.getSectors, s.unicef_sector),
          innovation_ways: this.parseList(
            this.getInnovationWays,
            s.innovation_ways
          ),
          stages: this.parseList(this.getStages, s.stages),
          hardware: this.parseList(this.getHardware, s.hardware),
          nontech: this.parseList(this.getNontech, s.nontech),
          functions: this.parseList(this.getFunctions, s.functions),
          isc: this.parseList(this.getInfoSec, [s.isc]),
          regional_priorities: this.parseList(
            this.getRegionalPriorities,
            s.regional_priorities
          ),
        }
        let selectedCols = []
        this.mapColKeys.forEach((i) => {
          if (this.selectedCol.includes(i.id)) selectedCols.push(i.key)
        })
        selectedCols = flatten(selectedCols)
        return pick(
          pickBy(parsed, (v) => v !== undefined && v !== null),
          selectedCols
        )
      })
    },
  },
  methods: {
    parseBoolean(value) {
      return value ? this.$gettext('yes') : this.$gettext('no')
    },
    parseFlatList(flatList, type) {
      try {
        const all = typeof this[type] === 'function' ? this[type]() : this[type]
        return all
          .filter((cb) => flatList.includes(cb.id))
          .map((cb) => cb.name)
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseList(list, filter) {
      return list
        .filter((tp) => filter.includes(tp.id))
        .map((i) => i.name)
        .join(', ')
    },
    parseSingleSelection(id, type) {
      try {
        const item = this[type].find((i) => i.id === id)
        return item && item.name ? item.name : ''
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseCountry(countryId) {
      const country = this.getCountryDetails(countryId)
      return country && country.name ? country.name : ''
    },
    parseDonors(donors) {
      try {
        return donors
          .map((d) => this.getDonorDetails(d))
          .filter((d) => d)
          .map((d) => d.name)
          .join(',')
      } catch (e) {
        console.log(e)
        return ''
      }
    },
    parseHscChallenges(values) {
      try {
        return this.hscChallenges
          .reduce((a, c) => {
            c.challenges.forEach((cc) => {
              if (values.includes(cc.id)) {
                a.push(cc.challenge)
              }
            })
            return a
          }, [])
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseHealthFocusAreas(health_focus_areas) {
      try {
        return this.getHealthFocusAreas
          .filter((hfa) =>
            hfa.health_focus_areas.some((h) =>
              health_focus_areas.includes(h.id)
            )
          )
          .map((hf) => hf.name)
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseCustomQuestions(donor_answers, country_answers) {
      let custom = {}
      if (this.dashboardType === 'donor') {
        try {
          this.donorColumns.forEach((dc) => {
            const value =
              donor_answers && donor_answers[dc.donorId]
                ? donor_answers[dc.donorId][dc.originalId]
                : ''
            custom[dc.label] = value.join(',')
          })
        } catch (e) {
          console.warn('failed to parse custom donor answers', e)
        }
      }
      if (this.dashboardType === 'country') {
        try {
          custom = this.countryColumns.forEach((cc) => {
            const value = country_answers ? country_answers[cc.originalId] : ''
            custom[cc.label] = value.join(',')
          })
        } catch (e) {
          console.warn('failed to parse custom country answers', e)
        }
      }
      return custom
    },
  },
  render() {
    return this.$scopedSlots.default({
      parsed: this.parsed,
    })
  },
}
</script>

<style></style>
