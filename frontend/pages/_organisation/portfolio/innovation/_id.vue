<template>
  <div class="portfolio">
    <h2>
      Portfolio:
      <el-dropdown
        trigger="click"
        placement="bottom-end"
      >
        <span class="title el-dropdown-link">
          Learning<i class="el-icon-caret-bottom el-icon--right" />
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>Action 1</el-dropdown-item>
          <el-dropdown-item>Action 2</el-dropdown-item>
          <el-dropdown-item>Action 3</el-dropdown-item>
          <el-dropdown-item disabled>
            Action 4
          </el-dropdown-item>
          <el-dropdown-item divided>
            Action 5
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </h2>
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
        PROBLEM
      </el-tab-pane>
      <el-tab-pane
        label="MAP VIEW"
        name="map"
      >
        MAP
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Matrix from '@/components/portfolio/Matrix';
export default {
  components: {
    Matrix
  },
  data () {
    return {
      activeName: 'ambition',
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
        {
          x: 1,
          y: 4,
          ratio: 0.1,
          projects: []
        },
        {
          x: 3,
          y: 4,
          ratio: 0.1,
          projects: []
        },
        {
          x: 4,
          y: 4,
          ratio: 0.9,
          projects: []
        },
        {
          x: 3,
          y: 3,
          ratio: 0.7,
          projects: []
        },
        {
          x: 1,
          y: 1,
          ratio: 0.3,
          projects: []
        }
      ]
    };
  }
};
</script>

<style lang="less" scoped>
.portfolio {
  margin: 50px 40px 160px 40px;

  &::v-deep .el-tabs {
    .el-tabs__nav-wrap::after {
      background-color: transparent;
    }
    .el-tabs__active-bar {
      height: 3px;
    }
    .el-tabs__content {
      padding-top: 40px;
    }
  }
  &::v-deep .el-tabs__nav {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;

   & > div:before {
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    display: inline-block;
    font-style: normal;
    font-feature-settings: normal;
    font-variant: normal;
    text-rendering: auto;
    line-height: 1;
    font-family: 'Font Awesome 5 Free';
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
  .title {
    display: inline-block;
    cursor: pointer;
    font-size: 36px;
    color: #1CABE2;
    &:focus {
      outline: none;
    }
  }
  h2 {
    margin: 50px 0 24px 0;
    height: 45px;
    color: #1CABE2;
    font-size: 36px;
    letter-spacing: -1px;
    line-height: 45px;
    font-weight: normal;
  }
}
</style>
