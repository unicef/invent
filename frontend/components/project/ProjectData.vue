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

          <simple-field :header="$gettext('Organisation') | translate">
            <organisation-item :id="project.organisation" />
          </simple-field>

          <simple-field
            :header="$gettext('Unicef Office') | translate"
            :content="office.name"
          />

          <simple-field :header="$gettext('Country') | translate">
            <country-item :id="project.country" :show-flag="false" />
          </simple-field>

          <simple-field
            :header="$gettext('Region') | translate"
            :content="selectedRegion"
          />

          <simple-field
            :header="$gettext('Multicountry or Regional Office\n') | translate"
            :content="selectedRegionOffice"
          />

          <simple-field :header="$gettext('Field Office') | translate">
            <FieldOfficeItem
              :value="project.field_office"
              :office="office.id"
            />
          </simple-field>

          <simple-field
            :header="$gettext('Last Updated') | translate"
            :content="lastUpdated"
          />
          <simple-field
            :content="project.overview"
            :header="$gettext('Overview') | translate"
          />
          <simple-field
            :content="project.implementation_overview"
            :header="$gettext('Initiative Description') | translate"
          />

          <el-row>
            <el-col :span="12">
              <simple-field
                :content="project.start_date"
                :header="$gettext('Initiative start date') | translate"
                date
              />
            </el-col>
            <el-col :span="12">
              <simple-field
                :content="project.end_date"
                :header="$gettext('Initiative end date') | translate"
                date
              />
            </el-col>
          </el-row>
          <div class="GrayArea">
            <simple-field :header="$gettext('Team members') | translate">
              <team-list :value="project.team" />
            </simple-field>
            <simple-field :header="$gettext('Viewers') | translate">
              <team-list :value="project.viewers" />
            </simple-field>
          </div>
        </collapsible-card>

        <collapsible-card
          id="focalpoint"
          :title="$gettext('2. Focal Point Overview') | translate"
        >
          <el-row>
            <el-col :span="12">
              <simple-field
                :content="project.contact_name"
                :header="$gettext('Programme Focal Point Name') | translate"
              />
            </el-col>
            <el-col :span="12">
              <simple-field
                :content="project.contact_email"
                :header="$gettext('Programme Focal Point Email') | translate"
              />
            </el-col>
          </el-row>
        </collapsible-card>

        <collapsible-card
          id="implementation"
          :title="$gettext('3. Implementation Overview') | translate"
        >
          <simple-field
            :header="$gettext('Goal area') | translate"
            :content="goalArea.name"
          />

          <simple-field
            :header="$gettext('Result area') | translate"
            :content="resultArea.name"
          />

          <template v-if="goalArea && goalArea.id && goalArea.id === 1">
            <simple-field
              :header="
                $gettext(
                  'What is the health capability area(s) addressed? What are the Health System Challenges addressed by the Digital Health Intervention?'
                ) | translate
              "
            >
              <DhiList :values="project.dhis" />
            </simple-field>

            <simple-field
              :header="$gettext('Health focus area(s)') | translate"
            >
              <health-focus-areas-list :value="project.health_focus_areas" />
            </simple-field>

            <simple-field
              :header="$gettext('Health System Challenges (HSC)') | translate"
            >
              <health-system-challenges-list :value="project.hsc_challenges" />
            </simple-field>
          </template>

          <template v-else-if="goalArea && goalArea.id">
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

          <simple-field :header="$gettext('Software') | translate">
            <platforms-list :platforms="project.platforms" />
          </simple-field>

          <simple-field :header="$gettext('Investor(s)') | translate">
            <donors-list :value="project.donors" />
          </simple-field>

          <simple-field
            :content="project.program_targets"
            :header="$gettext('Program Targets') | translate"
          />
          <simple-field
            :content="project.program_targets_achieved"
            :header="$gettext('Program Targets Achieved') | translate"
          />
          <simple-field
            :content="project.target_group_reached"
            :header="
              $gettext('Target Group (Target Population) Reached ') | translate
            "
          />
          <simple-field
            :content="project.current_achievements"
            :header="$gettext('Current Achievements') | translate"
          />
          <simple-field
            :header="
              $gettext(
                'In Country programme document (CPD) and annual work plan'
              ) | translate
            "
          >
            <platforms-list :platforms="project.cpd" source="getCpd" />
          </simple-field>
          <simple-field
            :content="project.awp"
            :header="$gettext('Annual Work Plan') | translate"
          />
          <simple-field
            :header="$gettext('Work Breakdown Structure (WBS)') | translate"
          >
            <ul>
              <li v-for="wbs in project.wbs" :key="wbs">
                <span>{{ wbs }}</span>
              </li>
            </ul>
          </simple-field>
          <simple-field :header="$gettext('Total Budget') | translate">
            {{ project.total_budget }}
            <list-element :value="project.currency" source="getCurrencies" />
          </simple-field>
          <simple-field
            :content="project.total_budget_narrative"
            :header="$gettext('Total Budget (Narrative)') | translate"
          />
          <simple-field
            :content="project.funding_needs"
            :header="$gettext('Funding Needs') | translate"
          />
          <simple-field
            :content="project.partnership_needs"
            :header="$gettext('Partnership Needs') | translate"
          />
          <simple-field
            v-for="{ link_url, link_type } in orderedLinkList"
            :key="'link_type' + link_type"
            :content="link_url"
            :header="getLinkHeader(link_type)"
          />
        </collapsible-card>

        <collapsible-card id="phase" :title="$gettext('4. Phase') | translate">
          <simple-field :header="$gettext('Phase of Initiative') | translate">
            <list-element :value="project.phase" source="getPhases" />
          </simple-field>
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
                  <translate>Partner Type</translate>:
                  <list-element
                    :value="partner.partner_type"
                    source="getPartnerTypes"
                    root="system"
                  />
                </li>
                <li>
                  <translate>Partner Contact</translate>:
                  {{ partner.partner_contact }}
                </li>
                <li>
                  <translate>Partner Email</translate>:
                  <a :href="`mailto:${partner.partner_email}`">{{
                    partner.partner_email
                  }}</a>
                </li>
                <li>
                  <translate>Partner Website</translate>:
                  <a :href="`mailto:${partner.partner_website}`">{{
                    partner.partner_website
                  }}</a>
                </li>
              </ul>
            </simple-field>
          </div>
        </collapsible-card>

        <collapsible-card
          id="categorization"
          :title="$gettext('6. Categorization') | translate"
        >
          <simple-field :header="$gettext('UNICEF Sector') | translate">
            <platforms-list
              :platforms="project.unicef_sector"
              source="getSectors"
            />
          </simple-field>
          <simple-field :header="$gettext('Regional Priorities') | translate">
            <platforms-list
              :platforms="project.regional_priorities"
              source="getRegionalPriorities"
            />
          </simple-field>
          <simple-field :header="$gettext('Innovation Categories') | translate">
            <platforms-list
              :platforms="project.innovation_categories"
              source="getInnovationCategories"
            />
          </simple-field>
        </collapsible-card>

        <collapsible-card
          id="technology"
          :title="$gettext('7. Technology') | translate"
        >
          <simple-field
            :header="
              $gettext('Hardware Platform(s) and Physical Product(s)')
                | translate
            "
          >
            <platforms-list
              :platforms="project.hardware"
              source="getHardware"
            />
          </simple-field>
          <simple-field
            :header="
              $gettext('Programme Innovation(s) and Non-Technology Platform(s)')
                | translate
            "
          >
            <platforms-list :platforms="project.nontech" source="getNontech" />
          </simple-field>
          <simple-field
            :header="$gettext('Function(s) of Platform') | translate"
          >
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
import OrganisationItem from '../common/OrganisationItem'
import CountryItem from '../common/CountryItem'
import HealthFocusAreasList from '../common/list/HealthFocusAreasList'
import HealthSystemChallengesList from '../common/list/HealthSystemChallengesList'
import DonorsList from '../common/list/DonorsList'
import ProjectNavigation from './ProjectNavigation'
import CollapsibleCard from './CollapsibleCard'
import SimpleField from './SimpleField'
import TeamList from './TeamList'
import PlatformsList from './PlatformsList'
import FieldOfficeItem from './FieldOfficeItem'
import DhiList from './DhiList'
import CapabilitiesList from './CapabilitiesList'
import CustomReadonlyField from './CustomReadonlyField'

export default {
  components: {
    ProjectNavigation,
    CollapsibleCard,
    SimpleField,
    OrganisationItem,
    CountryItem,
    TeamList,
    PlatformsList,
    FieldOfficeItem,
    DhiList,
    HealthFocusAreasList,
    HealthSystemChallengesList,
    DonorsList,
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
      return null
    },
    selectedRegion() {
      if (this.office) {
        const result = this.unicef_regions.find(
          (uf) => uf.id === this.office.region
        )
        return (result && result.name) || 'N/A'
      }
      return 'N/A'
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
      return type ? `${type.name} URL` : link_type
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
