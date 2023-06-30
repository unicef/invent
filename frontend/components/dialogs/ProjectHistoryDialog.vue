<template>
  <el-dialog :visible.sync="visible" top="30vh" width="800px" @opened="showTimeline = true">
    <template v-if="projectHistory" #title>
      <div class="header">
        <div class="title">
          <translate :parameters="{ title: projectHistory.title }"> History of ’{title}’ </translate>
        </div>
        <div class="status">
          <StatusBadge :status="projectHistory.status" large />
          <translate
            v-if="projectHistory.teamMember"
            key="team"
            :parameters="{ currentVersion: projectHistory.currentVersion, changed: projectHistory.changed }"
            class="change"
          >
            Version {currentVersion} on {changed}
          </translate>
          <translate v-else key="viewer" :parameters="{ changed: projectHistory.changed }" class="change">
            on {changed}
          </translate>
        </div>
      </div>
    </template>
    <Timeline v-if="showTimeline">
      <component
        :is="version.component"
        v-for="(version, index) in projectHistory.versions"
        :key="version.version"
        :version="version"
        :team-member="projectHistory.teamMember"
        :stack="timelineStack(index)"
      />
    </Timeline>
    <div v-else class="skeleton-wrapper">
      <div class="event skeleton"></div>
      <div class="avatar skeleton"></div>
      <div class="changes skeleton"></div>
    </div>
  </el-dialog>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import { format } from 'date-fns'
import Timeline from '@/components/project/history/Timeline'
import StatusBadge from '@/components/project/history/StatusBadge'
import TimelineItem from '@/components/project/history/TimelineItem'
import TimelineItemNoData from '@/components/project/history/TimelineItemNoData'

export default {
  components: {
    Timeline,
    StatusBadge,
    TimelineItem,
    TimelineItemNoData,
  },
  loading: false,
  data() {
    return {
      visible: false,
      showTimeline: false,
      projectHistory: {},
      fieldMap: {
        organisation: undefined,
        donors: undefined,
        donor_answers: undefined,
        country_answers: undefined,
        name: {
          component: 'ValueText',
          title: this.$gettext('Initiative mame'),
          parse: (name) => name || '',
        },
        country: {
          component: 'ValueText',
          title: this.$gettext('Country'),
          parse: (countryId) => this.parseCountry(countryId),
        },
        country_office: {
          component: 'ValueText',
          title: this.$gettext('UNICEF Office'),
          parse: (officeId) => (officeId ? this.parseCountryOffice(officeId) : ''),
        },
        regional_office: {
          component: 'ValueTags',
          title: this.$gettext('Multicountry or Regional Office'),
          parse: (regional_office) => this.parseList(this.getRegionalOffices, [regional_office]),
        },
        modified: {
          component: 'ValueText',
          title: this.$gettext('Last updated'),
          parse: (modified) => this.parseDate(modified),
        },
        implementation_overview: {
          component: 'ValueText',
          title: this.$gettext('Narrative of the initiative'),
          parse: (implementation_overview) => implementation_overview || '',
        },
        research: {
          component: 'ValueText',
          title: this.$gettext('title'),
          parse: (research) => research || '',
        },
        start_date: {
          component: 'ValueText',
          title: this.$gettext('Start date'),
          parse: (startDate) => this.parseDate(startDate),
        },
        end_date: {
          component: 'ValueText',
          title: this.$gettext('End date'),
          parse: (endDate) => this.parseDate(endDate),
        },
        end_date_note: {
          component: 'ValueText',
          title: this.$gettext('Note'),
          parse: (endNote) => endNote || '',
        },
        contact_name: {
          component: 'ValueText',
          title: this.$gettext('Contact name'),
          parse: (contactName) => contactName || '',
        },
        contact_email: {
          component: 'ValueText',
          title: this.$gettext('Contact email'),
          parse: (contactEmail) => contactEmail || '',
        },
        team: {
          component: 'ValueText',
          title: this.$gettext('Team members'),
          parse: (contactEmail) => contactEmail || '',
        },
        viewers: {
          component: 'ValueText',
          title: this.$gettext('INVENT country focal points'),
          parse: (viewers) => viewers || '',
        },
        goal_area: {
          component: 'ValueText',
          title: this.$gettext('Goal Area'),
          parse: (goal_area) => this.parseSingleSelection(goal_area, 'goalAreas'),
        },
        result_area: {
          component: 'ValueText',
          title: this.$gettext('Result Area'),
          parse: (resultArea) => this.parseSingleSelection(resultArea, 'resultAreas'),
        },
        capability_levels: {
          component: 'ValueTags',
          title: this.$gettext('Capability Levels'),
          parse: (capabilityLevels) => this.parseFlatList(capabilityLevels, 'capabilityLevels'),
        },
        capability_categories: {
          component: 'ValueTags',
          title: this.$gettext('Capability Categories'),
          parse: (capabilityCategories) => this.parseFlatList(capabilityCategories, 'capabilityCategories'),
        },
        capability_subcategories: {
          component: 'ValueTags',
          title: this.$gettext('Capability Subcategories'),
          parse: (capabilitySubCategories) => this.parseFlatList(capabilitySubCategories, 'capabilitySubcategories'),
        },
        platforms: {
          component: 'ValueTags',
          title: this.$gettext('Software Platforms(s)'),
          parse: (platforms) => this.parseFlatList(platforms, 'platforms'),
        },
        dhis: {
          component: 'ValueTags',
          title: this.$gettext('Digital Health Intervention(s)'),
          parse: (dhis) => this.parseDHIList(dhis),
        },
        health_focus_areas: {
          component: 'ValueTags',
          title: this.$gettext('Programme Focus Area(s)'),
          parse: (hfa) => this.parseTwoLevelList(this.getHealthFocusAreas, 'health_focus_areas', hfa),
        },
        hsc_challenges: {
          component: 'ValueTags',
          title: this.$gettext('System challenge(s)'),
          parse: (hsc) => this.parseTwoLevelList(this.hscChallenges, 'challenges', hsc),
        },
        unicef_sector: {
          component: 'ValueTags',
          title: this.$gettext('Sector'),
          parse: (unicef_sector) => this.parseList(this.getSectors, unicef_sector),
        },
        unicef_leading_sector: {
          component: 'ValueTags',
          title: this.$gettext('Lead Sector'),
          parse: (unicef_leading_sector) => this.parseList(this.getLeadingSectors, unicef_leading_sector),
        },
        unicef_suppoting_sectors: {
          component: 'ValueTags',
          title: this.$gettext('Supporting Sectors'),
          parse: (unicef_supporting_sectors) => this.parseList(this.getSupportingSectors, unicef_supporting_sectors),
        },
        functions: {
          component: 'ValueTags',
          title: this.$gettext('Platform/Product Function'),
          parse: (functions) => this.parseList(this.getFunctions, functions),
        },
        hardware: {
          component: 'ValueTags',
          title: this.$gettext('Hardware platform(s)'),
          parse: (hardware) => this.parseList(this.getHardware, hardware),
        },
        nontech: {
          component: 'ValueTags',
          title: this.$gettext('Non-technology platform(s)'),
          parse: (nontech) => this.parseList(this.getNontech, nontech),
        },
        regional_priorities: {
          component: 'ValueTags',
          title: this.$gettext('Regional priorities'),
          parse: (regional_priorities) => this.parseList(this.getRegionalPriorities, regional_priorities),
        },
        wbs: {
          component: 'ValueText',
          title: this.$gettext('Work Breakdown Structure (WBS)'),
          parse: (wbs) => this.joinSimpleArr(wbs),
        },
        innovation_categories: {
          component: 'ValueTags',
          title: this.$gettext('Innovation Categories'),
          parse: (innovation_categories) => this.parseList(this.getInnovationCategories, innovation_categories),
        },
        cpd: {
          component: 'ValueTags',
          title: this.$gettext('Country Programme Document inclusion'),
          parse: (cpd) => this.parseList(this.getCpd, cpd),
        },
        partners: {
          component: 'ValueSpecial', // should be 'ValuePartners'
          title: this.$gettext('Partners'),
          parse: () => this.$gettext('Partner list has been changed'),
        },
        links: {
          component: 'ValueSpecial', // should be 'ValueTags'
          title: this.$gettext('Links to website/Current Documentation'),
          parse: () => this.$gettext('Link list has been changed.'),
        },
        overview: {
          component: 'ValueText',
          title: this.$gettext('Overview of the initiative'),
          parse: (overview) => overview || '',
        },
        coverImage: {
          component: 'ValueSpecial',
          title: this.$gettext('Cover image'),
          parse: () => this.$gettext('Cover image has been changed'),
        },
        program_targets: {
          component: 'ValueText',
          title: this.$gettext('Program targets'),
          parse: (program_targets) => program_targets || '',
        },
        program_targets_achieved: {
          component: 'ValueText',
          title: this.$gettext('Program Targets Archieved'),
          parse: (program_targets_achieved) => program_targets_achieved || '',
        },
        current_achievements: {
          component: 'ValueText',
          title: this.$gettext('Initiative achievements'),
          parse: (current_achievements) => current_achievements || '',
        },
        awp: {
          component: 'ValueText',
          title: this.$gettext('Annual Work Plan (AWP) Outcome/Activity'),
          parse: (awp) => awp || '',
        },
        funding_needs: {
          component: 'ValueText',
          title: this.$gettext('Funding Needs'),
          parse: (funding_needs) => funding_needs || '',
        },
        partnership_needs: {
          component: 'ValueText',
          title: this.$gettext('Partnership needs'),
          parse: (partnership_needs) => partnership_needs || '',
        },
        target_group_reached: {
          component: 'ValueText',
          title: this.$gettext('Target Group (Target Population) Reached'),
          parse: (target_group_reached) => (target_group_reached === null ? '' : target_group_reached),
        },
        currency: {
          component: 'ValueText',
          title: this.$gettext('Currency'),
          parse: (currencyId) => this.parseCurrency(currencyId),
        },
        total_budget: {
          component: 'ValueText',
          title: this.$gettext('Total Budget'),
          parse: (total_budget) => (total_budget === null ? '' : total_budget),
        },
        total_budget_narrative: {
          component: 'ValueText',
          title: this.$gettext('Total Budget (Narrative)'),
          parse: (total_budget_narrative) => total_budget_narrative || '',
        },
        innovation_ways: {
          component: 'ValueTags',
          title: this.$gettext('Innovation Ways'),
          parse: (innovation_ways) => this.parseList(this.getInnovationWays, innovation_ways),
        },
        isc: {
          component: 'ValueTags',
          title: this.$gettext('Information security classification'),
          parse: (isc) => this.parseList(this.getInfoSec, [isc]),
        },
        stages: {
          component: 'ValueSpecial', // should be 'ValuePhases'
          title: this.$gettext('Completed phases'),
          parse: () => this.$gettext('Completed phases have been changed.'),
        },
        current_phase: {
          component: 'ValueText',
          title: this.$gettext('Current phase'),
          parse: (phaseId) => this.parseSingleSelection(phaseId, 'getStages'),
        },
        country_custom_answers: {
          component: 'ValueSpecial',
          title: this.$gettext('Country custom answers'),
          parse: () => this.$gettext('Custom answers have been changed.'),
        },
      },
    }
  },
  computed: {
    ...mapState({
      systemDicts: (state) => state,
      offices: (state) => state.offices.offices,
      scalePhases: (state) => state.system.scalePhases,
      projectDicts: (state) => state.projects.projectStructure,
    }),
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      getHealthFocusAreas: 'projects/getHealthFocusAreas',
      goalAreas: 'projects/getGoalAreas',
      resultAreas: 'projects/getResultAreas',
      capabilityLevels: 'projects/getCapabilityLevels',
      capabilityCategories: 'projects/getCapabilityCategories',
      capabilitySubcategories: 'projects/getCapabilitySubcategories',
      regions: 'system/getUnicefRegions',
      platforms: 'projects/getTechnologyPlatforms',
      hscChallenges: 'projects/getHscChallenges',
      currencies: 'projects/getCurrencies',
      getCpd: 'projects/getCpd',
      // new fields
      getSectors: 'projects/getSectors',
      getRegionalPriorities: 'projects/getRegionalPriorities',
      getInnovationWays: 'projects/getInnovationWays',
      getInnovationCategories: 'projects/getInnovationCategories',
      getStages: 'projects/getStages',
      getHardware: 'projects/getHardware',
      getNontech: 'projects/getNontech',
      getFunctions: 'projects/getFunctions',
      dhis: 'projects/getDigitalHealthInterventions',
      getDHIDetails: 'projects/getDigitalHealthInterventionDetails',
      // single new field
      getRegionalOffices: 'projects/getRegionalOffices',
      getInfoSec: 'projects/getInfoSec',
    }),
  },
  mounted() {
    if (this.offices.length === 0) {
      this.loadOffices()
    }
  },
  methods: {
    ...mapActions({
      loadOffices: 'offices/loadOffices',
    }),
    open(project) {
      this.getProjectHistory(project)
      this.visible = true
    },
    timelineStack(row) {
      return {
        row,
        rows: this.projectHistory.versions.length,
      }
    },
    async getProjectHistory(project) {
      const { data: versionHistoryRaw } = await this.$axios.get(`/api/projects/${project.id}/version-history`)

      // Prepare version changes field by field
      if (versionHistoryRaw.length > 0) {
        const versions = versionHistoryRaw.map((v) => {
          const cleanedChanges = v.changes.filter((ch) => {
            return this.fieldMap[ch.field] !== undefined
          })
          return {
            component: 'TimelineItem',
            status: v.published ? 'published' : v.was_unpublished ? 'unpublished' : 'draft',
            version: v.version,
            changed: v.modified ? format(new Date(v.modified), 'DD/MM/YYYY') : '',
            user: v.user,
            changes: cleanedChanges.map((ch, i) => {
              return {
                component: this.fieldMap[ch.field].component,
                field: ch.field,
                fieldTitle: this.fieldMap[ch.field].title,
                key: i,
                values: this.parseChanges(ch),
              }
            }),
          }
        })

        // Check and prepare beyond history edge case
        versions[0].beyond_history = false
        if (versionHistoryRaw[0].beyond_history) {
          const beyondHistory = [
            {
              component: 'TimelineItem',
              status: 'created',
              version: -2,
              changed: format(new Date(project.created), 'DD/MM/YYYY'),
              user: null,
              changes: [],
            },
            {
              component: 'TimelineItemNoData',
              status: 'empty',
              version: -1,
              changed: '',
              user: null,
              changes: [],
            },
            {
              component: 'TimelineItem',
              status: versionHistoryRaw[0].published ? 'noversionPublished' : 'noversionDraft',
              version: 0,
              changed: versions[0].changed,
              user: null,
              changes: [],
            },
          ]
          versions.push(...beyondHistory)
        }

        // Calculate current version
        let publishedOrUnpublished = false
        const latestVersionIndex = versionHistoryRaw.length - 1
        let pIndex = latestVersionIndex
        while (!publishedOrUnpublished && pIndex >= 0) {
          publishedOrUnpublished = versionHistoryRaw[pIndex].published || versionHistoryRaw[pIndex].was_unpublished
          if (!publishedOrUnpublished) pIndex--
        }
        const status = publishedOrUnpublished && versionHistoryRaw[pIndex].published ? 'published' : 'draft'
        const currentVersion = {
          status,
          currentVersion:
            status === 'published' ? versionHistoryRaw[pIndex].version : versionHistoryRaw[latestVersionIndex].version,
          changed:
            status === 'published'
              ? format(new Date(versionHistoryRaw[pIndex].modified), 'DD/MM/YYYY')
              : format(new Date(versionHistoryRaw[latestVersionIndex].modified), 'DD/MM/YYYY'),
        }

        // return prepared data
        this.projectHistory = {
          ...project,
          ...currentVersion,
          versions: versions.sort((a, b) => b.version - a.version),
        }
      } else {
        this.projectHistory = {}
      }
    },
    parseChanges(change) {
      try {
        if (change.special) {
          return {
            changeType: 'edit',
            changeTypeIcon: 'el-icon-edit',
            value: this.fieldMap[change.field].parse(),
          }
        }
        const added = {
          changeType: 'new',
          changeTypeIcon: 'el-icon-circle-plus-outline',
          value: this.fieldMap[change.field].parse(change.added),
        }
        const removed = {
          changeType: 'old',
          changeTypeIcon: 'el-icon-remove-outline',
          value: this.fieldMap[change.field].parse(change.removed),
        }
        return { added, removed }
      } catch (error) {
        console.error('🚀 ~ parseChanges ~ error', error)
      }
    },
    parseDate(value) {
      return value ? format(new Date(value), 'DD/MM/YYYY') : ''
    },
    parseFlatList(flatList, type) {
      if (typeof flatList === 'object' && flatList !== null) {
        const all = typeof this[type] === 'function' ? this[type]() : this[type]
        return all.filter((cb) => flatList.includes(cb.id)).map((cb) => cb.name)
      }
      return []
    },
    parseListWithObjects(list, filter) {
      if (filter == null) return ''
      if (typeof filter === 'object' || Array.isArray(filter)) {
        const filterIDs = filter.map((item) => item.id)
        return list.filter((tp) => filterIDs.includes(tp.id)).map((i) => i.name)
      }
      return []
    },
    parseCurrency(id) {
      if (id === null) return ''
      const currency = this.currencies.find((c) => c.id === id)
      return currency ? `${currency.name} (${currency.code})` : ''
    },
    parseList(list, filter) {
      if (typeof filter === 'object' && filter !== null) {
        return list.filter((tp) => filter.includes(tp.id)).map((i) => i.name)
      }
      return []
    },
    parseDHIList(filter) {
      if (filter === null) return []
      return filter.map((dhiId) => this.getDHIDetails(dhiId).name)
    },
    joinSimpleArr(arr) {
      if (arr === null) return ''
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
    parseCountryOffice(officeId) {
      const office = this.offices.find((obj) => obj.id === officeId)
      return office && office.name ? office.name : ''
    },
    parseTwoLevelList(list, secondListName, filter) {
      if (filter === null) return []
      const changedTags = list.reduce((tags, obj) => {
        obj[secondListName].filter((h) => filter.includes(h.id)).forEach((h) => tags.push(h.name))
        return tags
      }, [])
      return changedTags
    },
    parseCustomAnswers(answers) {
      if (Object.keys(answers).length > 0) {
        const joinedAnswers = Object.keys(answers).map((a) => {
          return answers[a]
        })
        return joinedAnswers.join(', ')
      }
      return 'empty'
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

::v-deep .el-dialog {
  margin: 50px auto 50px !important;
}

::v-deep .el-dialog .el-dialog__header .el-dialog__headerbtn {
  top: 30px;
}

::v-deep .el-dialog .el-dialog__body {
  padding: 0;
  overflow-y: auto;
  max-height: calc(100vh - 228px);
}

.header {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 14px 0;
  .title {
    font-size: 20px;
    line-height: 32px;
    color: #1cace3;
  }
  .status {
    display: flex;
    align-items: center;
    gap: 10px;
    .change {
      font-size: 14px;
      font-weight: normal;
      line-height: 20px;
      color: @colorTextMuted;
    }
  }
}

.skeleton-wrapper {
  display: flex;
  gap: 8px;
  padding: 1em;
  .event {
    width: 128px;
    height: 128px;
  }
  .avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
  }
  .changes {
    flex: 1;
    height: 128px;
  }

  .skeleton {
    background-image: linear-gradient(
      90deg,
      #eeeeee 0%,
      #eeeeee 40%,
      #dddddd 50%,
      #dddddd 55%,
      #eeeeee 65%,
      #eeeeee 100%
    );
    background-size: 400%;
    animation: shimmer 1500ms infinite;
  }
  @keyframes shimmer {
    from {
      background-position: 100% 100%;
    }
    to {
      background-position: 0 0;
    }
  }
}
</style>
