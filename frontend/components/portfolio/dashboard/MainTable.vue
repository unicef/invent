<template>
  <div class="MainTable">
    <el-table
      ref="mainTable"
      :data="projects"
      :max-height="tableMaxHeight"
      :row-class-name="rowClassCalculator"
      :stripe="false"
      :border="true"
      size="mini"
      style="width: 100%"
      @select="selectHandler"
      @select-all="selectHandler"
      @sort-change="sortChanged"
    >
      <el-table-column :resizable="false" type="selection" align="center" width="45" class-name="selection-td" />
      <el-table-column
        v-if="selectedColumns.includes('1')"
        :resizable="false"
        :label="$gettext('Initiative Name') | translate"
        fixed
        sortable="custom"
        prop="project__name"
        width="240"
        class-name="project-td"
      >
        <template slot-scope="scope">
          <ProjectCard :project="scope.row" hide-borders show-verified />
          <el-tooltip :content="scope.row.favorite ? removeFavoriteText : addFavoriteText" placement="bottom">
            <div class="favorite">
              <fa
                v-if="scope.row.favorite"
                class="heart-full"
                :icon="['fas', 'heart']"
                @click="removeFavorite({ id: scope.row.id, type: 'table' })"
              />
              <fa
                v-else
                class="heart-empty"
                :icon="['far', 'heart']"
                @click="addFavorite({ id: scope.row.id, type: 'table' })"
              />
            </div>
          </el-tooltip>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('61') && tab > 1"
        :resizable="false"
        :label="$gettext('Questionnaires Assigned') | translate"
        sortable="custom"
        prop="review_states"
        width="511"
      >
        <template slot-scope="scope">
          <Reviewers v-if="scope.row.review_states" :id="scope.row.id" :items="scope.row.review_states.review_scores" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="scoringDisplay"
        :resizable="false"
        :label="$gettext('Scoring') | translate"
        prop="scores"
        width="221"
      >
        <template slot-scope="scope">
          <Scores v-if="scope.row.review_states" :scores="scope.row.review_states" :name="scope.row.name" :tab="tab" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('5')"
        :resizable="false"
        :label="$gettext('Region') | translate"
        sortable="custom"
        prop="country__region"
        width="180"
      >
        <template slot-scope="scope">
          <region-item :id="scope.row.region" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('18')"
        :resizable="false"
        :label="$gettext('Regional Office') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <ListElement :value="scope.row.regional_office" source="getRegionalOffices" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('2')"
        :resizable="false"
        :label="$gettext('Country') | translate"
        sortable="custom"
        prop="country__name"
        width="180"
      >
        <template slot-scope="scope">
          <CountryItem :id="scope.row.country" :show-flag="false" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('4')"
        :resizable="false"
        :label="$gettext('UNICEF Office') | translate"
        sortable="custom"
        prop="country_office__name"
        width="180"
      >
        <template slot-scope="scope">
          {{ countryOffice(scope.row.country_office) }}
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('3')"
        :resizable="false"
        :label="$gettext('Last updated') | translate"
        sortable="custom"
        prop="project__modified"
        width="180"
      >
        <template slot-scope="scope">
          {{ convertDate(scope.row.modified) }}
        </template>
      </el-table-column>

      <!-- <el-table-column
        v-if="selectedColumns.includes('19')"
        :resizable="false"
        :label="$gettext('UNICEF Sector') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList
            class="SimpleList"
            :platforms="scope.row.unicef_sector"
            source="getSectors"
          />
        </template>
      </el-table-column> -->
      <el-table-column
        v-if="selectedColumns.includes('64')"
        :resizable="false"
        :label="$gettext('Lead Sector') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.unicef_leading_sector" source="getLeadingSector" />
        </template>
      </el-table-column>
      <el-table-column
        v-if="selectedColumns.includes('65')"
        :resizable="false"
        :label="$gettext('Supporting Sectors') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList
            class="SimpleList"
            :platforms="scope.row.unicef_supporting_sectors"
            source="getSupportingSectors"
          />
        </template>
      </el-table-column>
      <el-table-column
        v-if="selectedColumns.includes('11')"
        :resizable="false"
        :label="$gettext('Goal Area') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <GoalAreaItem :value="scope.row.goal_area" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('26')"
        :resizable="false"
        :label="$gettext('Regional Priorities') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.regional_priorities" source="getRegionalPriorities" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('20')"
        :resizable="false"
        :label="$gettext('Innovation Ways') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.innovation_ways" source="getInnovationWays" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('17')"
        :resizable="false"
        :label="$gettext('Innovation Categories') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList
            class="SimpleList"
            :platforms="scope.row.innovation_categories"
            source="getInnovationCategories"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('21')"
        :resizable="false"
        :label="$gettext('Completed phases') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="stageIDs(scope.row.stages)" source="getStages" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('63')"
        :resizable="false"
        :label="$gettext('Current Phase') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="[scope.row.current_phase]" source="getStages" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('12')"
        :resizable="false"
        :label="$gettext('Result Area') | translate"
        width="180"
      >
        <template slot-scope="scope">
          <ResultAreaItem :value="scope.row.result_area" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('13')"
        :resizable="false"
        :label="$gettext('Capability Levels') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_levels"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilityLevels"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('14')"
        :resizable="false"
        :label="$gettext('Capability Categories') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_categories"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilityCategories"
          />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('15')"
        :resizable="false"
        :label="$gettext('Capability Subcategories') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <CapabilitiesList
            show-icon
            :value="scope.row.capability_subcategories"
            :goal-area="scope.row.goal_area"
            :values-function="getCapabilitySubcategories"
          />
        </template>
      </el-table-column>

      <!-- <el-table-column
        v-if="selectedColumns.includes('6')"
        :resizable="false"
        :label="$gettext('Investors') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <donors-list :value="scope.row.donors" :limit="3" show-icon />
        </template>
      </el-table-column> -->

      <el-table-column
        v-if="selectedColumns.includes('7')"
        :resizable="false"
        :label="$gettext('Programme Focal Point Name') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.contact_name }}</span>
          <a :href="`mailto:${scope.row.contact_email}`" :rel="`email`" class="TextLink">
            {{ scope.row.contact_email }}
          </a>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('8')"
        :resizable="false"
        :label="$gettext('Narrative') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.implementation_overview }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('10')"
        :resizable="false"
        :label="$gettext('Health Focus Areas') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <HfaCategoriesList :value="scope.row.health_focus_areas" :limit="3" value-is-child show-check />
        </template>
      </el-table-column>

      <el-table-column
        v-for="col in countryColumns"
        :key="col.id"
        :resizable="false"
        :render-header="customHeaderRenderer"
        :label="col.label"
        width="240"
      >
        <template slot-scope="scope">
          <CustomAnswersCell :id="col.originalId" :row="scope.row" :type="col.type" :limit="3" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('22')"
        :resizable="false"
        :label="$gettext('Hardware Platforms') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.hardware" source="getHardware" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('23')"
        :resizable="false"
        :label="$gettext('Programme Innovation/Non-Technology Platforms') | translate"
        sortable="custom"
        width="300"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.nontech" source="getNontech" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('24')"
        :resizable="false"
        :label="$gettext('Platform/Product Function') | translate"
        sortable="custom"
        width="250"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.functions" source="getFunctions" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('60')"
        :resizable="false"
        :label="$gettext('Software Platforms(s)') | translate"
        sortable="custom"
        width="180"
      >
        <template slot-scope="scope">
          <PlatformsList class="SimpleList" :platforms="scope.row.platforms" source="getTechnologyPlatforms" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('25')"
        :resizable="false"
        :label="$gettext('Information Security Classification') | translate"
        sortable="custom"
        width="220"
      >
        <template slot-scope="scope">
          <ListElement class="SimpleList" :value="scope.row.isc" source="getInfoSec" />
        </template>
      </el-table-column>

      <!-- new table fields -->
      <el-table-column
        v-if="selectedColumns.includes('28')"
        :resizable="false"
        :label="$gettext('Annual Work Plan (AWP) Outcome/Activity') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.awp }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('29')"
        :resizable="false"
        :label="$gettext('Currency') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.currency }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('30')"
        :resizable="false"
        :label="$gettext('Current Achievements') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.current_achievements }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('31')"
        :resizable="false"
        :label="$gettext('Funding Needs') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.funding_needs }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('32')"
        :resizable="false"
        :label="$gettext('In Country programme document (CPD) and annual work plan?') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <SimpleList :items="scope.row.cpd" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('33')"
        :resizable="false"
        :label="$gettext('Links to website/Current Documentation + URL') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <SimpleList :items="scope.row.links" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('34')"
        :resizable="false"
        :label="$gettext('Overview') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.overview }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('35')"
        :resizable="false"
        :label="$gettext('Partner Data') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <SimpleList :items="scope.row.partners" />
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('36')"
        :resizable="false"
        :label="$gettext('Partnership needs') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.partnership_needs }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('37')"
        :resizable="false"
        :label="$gettext('Program Targets') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.program_targets }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('38')"
        :resizable="false"
        :label="$gettext('Program Targets Archieved') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.program_targets_achieved }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('39')"
        :resizable="false"
        :label="$gettext('Start Date') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.start_date | simpleDateFormat }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('40')"
        :resizable="false"
        :label="$gettext('End Date') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.end_date | simpleDateFormat }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('41')"
        :resizable="false"
        :label="$gettext('Target Group (Target Population) Reached') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.target_group_reached | formatNumber }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('42')"
        :resizable="false"
        :label="$gettext('Total Budget') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.total_budget | formatNumber }}</p>
        </template>
      </el-table-column>

      <el-table-column
        v-if="selectedColumns.includes('43')"
        :resizable="false"
        :label="$gettext('Total Budget (Narrative)') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <p>{{ scope.row.total_budget_narrative }}</p>
        </template>
      </el-table-column>
      <el-table-column
        v-if="selectedColumns.includes('44')"
        :resizable="false"
        :label="$gettext('Work Breakdown Structure (WBS)') | translate"
        width="240"
      >
        <template slot-scope="scope">
          <SimpleList :items="scope.row.wbs" />
        </template>
      </el-table-column>
      <!-- new table fields -->

      <el-table-column
        v-for="col in donorColumns"
        :key="col.id"
        :resizable="false"
        :render-header="customHeaderRenderer"
        :label="col.label"
        width="240"
      >
        <template slot-scope="scope">
          <CustomAnswersCell
            :id="col.originalId"
            :row="scope.row"
            :type="col.type"
            :donor-id="col.donorId"
            :limit="3"
          />
        </template>
      </el-table-column>
    </el-table>

    <div class="Pagination">
      <el-pagination
        :current-page="page"
        :page-size="pageSize"
        :page-sizes="pageSizeOption"
        :total="total"
        :layout="paginationOrderStr"
        @size-change="sizeChange"
        @prev-click="pagClick"
        @next-click="pagClick"
      >
        <current-page :total="total" :page-size="pageSize" :page="page" />
      </el-pagination>
    </div>
    <!-- dialogs -->
    <review />
    <score />
  </div>
</template>

<script>
import { setTimeout } from 'timers'
import { format } from 'date-fns'
import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'
import { mapGettersActions } from '@/utilities/form.js'
import debounce from 'lodash/debounce'

import ProjectCard from '@/components/common/ProjectCard'
import CountryItem from '@/components/common/CountryItem'
import HfaCategoriesList from '@/components/common/list/HfaCategoriesList'
// import DonorsList from '@/components/common/list/DonorsList'
import RegionItem from '@/components/common/RegionItem'
import CustomAnswersCell from '@/components/dashboard/CustomAnswersCell'
import GoalAreaItem from '@/components/dashboard/GoalAreaItem'
import ResultAreaItem from '@/components/dashboard/ResultAreaItem'
import CurrentPage from '@/components/dashboard/CurrentPage'
import CapabilitiesList from '@/components/project/CapabilitiesList'
import Reviewers from '@/components/portfolio/dashboard/table/Reviewers'
import Scores from '@/components/portfolio/dashboard/table/Scores'
import ListElement from '@/components/project/ListElement'
import SimpleList from '@/components/common/list/SimpleList'

// dialogs
import Review from '@/components/portfolio/dashboard/dialog/Review'
import Score from '@/components/portfolio/dashboard/dialog/Score'
import PlatformsList from '@/components/project/PlatformsList'

export default {
  components: {
    ProjectCard,
    CountryItem,
    HfaCategoriesList,
    // DonorsList,
    RegionItem,
    CustomAnswersCell,
    CurrentPage,
    CapabilitiesList,
    GoalAreaItem,
    ResultAreaItem,
    Reviewers,
    Scores,
    Review,
    PlatformsList,
    ListElement,
    Score,
    SimpleList,
  },
  data() {
    return {
      pageSizeOption: [10, 20, 50, 100],
      tableMaxHeight: 200,
      localSort: null,
      addFavoriteText: this.$gettext('Add to Favorites'),
      removeFavoriteText: this.$gettext('Remove from Favorites'),
    }
  },
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
      projects: (state) => state.portfolio.projects,
      tab: (state) => state.portfolio.tab,
      // pagination
      total: (state) => state.portfolio.total,
      pageSize: (state) => state.search.filter.page_size,
      page: (state) => state.search.filter.page,
    }),
    ...mapGetters({
      selectedColumns: 'dashboard/getSelectedColumns',
      selectedRows: 'portfolio/getSelectedRows',
      selectAll: 'portfolio/getSelectAll',
      countryColumns: 'dashboard/getCountryColumns',
      donorColumns: 'dashboard/getDonorColumns',
      getCapabilityLevels: 'projects/getCapabilityLevels',
      getCapabilityCategories: 'projects/getCapabilityCategories',
      getCapabilitySubcategories: 'projects/getCapabilitySubcategories',
    }),
    ...mapGettersActions({
      sorting: ['dashboard', 'getSorting', 'setSorting', 0],
    }),
    paginationOrderStr() {
      const loc = this.$i18n.locale
      return loc === 'ar' ? 'sizes, next, slot, prev' : 'sizes, prev, slot, next'
    },
    scoringDisplay() {
      if (this.$route.name.includes('organisation-portfolio-management-id')) {
        return this.selectedColumns.includes('62') && (this.tab === 2 || this.tab === 3)
      }
      return false
    },
  },
  watch: {
    selectAll: {
      immediate: true,
      handler(value) {
        if (this.$refs.mainTable) {
          if (value) {
            this.$refs.mainTable.toggleAllSelection()
          } else if (this.selectedRows.length === 0) {
            this.$refs.mainTable.clearSelection()
          }
        }
      },
    },
    selectedColumns: {
      immediate: false,
      handler(columns) {
        this.$nextTick(() => {
          this.$refs.mainTable.doLayout()
          setTimeout(() => {
            this.alignFixedTableWidthForRTL()
          }, 50)
        })
      },
    },
    sorting: {
      immediate: false,
      handler(current) {
        if (current !== this.localSort) {
          this.fixSorting(current)
        }
      },
    },
  },
  mounted() {
    if (this.offices.length === 0) {
      this.loadOffices()
    }
    setTimeout(() => {
      this.fixTableHeight()
      this.fixSorting(this.$route.query.ordering)
      if (this.selectAll) {
        this.$refs.mainTable.clearSelection()
        this.$refs.mainTable.toggleAllSelection()
      }
      this.$nextTick(() => {
        this.alignFixedTableWidthForRTL()
      })
    }, 500)
  },
  methods: {
    ...mapMutations({
      setSearch: 'search/SET_SEARCH',
      setPageSize: 'search/setPageSize',
    }),
    ...mapActions({
      setSelectedRows: 'portfolio/setSelectedRows',
      loadOffices: 'offices/loadOffices',
      getSearch: 'search/getSearch',
      addFavorite: 'projects/addFavorite',
      removeFavorite: 'projects/removeFavorite',
    }),
    customHeaderRenderer(h, { column, $index }) {
      return h('span', { attrs: { title: column.label } }, column.label)
    },
    selectHandler(selection) {
      this.setSelectedRows(selection.map((s) => s.id))
    },
    rowClassCalculator({ row }) {
      return this.selectedRows.includes(row.id) ? 'Selected' : 'NotSelected'
    },
    sortChanged({ prop, order }) {
      if (order === 'descending') {
        this.sorting = '-' + prop
        this.localSort = '-' + prop
      } else {
        this.sorting = prop
        this.localSort = prop
      }
    },
    convertDate(date) {
      return date ? format(date, 'DD/MM/YYYY HH:mm') : ' ' // N/A
    },
    fixTableHeight() {
      const maxHeight = window.getComputedStyle(this.$el).getPropertyValue('max-height')
      this.tableMaxHeight = +maxHeight.replace('px', '')
      this.$refs.mainTable.doLayout()
    },
    fixSorting(prop) {
      if (prop) {
        let direction = 'ascending'
        if (prop.startsWith('-')) {
          direction = 'descending'
          prop = prop.replace('-', '')
        }
        this.$refs.mainTable.sort(prop, direction)
      }
    },
    alignFixedTableWidthForRTL() {
      const locale = this.$i18n.locale
      if (locale === 'ar') {
        const rawTableWidth = document.querySelector('.el-table__header').offsetWidth
        const fixedFieldWidths = 275
        const toShowBorder = 1

        const toAlignWidth = rawTableWidth - fixedFieldWidths - toShowBorder

        const fixedTableHeader = document.querySelector('.el-table__fixed-header-wrapper')
        const fixedTableBody = document.querySelector('.el-table__fixed-body-wrapper')

        if (fixedTableBody && fixedTableHeader) {
          fixedTableHeader.style.left = -toAlignWidth + 'px'
          fixedTableBody.style.left = -toAlignWidth + 'px'
        }
      }
    },
    countryOffice(id) {
      const office = this.offices.find((obj) => obj.id === id)
      return office ? office.name : ' ' // N/A
    },
    handleFavorite(id) {
      console.log(`this will mark or unmark ${id}`)
    },
    sizeChange(val) {
      this.setPageSize(val)
      this.getSearchResults()
    },
    pagClick(val) {
      this.setSearch({ key: 'page', val })
      this.getSearchResults()
    },
    getSearchResults: debounce(function () {
      this.getSearch()
    }, 350),
    stageIDs(stageList) {
      return stageList ? stageList.map((stage) => stage.id) : []
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.MainTable {
  margin: 0 40px 120px;
  max-height: calc(100vh - @topBarHeightSubpage - @actionBarHeight - @tableTopActionsHeight - @appFooterHeight - 93px);

  .SimpleList {
    ul {
      margin: 0;
      padding: 0;
      list-style-type: none;
    }
  }

  .favorite {
    cursor: pointer;
    position: absolute;
    top: 32px;
    left: -30px;
    svg {
      font-size: 14px;
    }
    .heart-full {
      color: #c4225f;
    }
    .heart-empty {
      color: @colorBrandGrayLight;
    }
  }

  .el-table--border th {
    border-right: 1px solid @colorWhite;
  }
  .el-table--group,
  .el-table--border {
    border: 0px solid transparent;
  }
  .el-table__body tr.hover-row > td,
  .el-table__body tr.hover-row.current-row > td {
    background-color: #e8f6fd;
  }
  // Custom table template
  .el-table {
    th,
    td {
      vertical-align: top;
    }

    .caret-wrapper .sort-caret {
      &.ascending {
        border-bottom-color: @colorWhite;
      }
      &.descending {
        border-top-color: @colorWhite;
      }
    }

    th {
      background-color: @colorBrandPrimary;
      > .cell {
        font-size: @fontSizeSmall;
        color: @colorWhite;
        font-weight: bold;
        letter-spacing: 0;
        line-height: 29px;
        white-space: nowrap;
      }

      &.is-leaf {
        border-bottom-color: @colorWhite;
      }

      // Disable select-all-row
      &.el-table-column--selection {
        .el-checkbox {
          display: none;
        }
      }
    }

    td {
      padding: 10px 16px 10px 12px;
      &.selection-td {
        padding: 10px 0 10px 0 !important;
      }
      &.project-td {
        padding: 10px 10px 10px 12px;
      }
      > .cell {
        min-height: 37px;
        line-height: 17px;
        word-break: normal;
        padding: 0;
        p {
          position: relative;
          margin: 0;
          display: -webkit-box;
          -webkit-line-clamp: 4;
          -webkit-box-orient: vertical;
          // With 17 in the calc the fixed columns and the rest of the table go out of sync
          // max-height: calc(16.5px * 4);
          // but it should be 15, based on the line-height
          max-height: calc(15px * 4);
          font-size: @fontSizeSmall;
          letter-spacing: 0;
          line-height: 15px;
          font-weight: 100;
        }

        a {
          &[rel='email'] {
            display: block;
          }
        }
      }
    }

    // selected table row
    .el-table__row {
      &.Selected {
        > td {
          background-color: #e8f6fd;
        }
      }
    }

    .el-table-column--selection {
      > .cell {
        text-overflow: clip !important;
      }
    }

    .caret-wrapper {
      position: absolute;
      top: 4px;
      right: 4px;
    }

    .el-table__empty-block {
      position: relative;
      width: 100% !important;
      text-align: center;

      .el-table__empty-text {
        width: auto;
        font-weight: 700;
      }
    }

    .ProjectCard {
      overflow: visible;

      .ProjectLegend {
        top: 1px;
        right: -1px;
        opacity: 1 !important;

        .svg-inline--fa {
          position: relative;
          height: 14px;
          font-size: 12px;

          &.fa-star {
            right: 1px;
            font-size: 11px;
          }

          &.fa-globe-africa {
            right: 1px;
          }
        }
      }
    }

    .CountryItem {
      .CountryFlag {
        display: none;
      }

      .CountryName {
        margin: 0;
        font-size: @fontSizeSmall;
        letter-spacing: 0;
        line-height: 15px;
        font-weight: 100;
      }
    }

    .DonorList {
      ul {
        padding: 0;
        margin: 0;
      }

      .DonorItem {
        display: inline-flex;
        align-items: flex-start;
        width: 100%;

        .svg-inline--fa {
          position: relative;
          top: -1px;
          margin-right: 5px;
        }
      }
    }

    .HealthFocusAreasList,
    .CustomAnswersCell,
    .CapabilitiesList {
      ul {
        list-style-type: none;
        margin: 0;
        padding: 0;

        li {
          position: relative;
          display: flex;
          align-items: center;
          > span {
            &:last-child {
              margin-left: 6px;
              .textTruncate();
            }
          }
        }
      }
    }
  }

  .Pagination {
    z-index: 5;
    position: relative;
    top: -1px;
    width: 100%;
    // don't forget to calculate this into max-height of MainTable
    height: 53px;
    //
    box-sizing: border-box;
    border-top: 1px solid @colorGrayLight;
    background-color: @colorWhite;
    text-align: right;

    .el-pagination {
      padding: 11px 15px;
      font-weight: 400;

      .el-pagination__sizes {
        float: left;
        margin: 0;
      }

      .PageCounter {
        display: inline-block;
        margin: 0 10px;
        font-size: @fontSizeSmall;
        color: @colorTextSecondary;
        letter-spacing: 0;
        line-height: 15px;
      }

      button {
        padding: 0;
        background-color: transparent;
        transition: @transitionAll;
        i {
          font-size: @fontSizeLarge;
          font-weight: 700;
        }
      }
    }
  }
}
</style>
