<template>
  <div class="ProjectData">
    <el-row type="flex">
      <el-col :span="18">
        <collapsible-card
          id="general"
          :title="$gettext('1. General Overview') | translate"
        >
          <simple-field
            :content="project.name"
            :header="$gettext('Initiative Name') | translate"
          />

          <simple-field
            :header="$gettext('UNICEF Office') | translate"
            :content="location"
          />

          <simple-field
            :content="project.overview"
            :header="$gettext('Overview of the initiative') | translate"
          />

          <simple-field
            :content="project.implementation_overview"
            :header="$gettext('Narrative of the initiative') | translate"
          />

          <el-row>
            <el-col :span="12">
              <simple-field
                :content="project.contact_name"
                :header="$gettext('Contact name') | translate"
              />
            </el-col>
            <el-col :span="12">
              <simple-field
                :content="project.contact_email"
                :header="$gettext('Contact email') | translate"
              />
            </el-col>
          </el-row>

          <div class="GrayArea">
            <simple-field :header="$gettext('Team members') | translate">
              <team-list :value="project.team" />
            </simple-field>
          </div>

          <simple-field
            :header="$gettext('Last Updated') | translate"
            :content="lastUpdated"
          />
        </collapsible-card>

        <collapsible-card
          id="categorization"
          :title="$gettext('2. Categorization') | translate"
        >
          <simple-field :header="$gettext('Sector') | translate">
            <platforms-list
              :platforms="project.unicef_sector"
              source="getSectors"
            />
          </simple-field>

          <simple-field
            :header="$gettext('Goal Area') | translate"
            :content="goalArea.name"
          />

          <simple-field
            :header="$gettext('Result Area') | translate"
            :content="resultArea.name"
          />

          <template v-if="goalArea && goalArea.id && goalArea.id === 1">
            <simple-field
              :header="$gettext('Digital Health Intervention(s)') | translate"
            >
              <DhiList :values="project.dhis" />
            </simple-field>

            <simple-field
              :header="$gettext('Programme Focus Area(s)') | translate"
            >
              <health-focus-areas-list :value="project.health_focus_areas" />
            </simple-field>

            <simple-field :header="$gettext('System challenge(s)') | translate">
              <health-system-challenges-list :value="project.hsc_challenges" />
            </simple-field>
          </template>

          <template
            v-else-if="
              goalArea &&
              goalArea.id &&
              goalArea.capability_level_question !== 'MISSING'
            "
          >
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
            :header="$gettext('Regional priority(ies)') | translate"
          >
            <platforms-list
              :platforms="project.regional_priorities"
              source="getRegionalPriorities"
            />
          </simple-field>

          <simple-field
            :header="$gettext('Innovation category(ies)') | translate"
          >
            <platforms-list
              :platforms="project.innovation_categories"
              source="getInnovationCategories"
            />
          </simple-field>
        </collapsible-card>

        <collapsible-card
          id="implementation"
          :title="$gettext('3. Implementation Overview') | translate"
        >
          <simple-field
            :content="project.program_targets"
            :header="$gettext('Programme targets') | translate"
          />
          <simple-field
            :content="project.program_targets_achieved"
            :header="$gettext('Achieved programme targets ') | translate"
          />
          <simple-field
            :content="project.target_group_reached"
            :header="$gettext('Number of beneficiaries reached') | translate"
          />

          <simple-field
            :content="project.current_achievements"
            :header="$gettext('Initiative achievements') | translate"
          />

          <simple-field
            :header="
              $gettext('Country Programme Document inclusion') | translate
            "
          >
            <platforms-list :platforms="project.cpd" source="getCpd" />
          </simple-field>
          <simple-field
            :content="project.awp"
            :header="
              $gettext('Annual Work Plan Outcome or Activity') | translate
            "
          />
          <simple-field
            :header="
              $gettext('Work Breakdown Structure (WBS) number') | translate
            "
          >
            <ul>
              <li v-for="wbs in project.wbs" :key="wbs">
                <span>{{ wbs }}</span>
              </li>
            </ul>
          </simple-field>
          <simple-field
            :header="$gettext('Total estimated budget') | translate"
          >
            {{ project.total_budget }}
            <list-element
              v-if="project.total_budget"
              :value="project.currency"
              source="getCurrencies"
            />
          </simple-field>
          <simple-field
            :content="project.total_budget_narrative"
            :header="$gettext('Activities covered by budget') | translate"
          />

          <simple-field
            :content="project.funding_needs"
            :header="$gettext('Funding gaps') | translate"
          />
          <simple-field
            :content="project.partnership_needs"
            :header="$gettext('Partnership needs') | translate"
          />
          <simple-field
            v-for="{ link_url, link_type } in orderedLinkList"
            :key="'link_type' + link_type"
            :content="link_url"
            :header="getLinkHeader(link_type)"
            link
          />
          <!--          <simple-field :header="$gettext('Investor(s)') | translate">-->
          <!--            <donors-list :value="project.donors" />-->
          <!--          </simple-field>-->
        </collapsible-card>

        <collapsible-card id="phase" :title="$gettext('4. Phase') | translate">
          <el-row>
            <el-col :span="12">
              <simple-field
                :content="project.start_date"
                :header="$gettext('Initiative start date') | translate"
                date
              />
            </el-col>
          </el-row>

          <simple-field :header="$gettext('Current phase') | translate">
            <list-element :value="project.phase" source="getPhases" />
          </simple-field>

          <el-row>
            <el-col :span="12">
              <simple-field
                :content="project.end_date"
                :header="$gettext('Initiative end date') | translate"
                date
              />
            </el-col>
          </el-row>
        </collapsible-card>

        <collapsible-card
          id="partners"
          :title="$gettext('5. Partners') | translate"
        >
          <div
            v-for="partner in project.partners"
            :key="partner.email"
            class="Partners"
          >
            <simple-field :header="partner.partner_name">
              <ul>
                <li>
                  <translate>Partner type</translate>:
                  <list-element
                    :value="partner.partner_type * 1"
                    source="getPartnerTypes"
                    root="system"
                  />
                </li>
                <li>
                  <translate>Partner contact</translate>:
                  {{ partner.partner_contact }}
                </li>
                <li>
                  <translate>Partner email</translate>:
                  <a :href="`mailto:${partner.partner_email}`">{{
                    partner.partner_email
                  }}</a>
                </li>
                <li>
                  <translate>Partner website</translate>:
                  <a :href="`mailto:${partner.partner_website}`">{{
                    partner.partner_website
                  }}</a>
                </li>
              </ul>
            </simple-field>
          </div>
        </collapsible-card>

        <collapsible-card
          id="technology"
          :title="$gettext('6. Technology') | translate"
        >
          <simple-field :header="$gettext('Software platform(s)') | translate">
            <platforms-list :platforms="project.platforms" />
          </simple-field>

          <simple-field :header="$gettext('Hardware platform(s)') | translate">
            <platforms-list
              :platforms="project.hardware"
              source="getHardware"
            />
          </simple-field>
          <simple-field
            :header="$gettext('Non-technology platform(s)') | translate"
          >
            <platforms-list :platforms="project.nontech" source="getNontech" />
          </simple-field>
          <simple-field :header="$gettext('Platform functions') | translate">
            <platforms-list
              :platforms="project.functions"
              source="getFunctions"
            />
          </simple-field>
        </collapsible-card>

        <div v-if="donors && donors.length > 0" id="donorcustom">
          <collapsible-card
            v-for="donor in donors"
            :key="donor.id"
            :title="customFieldsName(donor.name)"
          >
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
        <project-navigation
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
import { format } from 'date-fns'
import handleProjectActions from '@/components/mixins/handleProjectActions'
import ListElement from '@/components/project/ListElement'
import find from 'lodash/find'
import orderBy from 'lodash/orderBy'
import { mapGetters, mapState, mapActions } from 'vuex'
// import CountryItem from '../common/CountryItem'
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
  },
  mixins: [handleProjectActions],
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
    }),
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
    selectedRegion() {
      if (this.office) {
        const result = this.unicef_regions.find(
          (uf) => uf.id === this.office.region
        )
        return (result && result.name) || ' ' // N/A
      }
      return ' ' // N/A
    },
    selectedRegionOffice() {
      if (this.office) {
        const office = this.regionalOffices.find(
          (obj) => obj.id === this.office.regional_office
        )
        return office ? office.name : ''
      }
      return ''
    },
    lastUpdated() {
      return format(new Date(this.modified), 'DD/MM/YYYY HH:mm')
    },
    donors() {
      return this.project.donors
        .map((d) => this.getDonorDetails(d))
        .filter((d) => d.donor_questions && d.donor_questions.length > 0)
    },
    resultArea() {
      const result = this.resultAreas.find(
        (r) => r.id === this.project.result_area
      )
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
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.ProjectData {
  .limitPageWidth();

  .Loader {
    display: block;
    margin: 0 auto 80px;
  }

  > .el-row {
    > .el-col {
      // form fieldsets
      &:first-child {
        width: calc(100% - @projectAsideNavWidth - 20px);
        margin-right: 20px;
      }

      // aside navigation
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
}
</style>
