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
  data() {
    return {
      problemStatements: [],
      officialScoreFields: [
        this.$gettext('Problem Statement Alignment (Official Score)'),
        this.$gettext('Reach: Number of Children Impacted (Official Score)'),
        this.$gettext('Reach: Addressing Target Populations (Official Score)'),
        this.$gettext('Risk Assessment (Official Score)'),
        this.$gettext('Evidence of Effectiveness (Official Score)'),
        this.$gettext('Newness of Solution (Tool) (Official Score)'),
        this.$gettext('Newness of Challenge (Official Score)'),
        this.$gettext('Path to Scale (Official Score)'),
        this.$gettext('Overall Summary (Official Score)'),
        this.$gettext('Impact (Official Score)'),
        this.$gettext('Scale Phase (Official Score)'),
      ],
      reviewScoresFields: [
        this.$gettext('Reviewer Name'),
        this.$gettext('Review Status'),
        this.$gettext('Problem Statement Alignment'),
        this.$gettext('Comments'),
        this.$gettext('Reach: Number of Children Impacted'),
        this.$gettext('Comments'),
        this.$gettext('Reach: Addressing Target Populations'),
        this.$gettext('Comments'),
        this.$gettext('Risk Assessment'),
        this.$gettext('Comments'),
        this.$gettext('Evidence of Effectiveness'),
        this.$gettext('Comments'),
        this.$gettext('Newness of Solution (Tool)'),
        this.$gettext('Comments'),
        this.$gettext('Newness of Challenge'),
        this.$gettext('Comments'),
        this.$gettext('Path to Scale'),
        this.$gettext('Comments'),
        this.$gettext('Overall Summary'),
      ],
      colKeyValues: [
        {
          id: '1',
          label: 'Initiative Name',
          key: 'name',
          parse: (name) => name || '',
        },
        {
          id: '2',
          label: 'Country',
          key: 'country',
          parse: (country) => this.parseCountry(country),
        },
        {
          id: '3',
          label: 'Last updated',
          key: 'modified',
          parse: (datetime) => datetime || '',
        },
        {
          id: '4',
          label: 'Unicef Office',
          key: 'country_office',
          parse: (country_office) =>
            country_office ? this.offices.find((obj) => obj.id === country_office).name || '' : '',
        },
        {
          id: '5',
          label: 'Region',
          key: 'region',
          parse: (region) => this.parseSingleSelection(region, 'regions'),
        },
        {
          id: '7',
          label: 'Programme Focal Point Name',
          // key: ['contact_name', 'contact_email'],
          key: 'contact_name',
          parse: (contact_name) => contact_name || '',
        },
        {
          id: '8',
          label: 'Initiative Description',
          key: 'implementation_overview',
          parse: (implementation_overview) => implementation_overview || '',
        },
        {
          id: '10',
          label: 'Health Focus Areas',
          key: 'health_focus_areas',
          parse: (health_focus_areas) => this.parseHealthFocusAreas(health_focus_areas),
        },
        {
          id: '11',
          label: 'Goal Area',
          key: 'goal_area',
          parse: (goal_area) => this.parseSingleSelection(goal_area, 'goalAreas'),
        },
        {
          id: '12',
          label: 'Result Area',
          key: 'result_area',
          parse: (result_area) => this.parseSingleSelection(result_area, 'resultAreas'),
        },
        {
          id: '13',
          label: 'Capability Levels',
          key: 'capability_levels',
          parse: (capability_levels) => this.parseFlatList(capability_levels, 'capabilityLevels'),
        },
        {
          id: '14',
          label: 'Capability Categories',
          key: 'capability_categories',
          parse: (capability_categories) => this.parseFlatList(capability_categories, 'capabilityCategories'),
        },
        {
          id: '15',
          label: 'Capability Subcategories',
          key: 'capability_subcategories',
          parse: (capability_subcategories) => this.parseFlatList(capability_subcategories, 'capabilitySubcategories'),
        },
        {
          id: '18',
          label: 'Multicountry or Regional Office',
          key: 'regional_office',
          parse: (regional_office) => this.parseList(this.getRegionalOffices, [regional_office]),
        },
        // {
        //   id: '19',
        //   label: 'UNICEF Sector',
        //   key: 'unicef_sector',
        //   parse: (unicef_sector) =>
        //     this.parseList(this.getSectors, unicef_sector),
        // },
        {
          id: '64',
          label: 'Lead Sector',
          key: 'unicef_leading_sector',
          parse: (unicef_leading_sector) => this.parseList(this.getLeadingSector, unicef_leading_sector),
        },
        {
          id: '65',
          label: 'Supporting Sectors',
          key: 'unicef_supporting_sectors',
          parse: (unicef_supporting_sectors) => this.parseList(this.getSupportingSectors, unicef_supporting_sectors),
        },
        {
          id: '20',
          label: 'Innovation Ways',
          key: 'innovation_ways',
          parse: (innovation_ways) => this.parseList(this.getInnovationWays, innovation_ways),
        },
        {
          id: '17',
          label: 'Innovation Categories',
          key: 'innovation_categories',
          parse: (innovation_categories) => this.parseList(this.getInnovationCategories, innovation_categories),
        },
        {
          id: '21',
          label: 'Completed phases',
          key: 'stages',
          parse: (stages) => this.parseListWithObjects(this.getStages, stages),
        },
        {
          id: '63',
          label: 'Current phase',
          key: 'current_phase',
          parse: (phaseId) => this.parseSingleSelection(phaseId, 'getStages'),
        },
        {
          id: '22',
          label: 'Hardware platform(s)',
          key: 'hardware',
          parse: (hardware) => this.parseList(this.getHardware, hardware),
        },
        {
          id: '23',
          label: 'Non-technology platform(s)',
          key: 'nontech',
          parse: (nontech) => this.parseList(this.getNontech, nontech),
        },
        {
          id: '24',
          label: 'Platform/Product Function',
          key: 'functions',
          parse: (functions) => this.parseList(this.getFunctions, functions),
        },
        {
          id: '25',
          label: 'Information security classification',
          key: 'isc',
          parse: (isc) => this.parseList(this.getInfoSec, [isc]),
        },
        {
          id: '26',
          label: 'Regional priority(ies)',
          key: 'regional_priorities',
          parse: (regional_priorities) => this.parseList(this.getRegionalPriorities, regional_priorities),
        },
        // { id: '27', label: 'Programme Focal Point Email' },
        {
          id: '28',
          label: 'Annual Work Plan (AWP) Outcome/Activity',
          key: 'awp',
          parse: (awp) => awp || '',
        },
        {
          id: '29',
          label: 'Currency',
          key: 'currency',
          parse: (currency) => currency || '',
        },
        {
          id: '30',
          label: 'Current Achievements',
          key: 'current_achievements',
          parse: (current_achievements) => current_achievements || '',
        },
        {
          id: '31',
          label: 'Funding Needs',
          key: 'funding_needs',
          parse: (funding_needs) => funding_needs || '',
        },
        {
          id: '32',
          label: 'In Country programme document (CPD) and annual work plan?',
          key: 'cpd',
          parse: (cpd) => this.joinSimpleArr(cpd),
        },
        {
          id: '33',
          label: 'Links to website/Current Documentation + URL',
          key: 'links',
          parse: (links) => this.joinSimpleArr(links),
        },
        {
          id: '34',
          label: 'Overview',
          key: 'overview',
          parse: (overview) => overview,
        },
        {
          id: '35',
          label: 'Partner Data',
          key: 'partners',
          parse: (links) => this.joinSimpleArr(links),
        },
        {
          id: '36',
          label: 'Partnership needs',
          key: 'partnership_needs',
          parse: (partnership_needs) => partnership_needs || '',
        },
        {
          id: '37',
          label: 'Program Targets',
          key: 'program_targets',
          parse: (program_targets) => program_targets || '',
        },
        {
          id: '38',
          label: 'Program Targets Archieved',
          key: 'program_targets_achieved',
          parse: (program_targets_achieved) => program_targets_achieved || '',
        },
        {
          id: '39',
          label: 'Start Date',
          key: 'start_date',
          parse: (start_date) => start_date || '',
        },
        {
          id: '40',
          label: 'End Date',
          key: 'end_date',
          parse: (end_date) => end_date || '',
        },
        {
          id: '41',
          label: 'Target Group (Target Population) Reached',
          key: 'target_group_reached',
          parse: (target_group_reached) => target_group_reached || '',
        },
        {
          id: '42',
          label: 'Total Budget',
          key: 'total_budget',
          parse: (total_budget) => total_budget || '',
        },
        {
          id: '43',
          label: 'Total Budget (Narrative)',
          key: 'total_budget_narrative',
          parse: (total_budget_narrative) => total_budget_narrative || '',
        },
        {
          id: '44',
          label: 'Work Breakdown Structure (WBS)',
          key: 'wbs',
          parse: (wbs) => this.joinSimpleArr(wbs),
        },
        {
          id: '60',
          label: 'Software Platforms(s)',
          key: 'platforms',
          parse: (platforms) => this.parseFlatList(platforms, 'platforms'),
        },
        {
          id: '62',
          label: 'Scoring',
          key: 'review_states',
          parse: (review_states) => this.parseReviewState(review_states),
        },
        {
          id: '61',
          label: 'Questionnaires Assigned',
          key: 'review_states',
          parse: (review_scores) => this.parseReviews(review_scores),
        },
      ],
    }
  },
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
      mapColKeys: (state) => state.dashboard.mapColKeys,
      scalePhases: (state) => state.system.scalePhases,
      portfolioPage: (state) => state.search.filter.portfolio_page,
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
      review_statuses: 'system/getReviewStatuses',
      // new fields
      getSectors: 'projects/getSectors',
      getLeadingSector: 'projects/getLeadingSector',
      getSupportingSectors: 'projects/getSupportingSectors',
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
    parsedScores() {
      if (
        (!this.projects || !this.projects[0] || typeof this.projects !== 'object') &&
        this.projects[0]?.review_states
      ) {
        return null
      }
      const parsed = []
      const exportCols = []

      // create header row
      let row = []
      this.colKeyValues.forEach((i) => {
        if (this.selectedCol.includes(i.id)) {
          if (i.id !== '61' && i.id !== '62') {
            row.push(this.$gettext(i.label))
          }
          exportCols.push(i)
        }
      })
      if (this.portfolioPage !== 'inventory' && this.projects[0]?.review_states) {
        // official score header
        if (this.selectedCol.includes('62')) {
          row.push(...['', ...this.officialScoreFields])
        }
        if (this.selectedCol.includes('61')) {
          // get the max of reviews per project, then generate header for each one of them
          const maxReviewColGroups = this.projects.reduce((maxGroup, p) => {
            return p.review_states.review_scores.length > maxGroup ? p.review_states.review_scores.length : maxGroup
          }, 0)
          for (let i = 0; i < maxReviewColGroups; i++) {
            row.push(...['', ...this.reviewScoresFields])
          }
        }
      }
      parsed.push(row)

      let cell
      this.projects.forEach((p) => {
        row = []
        exportCols.forEach((col) => {
          if (p[col.key] && col.id !== '61') {
            cell = col.parse(p[col.key])
            if (Array.isArray(cell)) {
              row.push(...cell)
            } else {
              row.push(cell)
            }
          } else if (col.id !== '61') {
            row.push('')
          }
        })

        // generate reviews
        if (this.portfolioPage !== 'inventory' && this.selectedCol.includes('61') && this.projects[0]?.review_states) {
          row.push(...this.parseReviews(p.review_states.review_scores))
        }

        parsed.push(row)
      })

      return parsed
    },
    parsed() {
      if (!this.projects || !this.projects[0] || typeof this.projects !== 'object') {
        return null
      }
      return this.projects.map((s) => {
        const parsed = {
          ...s,
          country: this.parseCountry(s.country),
          country_office: s.country_office ? this.offices.find((obj) => obj.id === s.country_office).name || '' : '',
          // investors: this.parseDonors(s.donors),
          health_focus_areas: this.parseHealthFocusAreas(s.health_focus_areas),
          hsc_challenges: this.parseHscChallenges(s.hsc_challenges),
          capability_levels: this.parseFlatList(s.capability_levels, 'capabilityLevels'),
          capability_categories: this.parseFlatList(s.capability_categories, 'capabilityCategories'),
          capability_subcategories: this.parseFlatList(s.capability_subcategories, 'capabilitySubcategories'),
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
          regional_office: this.parseList(this.getRegionalOffices, [s.regional_office]),
          unicef_sector: this.parseList(this.getSectors, s.unicef_sector),
          unicef_leading_sector: this.parseList(this.getLeadingSector, s.unicef_leading_sector),
          unicef_supporting_sectors: this.parseList(this.getSupportingSectors, s.unicef_supporting_sectors),
          innovation_ways: this.parseList(this.getInnovationWays, s.innovation_ways),
          innovation_categories: this.parseList(this.getInnovationCategories, s.innovation_categories),
          stages: this.parseListWithObjects(this.getStages, s.stages),
          current_phase: this.parseSingleSelection(s.current_phase, 'getStages'),
          hardware: this.parseList(this.getHardware, s.hardware),
          nontech: this.parseList(this.getNontech, s.nontech),
          functions: this.parseList(this.getFunctions, s.functions),
          isc: this.parseList(this.getInfoSec, [s.isc]),
          regional_priorities: this.parseList(this.getRegionalPriorities, s.regional_priorities),
          wbs: this.joinSimpleArr(s.wbs),
          partners: this.joinSimpleArr(s.partners),
          cpd: this.joinSimpleArr(s.cpd),
          links: this.joinSimpleArr(s.links),
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
    async getProblemStatements() {
      try {
        const { data } = await this.$axios.get('api/problem-statement/')
        this.problemStatements = [...data]
      } catch (e) {
        console.error(e)
      }
    },
    parseBoolean(value) {
      return value ? this.$gettext('yes') : this.$gettext('no')
    },
    parseFlatList(flatList, type) {
      if (typeof flatList === 'object') {
        const all = typeof this[type] === 'function' ? this[type]() : this[type]
        return all
          .filter((cb) => flatList.includes(cb.id))
          .map((cb) => cb.name)
          .join(',')
      }
      return ''
    },
    parseListWithObjects(list, filter) {
      if (typeof filter === 'object' || Array.isArray(filter)) {
        const filterIDs = filter.map((item) => item.id)
        return list
          .filter((tp) => filterIDs.includes(tp.id))
          .map((i) => i.name)
          .join(', ')
      }
      return ''
    },
    parseList(list, filter) {
      if (typeof filter === 'object') {
        return list
          .filter((tp) => filter.includes(tp.id))
          .map((i) => i.name)
          .join(', ')
      }
      return ''
    },
    joinSimpleArr(arr) {
      return arr ? arr.join(', ') : ''
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
      if (typeof values === 'object') {
        return this.hscChallenges
          .reduce((a, c) => {
            c.challenges.forEach((cc) => {
              if (values && values.includes(cc.id)) {
                a.push(cc.challenge)
              }
            })
            return a
          }, [])
          .join(',')
      }
      return ''
    },
    parseHealthFocusAreas(health_focus_areas) {
      if (typeof health_focus_areas === 'object') {
        return this.getHealthFocusAreas
          .filter((hfa) => hfa.health_focus_areas.some((h) => health_focus_areas.includes(h.id)))
          .map((hf) => hf.name)
          .join(',')
      }
      return ''
    },
    parseCustomQuestions(donor_answers, country_answers) {
      let custom = {}
      if (this.dashboardType === 'donor') {
        try {
          this.donorColumns.forEach((dc) => {
            const value = donor_answers && donor_answers[dc.donorId] ? donor_answers[dc.donorId][dc.originalId] : ''
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
    parseReviewState(projectReviewState) {
      const scores = [''] // to make a gap
      scores.push(this.parseList(this.problemStatements, projectReviewState.psa))
      scores.push(projectReviewState.rnci || '')
      scores.push(projectReviewState.ratp || '')
      scores.push(projectReviewState.ra || '')
      scores.push(projectReviewState.ee || '')
      scores.push(projectReviewState.nst || '')
      scores.push(projectReviewState.nc || '')
      scores.push(projectReviewState.ps || '')
      scores.push(projectReviewState.overall_reviewer_feedback || '')
      scores.push(projectReviewState.impact || '')
      scores.push(this.parseSingleSelection(projectReviewState.scale_phase, 'scalePhases'))
      return scores
    },
    parseReviews(projectReviews) {
      const reviews = []
      projectReviews.forEach((review) => {
        reviews.push('')
        reviews.push(review.reviewer.name || '')
        reviews.push(this.review_statuses[review.status])
        reviews.push(this.parseList(this.scalePhases, review.psa))
        reviews.push(review.reviewer.psa_comment || '')
        reviews.push(review.rnci || '')
        reviews.push(review.rnci_comment || '')
        reviews.push(review.ratp || '')
        reviews.push(review.ratp_comment || '')
        reviews.push(review.ra || '')
        reviews.push(review.ra_comment || '')
        reviews.push(review.ee || '')
        reviews.push(review.ee_comment || '')
        reviews.push(review.nst || '')
        reviews.push(review.nst_comment || '')
        reviews.push(review.nc || '')
        reviews.push(review.nc_comment || '')
        reviews.push(review.ps || '')
        reviews.push(review.ps_comment || '')
        reviews.push(review.overall_reviewer_feedback || '')
      })
      return reviews
    },
  },
  render() {
    if (this.problemStatements.length === 0) {
      this.getProblemStatements()
    }
    return this.$scopedSlots.default({
      parsed: this.parsed,
      parsedScores: this.parsedScores,
    })
  },
}
</script>

<style></style>
