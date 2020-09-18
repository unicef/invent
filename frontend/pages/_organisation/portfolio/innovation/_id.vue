<template>
  <section class="portfolio-area">
    <div class="content-area">
      <div class="portfolio">
        <div class="PHeader">
          <h2>
            <translate>Portfolio:</translate>
            <el-dropdown
              trigger="click"
              placement="bottom-start"
            >
              <span class="Title el-dropdown-link">
                Learning<i class="el-icon-caret-bottom el-icon--right" />
              </span>
              <el-dropdown-menu
                slot="dropdown"
                class="PDropdown"
              >
                <el-dropdown-item>Action 1</el-dropdown-item>
                <el-dropdown-item>Action 2</el-dropdown-item>
                <el-dropdown-item>Action 3</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </h2>
        </div>
        <el-tabs
          v-model="activeName"
        >
          <el-tab-pane
            label="AMBITION MATRIX"
            name="ambition"
          >
            <Matrix
              bg-image="/bg-ambition_matrix.svg"
              :elements="elements"
              :left="['existing', 'challenge', 'new']"
              :bottom="['existing', 'solution (tools)', 'new']"
            />
          </el-tab-pane>
          <el-tab-pane
            label="RISK-IMPACT MATRIX"
            name="risk"
          >
            <Matrix
              bg-color="#FCEFE8"
              color="#F26A21"
              :elements="elements"
              :left="['low', 'risk', 'high']"
              :bottom="['low', 'impact (total global need)', 'high']"
            />
          </el-tab-pane>
          <el-tab-pane
            label="PROBLEM STATEMENT MATRIX"
            name="problem"
          >
            <div class="Problems">
              <el-row type="flex">
                <el-col
                  v-for="(col, index) in ['Neglected', 'Moderate', 'High activity']"
                  :key="col"
                  span="8"
                >
                  <div :class="`Problem Problem${index + 1}`">
                    <div class="Title">
                      {{ col }}
                    </div>
                    <div>
                      <radio
                        v-for="statement in problemColumns[index]"
                        :key="statement.id"
                        :value="selectedProblem === statement.id"
                        :disabled="disabledProblems.indexOf(statement.id) !== -1"
                        @update="select(statement.id, $event)"
                      >
                        {{ statement.title }}
                      </radio>
                    </div>
                  </div>
                </el-col>
              </el-row>
              <el-row>
                <div class="Info">
                  <i class="fas fa-info-circle" />
                  By clicking on a problem statement you can add or remove it from your current filter settings.
                </div>
              </el-row>
            </div>
          </el-tab-pane>
          <el-tab-pane
            label="MAP VIEW"
            name="map"
          >
            MAP
          </el-tab-pane>
        </el-tabs>

        <div class="DashboardListView">
          <el-row>
            <table-top-actions />
          </el-row>
          <el-row>
            <main-table />
          </el-row>
        </div>
      </div>
    </div>
    <aside class="filter-area">
      <advanced-search />
    </aside>
  </section>
</template>

<script>
import TableTopActions from '@/components/portfolio/dashboard/TableTopActions';
import MainTable from '@/components/portfolio/dashboard/MainTable';
import AdvancedSearch from '@/components/dashboard/AdvancedSearch';
import Matrix from '@/components/portfolio/Matrix';
import Radio from '@/components/portfolio/form/inputs/Radio';
import groupBy from 'lodash/groupBy';

export default {
  components: {
    Matrix,
    Radio,
    MainTable,
    AdvancedSearch,
    TableTopActions
  },
  data () {
    return {
      activeName: 'ambition',
      selectedProblem: -1,
      disabledProblems: [3, 9],
      problems: [
        { id: 1, col: 0, title: 'Learners and Language of Instruction Learners and Language of Instruction ' },
        { id: 2, col: 0, title: 'Learners and Language of Instruction' },
        { id: 3, col: 0, title: 'Learners and Language of Instruction' },
        { id: 4, col: 0, title: 'Learners and Language of Instruction' },
        { id: 5, col: 1, title: 'Learners and Language of Instruction' },
        { id: 6, col: 1, title: 'Learners and Language of Instruction' },
        { id: 7, col: 1, title: 'Learners and Language of Instruction' },
        { id: 8, col: 2, title: 'Learners and Language of Instruction' },
        { id: 9, col: 2, title: 'Learners and Language of Instruction' }
      ],
      elements: [
        {
          x: 4,
          y: 5,
          ratio: 0.5,
          projects: [
            { id: 1, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 2, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 3, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 4, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 5, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 6, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' },
            { id: 7, title: 'Hoji Mobile Data Collection and Analysis Platform Hoji Mobile Data Collection and Analysis Platform' }
          ]
        },
        { x: 1, y: 4, ratio: 0.1, projects: [] },
        { x: 3, y: 4, ratio: 0.1, projects: [] },
        { x: 4, y: 4, ratio: 0.9, projects: [] },
        { x: 3, y: 3, ratio: 0.7, projects: [] },
        { x: 1, y: 1, ratio: 0.3, projects: [] }
      ]
    };
  },
  computed: {
    problemColumns () {
      return groupBy(this.problems, 'col');
    }
  },
  methods: {
    select (id, value) {
      if (value) {
        this.selectedProblem = id;
        return;
      }
      if (this.selectedProblem === id) {
        this.selectedProblem = -1;
      }
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";
.portfolio-area::v-deep {
  .move {
    display: none;
  }
  .actions .right .settings {
    margin: 0;
  }
}
section.portfolio-area {
  aside.filter-area {
    right: 0;
    position: absolute;
  }
}

.portfolio {
  //margin: 0 40px 160px 40px;
  margin-bottom: 80px;
  .PHeader {
    padding: 0 40px;
    background-color: white;
  }
  &::v-deep .el-tabs {
    .el-tabs__header {
      padding: 0 40px;
      background-color: white;
    }
    .el-tabs__nav-wrap::after {
      background-color: transparent;
    }
    .el-tabs__active-bar {
      height: 3px;
      background-color: #1CABE2;
    }
    .el-tabs__content {
      margin: 0 40px;
      padding-top: 40px;
    }
    .el-tabs__item {
      color: #777779;
      &.is-active, &:hover {
        color: #404041;
      }
      &:hover {
        font-weight: bold;
      }
    }
  }
  &::v-deep .el-tabs__nav {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;

   & > div:before {
    font-family: 'Font Awesome 5 Free';
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    display: inline-block;
    font-style: normal;
    font-feature-settings: normal;
    font-variant: normal;
    text-rendering: auto;
    line-height: 1;
    font-weight: 900;
    margin-right: 8px;
  }
  & > div:first-child {
    & + div {
      &:before {
        content: "\f2a1";
      }
    }
    & + div + div {
      &:before {
        content: "\f00a";
      }
    }
    & + div + div + div {
      &:before {
        content: "\f0db";
      }
    }
    & + div + div + div + div {
      &:before {
        content: "\f57c";
      }
    }
  }

  }
  span.Title {
    display: inline-block;
    cursor: pointer;
    font-size: 36px;
    color: #1CABE2;
    &:focus {
      outline: none;
    }
  }
  h2 {
    margin: 0;
    padding: 50px 0 24px 0;
    height: 45px;
    color: #1CABE2;
    font-size: 36px;
    letter-spacing: -1px;
    line-height: 45px;
    font-weight: normal;
    .el-icon-caret-bottom {
      font-size: 22px;
    }
  }
  .Problems {
    background-color: white;
    .Info {
      color: #777779;
      font-size: 12px;
      letter-spacing: 0;
      line-height: 15px;
      padding: 16px;
      .fa-info-circle {
        margin-right: 3px;
        font-size: 14px;
        color: #A8A8A9;
      }
    }
    .Problem {
      height: 100%;
      min-height: 560px;
      &.Problem1 {
        background-color: #CDEDF9;
        margin-right: 7px;
      }
      &.Problem2 {
        background-color: #ADE1F5;
        margin-right: 3px;
        margin-left: 3px;
      }
      &.Problem3 {
        margin-left: 7px;
        background-color: #7BCFEF;
      }
      & > .Title {
        color: #404041;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: -0.25px;
        line-height: 23px;
        text-align: center;
        padding: 29px 0;
        margin: 0;
      }
    }
  }
}
</style>
