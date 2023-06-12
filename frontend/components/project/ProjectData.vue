<template>
  <div class="ProjectData">
    <el-row type="flex">
      <el-col :span="18">
        <collapsible-card id="general" :title="$gettext('1. General Overview') | translate">
          <simple-field :content="project.name" :header="$gettext('Initiative Name') | translate" />

          <simple-field :header="$gettext('UNICEF Office') | translate" :content="location" />

          <simple-field :content="project.overview" :header="$gettext('Overview of the initiative') | translate" />

          <simple-field
            v-if="project.implementation_overview"
            :content="project.implementation_overview"
            :header="$gettext('Narrative of the initiative') | translate"
          />

          <el-row>
            <el-col :span="12">
              <simple-field :content="getUserName" :header="$gettext('Contact name') | translate" />
            </el-col>
            <el-col :span="12">
              <simple-field :content="project.contact_email" :header="$gettext('Contact email') | translate" />
            </el-col>
          </el-row>

          <el-row class="GrayArea">
            <el-col :span="12">
              <simple-field :header="$gettext('Team members') | translate">
                <team-list :value="project.team" />
              </simple-field>
            </el-col>
            <el-col :span="12">
              <simple-field v-if="isEmptyArr(project.viewers)" :header="$gettext('Viewers') | translate">
                <team-list :value="project.viewers" />
              </simple-field>
            </el-col>
          </el-row>

          <simple-field
            v-if="countryManagers.length > 0"
            :header="$gettext('INVENT country focal point(s)') | translate"
          >
            <ul class="ma-0">
              <li v-for="manager in countryManagers" :key="manager.id">{{ manager.name }} ({{ manager.email }})</li>
            </ul>
          </simple-field>

          <simple-field :header="$gettext('Last Updated') | translate" :content="lastUpdated" />
        </collapsible-card>

        <collapsible-card id="categorization" :title="$gettext('2. Categorization') | translate">
          <simple-field
            v-if="project.unicef_leading_sector.length > 0"
            :header="$gettext('Lead Sector') | translate"
            :content="getLeadingSector"
          />

          <simple-field
            v-if="project.unicef_supporting_sectors.length > 0"
            :header="$gettext('Supporting Sector(s)') | translate"
          >
            <platforms-list :platforms="project.unicef_supporting_sectors" source="getSectors" />
          </simple-field>

          <simple-field :header="$gettext('Goal Area') | translate" :content="goalArea.name" />

          <simple-field
            v-if="resultArea.name"
            :header="$gettext('Result Area') | translate"
            :content="resultArea.name"
          />

          <template v-if="goalArea && goalArea.id && goalArea.id === 1">
            <simple-field :header="$gettext('Digital Health Intervention(s)') | translate">
              <DhiList :values="project.dhis" />
            </simple-field>

            <simple-field :header="$gettext('Programme Focus Area(s)') | translate">
              <health-focus-areas-list :value="project.health_focus_areas" />
            </simple-field>

            <simple-field :header="$gettext('System challenge(s)') | translate">
              <health-system-challenges-list :value="project.hsc_challenges" />
            </simple-field>
          </template>

          <template v-else-if="goalArea && goalArea.id && goalArea.capability_level_question !== 'MISSING'">
            <simple-field :header="goalArea.capability_level_question">
              <CapabilitiesList
                :value="project.capability_levels"
                :goal-area="goalArea.id"
                :values-function="getCapabilityLevels"
              />
            </simple-field>
            <simple-field :header="goalArea.capability_category_question">
              <CapabilitiesList
                :value="project.capability_categories"
                :goal-area="goalArea.id"
                :values-function="getCapabilityCategories"
              />
            </simple-field>
            <simple-field :header="goalArea.capability_subcategory_question">
              <CapabilitiesList
                :value="project.capability_subcategories"
                :goal-area="goalArea.id"
                :values-function="getCapabilitySubcategories"
              />
            </simple-field>
          </template>

          <simple-field
            v-if="isEmptyArr(project.regional_priorities)"
            :header="$gettext('Regional priority(ies)') | translate"
          >
            <platforms-list :platforms="project.regional_priorities" source="getRegionalPriorities" />
          </simple-field>

          <simple-field v-if="isEmptyArr(project.innovation_ways)" :header="$gettext('Innovation(s)') | translate">
            <platforms-list :platforms="project.innovation_ways" source="getInnovationWays" />
          </simple-field>

          <simple-field
            v-if="isEmptyArr(project.innovation_categories)"
            :header="$gettext('Innovation category(ies)') | translate"
          >
            <platforms-list :platforms="project.innovation_categories" source="getInnovationCategories" />
          </simple-field>
        </collapsible-card>

        <collapsible-card id="implementation" :title="$gettext('3. Implementation Overview') | translate">
          <template v-if="showOverview(project, orderedLinkList)">
            <template v-for="field in overviewFields">
              <simple-field
                v-if="['cpd', 'wbs'].includes(field.type) ? isEmptyArr(project[field.type]) : project[field.type]"
                :key="field.type"
                :content="['cpd', 'wbs', 'total_budget'].includes(field.type) ? null : project[field.type]"
                :header="field.header"
              >
                <template v-if="field.type === 'cpd'">
                  <platforms-list :platforms="project.cpd" source="getCpd" />
                </template>
                <template v-if="field.type === 'wbs'">
                  <ul>
                    <li v-for="(wbs, i) in project.wbs" :key="`${wbs}${i}`">
                      <span>{{ wbs }}</span>
                    </li>
                  </ul>
                </template>
                <template v-if="field.type === 'total_budget'">
                  {{ project.total_budget | formatNumber }}
                  <list-element v-if="project.total_budget" :value="project.currency" source="getCurrencies" />
                </template>
              </simple-field>
            </template>
            <simple-field
              v-for="{ link_url, link_type } in orderedLinkList"
              :key="'link_type' + link_type"
              :content="link_url"
              :header="getLinkHeader(link_type)"
              link
            />
          </template>
          <template v-else>
            <!-- <translate>
              There's no implemantation overview for the initiative.
            </translate> -->
          </template>
        </collapsible-card>

        <!-- stage graph -->
        <stage-history />
        <!-- stage graph -->

        <collapsible-card id="partners" :title="$gettext('5. Partners') | translate">
          <template v-if="isEmptyArr(project.partners)">
            <div v-for="partner in project.partners" :key="partner.email" class="Partners">
              <simple-field :header="partner.partner_name">
                <ul>
                  <li>
                    <translate>Partner type</translate>:
                    <list-element :value="partner.partner_type * 1" source="getPartnerTypes" root="system" />
                  </li>
                  <li>
                    <translate>Partner contact</translate>:
                    {{ partner.partner_contact }}
                  </li>
                  <li>
                    <translate>Partner email</translate>:
                    <a :href="`mailto:${partner.partner_email}`">{{ partner.partner_email }}</a>
                  </li>
                  <li>
                    <translate>Partner website</translate>:
                    <a :href="partner.partner_website" target="_blank">{{ partner.partner_website }}</a>
                  </li>
                </ul>
              </simple-field>
            </div>
          </template>
          <template v-else>
            <!-- <translate>There's no partners for the initiative.</translate> -->
          </template>
        </collapsible-card>

        <collapsible-card id="technology" :title="$gettext('6. Technology') | translate">
          <simple-field v-if="isEmptyArr(project.platforms)" :header="$gettext('Software platform(s)') | translate">
            <platforms-list :platforms="project.platforms" />
          </simple-field>

          <simple-field v-if="isEmptyArr(project.hardware)" :header="$gettext('Hardware platform(s)') | translate">
            <platforms-list :platforms="project.hardware" source="getHardware" />
          </simple-field>
          <simple-field v-if="isEmptyArr(project.nontech)" :header="$gettext('Non-technology platform(s)') | translate">
            <platforms-list :platforms="project.nontech" source="getNontech" />
          </simple-field>
          <simple-field v-if="isEmptyArr(project.functions)" :header="$gettext('Platform functions') | translate">
            <platforms-list :platforms="project.functions" source="getFunctions" />
          </simple-field>
          <simple-field v-if="project.isc" :header="$gettext('Information security classification ') | translate">
            <list-element :value="project.isc" source="getInfoSec" />
          </simple-field>
        </collapsible-card>

        <collapsible-card
          v-if="countryQuestions && isEmptyArr(countryQuestions)"
          id="countrycustom"
          :title="customFieldsName(country.name)"
        >
          <custom-readonly-field
            v-for="question in countryQuestions"
            :id="question.id"
            :key="question.id"
            :question="question.question"
            :is-draft="isDraft"
            :type="question.type"
          />
        </collapsible-card>

        <div v-if="donors && isEmptyArr(donors)" id="donorcustom">
          <collapsible-card v-for="donor in donors" :key="donor.id" :title="customFieldsName(donor.name)">
            <custom-readonly-field
              v-for="question in donor.donor_questions"
              :id="question.id"
              :key="question.id"
              :question="question.question"
              :is-draft="isDraft"
              :type="question.type"
              :donor-id="donor.id"
            />
          </collapsible-card>
        </div>
      </el-col>
      <el-col :span="6">
        <ProjectNavigation
          @handleClickUnPublish="
            handleClickUnPublish(
              {
                name: 'organisation-initiatives-id-edit',
                params: { ...$route.params },
              },
              $route.params.id
            )
          "
          @handleClickLatest="handleClickLatest($route.params.id)"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
// vuex
import { mapGetters, mapState, mapActions } from 'vuex'
// helpers
import orderBy from 'lodash/orderBy'
import find from 'lodash/find'
import { format } from 'date-fns'
// components
import handleProjectActions from '@/components/mixins/handleProjectActions'
import ListElement from '@/components/project/ListElement'
// import CountryItem from '../common/CountryItem'
import StageHistory from '@/components/project/sections/StageHistory'
import HealthFocusAreasList from '../common/list/HealthFocusAreasList'
import HealthSystemChallengesList from '../common/list/HealthSystemChallengesList'
// import DonorsList from '../common/list/DonorsList'
import ProjectNavigation from './ProjectNavigation'
import CollapsibleCard from './CollapsibleCard'
import SimpleField from './SimpleField'
import TeamList from './TeamList'
import PlatformsList from './PlatformsList'
import DhiList from './DhiList'
import CapabilitiesList from './CapabilitiesList'
import CustomReadonlyField from './CustomReadonlyField'

export default {
  components: {
    ProjectNavigation,
    CollapsibleCard,
    SimpleField,
    // CountryItem,
    TeamList,
    PlatformsList,
    DhiList,
    HealthFocusAreasList,
    HealthSystemChallengesList,
    // DonorsList,
    CustomReadonlyField,
    CapabilitiesList,
    ListElement,
    StageHistory,
  },
  mixins: [handleProjectActions],
  data() {
    return {
      overviewFields: [
        { type: 'program_targets', header: this.$gettext('Program targets') },
        {
          type: 'program_targets_achieved',
          header: this.$gettext('Achieved programme targets'),
        },
        {
          type: 'target_group_reached',
          header: this.$gettext('Number of beneficiaries reached'),
        },
        {
          type: 'current_achievements',
          header: this.$gettext('Initiative achievements'),
        },
        {
          type: 'cpd',
          header: this.$gettext('Country Programme Document inclusion'),
        },
        {
          type: 'awp',
          header: this.$gettext('Annual Work Plan Outcome or Activity'),
        },
        {
          type: 'wbs',
          header: this.$gettext('Work Breakdown Structure (WBS) number'),
        },
        {
          type: 'total_budget',
          header: this.$gettext('Total estimated budget'),
        },
        {
          type: 'total_budget_narrative',
          header: this.$gettext('Activities covered by budget'),
        },
        {
          type: 'funding_needs',
          header: this.$gettext('Funding gaps'),
        },
        {
          type: 'partnership_needs',
          header: this.$gettext('Partnership needs'),
        },
      ],
    }
  },
  computed: {
    ...mapState({
      office: (state) => state.offices.office,
    }),
    ...mapGetters({
      draft: 'project/getProjectData',
      published: 'project/getPublished',
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails',
      resultAreas: 'projects/getResultAreas',
      goalAreas: 'projects/getGoalAreas',
      getCapabilityLevels: 'projects/getCapabilityLevels',
      getCapabilityCategories: 'projects/getCapabilityCategories',
      getCapabilitySubcategories: 'projects/getCapabilitySubcategories',
      unicef_regions: 'system/getUnicefRegions',
      linkTypes: 'system/getLinkTypes',
      modified: 'project/getModified',
      regionalOffices: 'projects/getRegionalOffices',
      innovationWays: 'projects/getInnovationWays',
      userProfiles: 'system/getUserProfilesNoFilter',
      sectors: 'projects/getSectors',
    }),
    getLeadingSector() {
      const list = this.sectors
      return list && this.project && this.project.unicef_leading_sector
        ? list.find((tp) => this.project.unicef_leading_sector.some((sectorId) => sectorId === tp.id)).name
        : ''
    },
    getUserName() {
      const userName = this.userProfiles.find((profile) => profile.email === this.project.contact_email)
      return userName && userName.name ? userName.name : this.project.contact_name
    },
    location() {
      const { selectedRegionOffice, office, country, selectedRegion } = this
      if (selectedRegionOffice && selectedRegionOffice !== 'N/A') {
        return `UNICEF ${selectedRegionOffice}, ${office.city}, ${country.name}, ${selectedRegion}`
      }
      return `UNICEF ${country.name}, ${office.city}, ${country.name}, ${selectedRegion}`
    },
    route() {
      return this.$route.name.split('__')[0]
    },
    isDraft() {
      return this.route === 'organisation-initiatives-id'
    },
    project() {
      return this.isDraft ? this.draft : this.published
    },
    country() {
      if (this.project.country) {
        return this.getCountryDetails(this.project.country)
      }
      return {}
    },
    countryManagers() {
      return this.office?.managers?.length > 0 ? this.office?.managers : []
    },
    selectedRegion() {
      if (this.office) {
        const result = this.unicef_regions.find((uf) => uf.id === this.office.region)
        return (result && result.name) || ' ' // N/A
      }
      return ' ' // N/A
    },
    selectedRegionOffice() {
      if (this.office) {
        const office = this.regionalOffices.find((obj) => obj.id === this.office.regional_office)
        return office ? office.name : ''
      }
      return ''
    },
    lastUpdated() {
      return this.published.modified
        ? format(this.published.modified, 'DD/MM/YYYY HH:mm')
        : format(this.draft.modified, 'DD/MM/YYYY HH:mm')
    },
    countryQuestions() {
      if (this.country) {
        return this.country.country_questions
      }
      return []
    },
    donors() {
      return this.project.donors
        .map((d) => this.getDonorDetails(d))
        .filter((d) => d.donor_questions && d.donor_questions.length > 0)
    },
    resultArea() {
      const result = this.resultAreas.find((r) => r.id === this.project.result_area)
      return result || {}
    },
    goalArea() {
      const result = this.goalAreas.find((r) => r.id === this.project.goal_area)
      return result || {}
    },
    orderedLinkList() {
      return orderBy(this.project.links, ['link_type'], ['asc'])
    },
  },
  mounted() {
    this.loadOffice(this.project.country_office)
  },
  methods: {
    ...mapActions({
      loadOffice: 'offices/loadOffice',
    }),
    getLinkHeader(link_type) {
      const type = find(this.linkTypes, (t) => t.id === link_type)
      return type ? `${type.name}` : link_type
    },
    customFieldsName(name) {
      return this.$gettext('{name} custom fields', { name })
    },
    showOverview(project, linkList) {
      const {
        program_targets,
        program_targets_achieved,
        target_group_reached,
        current_achievements,
        cpd,
        awp,
        wbs,
        total_budget,
        total_budget_narrative,
        funding_needs,
        partnership_needs,
      } = project
      if (
        cpd.length > 0 ||
        wbs.length > 0 ||
        linkList.length > 0 ||
        program_targets ||
        program_targets_achieved ||
        target_group_reached ||
        current_achievements ||
        awp ||
        total_budget ||
        total_budget_narrative ||
        funding_needs ||
        partnership_needs
      ) {
        return true
      }
      return false
    },
    isEmptyArr(arr) {
      return arr.length > 0
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ProjectData {
  .limitPageWidth();

  .cover {
    max-width: 100%;
  }

  .Loader {
    display: block;
    margin: 0 auto 80px;
  }

  > .el-row {
    > .el-col {
      &:first-child {
        width: calc(100% - @projectAsideNavWidth - 20px);
        margin-right: 20px;
      }
      &:last-child {
        width: @projectAsideNavWidth;
      }
    }
  }

  .ContentContainer {
    padding-bottom: 20px;
  }

  .CollapsibleCard {
    .SimpleField {
      margin-bottom: 40px;
      font-size: @fontSizeBase;
      line-height: 20px;

      .Header {
        margin-bottom: 10px;
        font-size: @fontSizeMedium;
        font-weight: 700;
      }

      .Content {
        ul {
          li {
            .svg-inline--fa {
              display: none;
            }
          }
        }
      }

      .SubLevelItem {
        box-sizing: border-box;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 3px;
        padding-left: 30px;
        border-left: 5px solid @colorGrayLight;

        .SimpleField {
          margin: 0 !important;

          .Header {
            font-size: @fontSizeBase !important;
          }
        }

        .CoverageField {
          .SimpleField {
            margin: 20px 0 0 !important;
          }
        }
      }

      .CountryItem {
        .CountryFlag {
          display: none;
        }

        .CountryName {
          margin: 0;
          font-size: @fontSizeBase;
          font-weight: 400;
        }
      }

      .PlatformList {
        .Header {
          font-size: @fontSizeBase;
        }

        .Content {
          .SimpleField {
            margin-top: 20px;
          }
        }
      }

      .StandardsList {
        li {
          a {
            display: block;
            margin: 5px 0 20px;
            color: @colorBrandPrimary;
            text-decoration: none;
            transition: @transitionAll;

            &:hover {
              color: @colorBrandPrimaryLight;
              text-decoration: underline;
            }
          }

          &:last-child {
            a {
              margin-bottom: 0;
            }
          }
        }
      }
    }

    .GrayArea {
      .svg-inline--fa {
        margin-right: 8px;
      }
    }
  }
  .ma-0 {
    margin: 0;
  }
}
</style>
