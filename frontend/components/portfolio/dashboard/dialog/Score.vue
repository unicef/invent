<template>
  <el-dialog
    :title="$gettext('Scoring: Nutrition Information System') | translate"
    :visible="dialogScore"
    modal
    width="1240px"
    height="1086px"
    @close="setScoreDialog(false)"
  >
    <el-table :data="scoreTable" style="width: 100%" border>
      <el-table-column
        fixed
        prop="question"
        label="Questions"
        width="250"
        label-class-name="score-general-header"
        class-name="question"
      >
        <template slot-scope="scope">
          <div class="content">
            <el-popover
              ref="question"
              placement="right"
              :title="$gettext('Question Description') | translate"
              width="360"
              trigger="hover"
              popper-class="score-popover"
            >
              <template>
                <p>{{ scope.row.question.text }}</p>
              </template>
            </el-popover>
            <p>{{ scope.row.question.name }}</p>
            <fa class="question-icon" :icon="['fas', 'question-circle']" v-popover:question />
            </el-tooltip>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="user1"
        label="user1"
        width="240"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="user2"
        label="user2"
        width="240"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="user3"
        label="user3"
        width="240"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="average"
        label="Average"
        width="85"
        label-class-name="score-average"
      >
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Official Score"
        width="305"
        label-class-name="score-official"
        class-name="score-content question"
      >
        <template slot-scope="scope">
          <div class="content center">
            <el-popover
              ref="question"
              placement="left"
              :title="$gettext('Scoring Guidance') | translate"
              width="360"
              trigger="hover"
              popper-class="score-popover left"
            >
              <template>
                <p>{{ scope.row.question.guidance }}</p>
              </template>
            </el-popover>
            <el-select
              v-model="review[scope.row.type]"
            >
              <el-option
                v-for="(item, i) in 5"
                :key="item"
                :label="i + 1"
                :value="i + 1"
              />
            </el-select>
            <fa class="question-icon" :icon="['fas', 'question-circle']" v-popover:question />
            </el-tooltip>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <span slot="footer" class="dialog-footer">
      <el-button @click="setScoreDialog(false)" text>
        Cancel
      </el-button>
      <el-button type="primary" @click="handleSubmit">
        <translate>Submit Score</translate>
      </el-button>
    </span>
  </el-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      review: {
        psa: "",
        rcni: "",
        ratp: "",
        ra: "",
        ee: "",
        nst: "",
        nc: "",
        ps: "",
        impact: "",
        scale_phase: "",
      },
    };
  },
  computed: {
    ...mapState({
      dialogScore: (state) => state.portfolio.dialogScore,
      currentProjectId: (state) => state.portfolio.currentProjectId,
      reviewQuestions: (state) => state.system.review_questions,
    }),

    scoreTable() {
      // return reviewQuestions;
      return [
        {
          question: this.reviewQuestions.psa,
          type: "psa",
          user: "Tom",
          average: 1,
        },
        {
          question: this.reviewQuestions.rnci,
          type: "rnci",
          user: "Chris",
          average: 3,
        },
        {
          question: this.reviewQuestions.ratp,
          type: "ratp",
          user: "Orsi",
          average: 2,
        },
        {
          question: this.reviewQuestions.ra,
          type: "ra",
          user: "Daniel",
          average: 5,
        },
        {
          question: this.reviewQuestions.ee,
          type: "ee",
          user: "David",
          average: 4,
        },
        {
          question: this.reviewQuestions.nst,
          type: "nst",
          user: "Elsa",
          average: 2,
        },
        {
          question: this.reviewQuestions.nc,
          type: "nc",
          user: "Kyle",
          average: 3,
        },
        {
          question: this.reviewQuestions.ps,
          type: "ps",
          user: "Kyle",
          average: 3,
        },
        {
          question: this.reviewQuestions.impact,
          type: "impact",
          user: "Kyle",
          average: 3,
        },
        {
          question: this.reviewQuestions.scale_phase,
          type: "scale_phase",
          user: "Kyle",
          average: 3,
        },
      ];
    },
  },
  methods: {
    ...mapActions({
      setScoreDialog: "portfolio/setScoreDialog",
      addScore: "portfolio/addScore",
    }),
    handleSubmit() {
      // todo: transform and add data
      this.addScore({ id: this.currentProjectId, data: {} });
    },
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
  },
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.dialog-footer {
  display: flex;
  justify-content: space-between;
}
.score-content {
  background-color: #eae6e1;
}
.score-average {
  background-color: #a8a8a9 !important;
}
.score-official {
  background-color: #374ea2 !important;
}
.score-general-header {
  border-right: 1px solid @colorWhite;
}
.cell.score-general-header {
  border-right: 1px solid transparent;
}
.score-popover.el-popover {
  padding: 0 !important;
  margin-left: 14px !important;
  &.left {
    margin-left: 0px !important;
    margin-right: 14px !important;
  }
  .el-popover__title {
    font-size: 18px;
    letter-spacing: -0.5px;
    line-height: 23px;
    padding: 20px;
    border-bottom: 1px solid #eae6e2;
  }
  p {
    font-size: 14px;
    letter-spacing: 0;
    line-height: 21px;
    padding: 17px 20px 23px;
  }
  .popper__arrow {
    display: inline;
  }
}
.el-table td {
  &.question {
    padding: 16.5px 12px !important;
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      &.center {
        justify-content: center;
        .question-icon {
          margin-left: 12px;
        }
      }
      p {
        margin-bottom: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        letter-spacing: 0 !important;
        line-height: 21px !important;
        min-width: 207px;
      }
      input {
        width: 90px;
      }
      .question-icon {
        cursor: pointer;
        color: #a8a8a9;
        font-size: 18px;
        &:hover {
          color: @colorTextPrimary;
        }
      }
    }
  }
}
</style>
