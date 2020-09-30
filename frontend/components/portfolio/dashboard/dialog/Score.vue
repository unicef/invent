<template>
  <el-dialog
    :visible="dialogScore"
    modal
    width="1240px"
    height="1086px"
    custom-class="dialog-score"
    @close="setScoreDialog(false)"
    @open="handleScoreFeed()"
  >
    <template slot="title">
      <span class="el-dialog__title">
        <translate :parameters="{ name }">
          Scoring: {name}
        </translate>
      </span>
      <button type="button" aria-label="Close" class="el-dialog__headerbtn">
        <i class="el-dialog__close el-icon el-icon-close"></i>
      </button>
    </template>
    <!-- {{ review }} -->
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
        <template slot-scope="scope">
          <p class="average">{{ scope.row.average }}</p>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Official Score"
        width="305"
        label-class-name="score-official"
        class-name="score-content question"
      >
        <template slot-scope="scope">
          <div :class="`content ${scope.row.type === 'psa' ? '' : 'center'}`">
            <template v-if="review.reviewed">
              <template v-if="scope.row.type === 'psa'">
                <ul class="psa-list">
                  <li v-for="statement in statements(score[scope.row.type])">
                    <fa class="triangle-icon" :icon="['fas', 'caret-right']" />
                    {{ statement.name }}
                  </li>
                </ul>
              </template>
              <template v-else>
                <p class="statement">{{ score[scope.row.type] === null ? 'N/A' : score[scope.row.type] }}</p>
              </template>
            </template>
            <template v-else>
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
                v-model="score[scope.row.type]"
                :class="`${scope.row.type === 'psa' && 'select-psa'}`"
                :multiple="scope.row.type === 'psa'"
                :filterable="scope.row.type === 'psa'"
                clearable
                :disabled="review.reviewed"
              >
                <el-option
                  v-if="scope.row.type === 'psa'"
                  v-for="i in problemStatements"
                  :key="i.id"
                  :label="i.name"
                  :value="i.id">
                </el-option>
                <el-option
                  v-else
                  v-for="(item, i) in 5"
                  :key="item"
                  :label="i + 1"
                  :value="i + 1"
                />
              </el-select>
              <fa class="question-icon" :icon="['fas', 'question-circle']" v-popover:question />
            </template>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <template v-if="!review.reviewed">
      <span slot="footer" class="dialog-footer">
        <el-button type="info" @click="setScoreDialog(false)" text>
          <translate>Cancel</translate>
        </el-button>
        <el-button type="primary" :loading="loadingScore" :disabled="disabled" @click="handleScoreSubmit">
          <translate>Submit Score</translate>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      score: {
        psa: [],
        rnci: null,
        ratp: null,
        ra: null,
        ee: null,
        nst: null,
        nc: null,
        ps: null,
        impact: null,
        scale_phase: null,
      },
    };
  },
  computed: {
    ...mapState({
      dialogScore: (state) => state.portfolio.dialogScore,
      reviewQuestions: (state) => state.system.review_questions,
      name: (state) => state.portfolio.projectName,
      review: (state) => state.portfolio.review,
      loadingScore: (state) => state.portfolio.loadingScore,
      problemStatements: (state) => state.portfolio.problemStatements,
    }),
    disabled() {
      if (this.review.reviewed) {
        return true;
      }
      if (this.score.impact === null || this.score.impact === "") {
        return true;
      }
      if (this.score.scale_phase === null || this.score.scale_phase === "") {
        return true;
      }
      return (
        Object.values(this.score)
          .filter((i) => i !== null)
          .filter((i) => i !== "").length === 1 &&
        Object.values(this.score).filter((i) => Array.isArray(i) && i.length)
          .length == 0
      );
    },
    scoreTable() {
      return [
        {
          question: this.reviewQuestions.psa,
          type: "psa",
          user: "Tom",
          average: this.review.averages && this.review.averages.psa,
        },
        {
          question: this.reviewQuestions.rnci,
          type: "rnci",
          user: "Chris",
          average: this.review.averages && this.review.averages.rnci,
        },
        {
          question: this.reviewQuestions.ratp,
          type: "ratp",
          user: "Orsi",
          average: this.review.averages && this.review.averages.ratp,
        },
        {
          question: this.reviewQuestions.ra,
          type: "ra",
          user: "Daniel",
          average: this.review.averages && this.review.averages.ra,
        },
        {
          question: this.reviewQuestions.ee,
          type: "ee",
          user: "David",
          average: this.review.averages && this.review.averages.ee,
        },
        {
          question: this.reviewQuestions.nst,
          type: "nst",
          user: "Elsa",
          average: this.review.averages && this.review.averages.nst,
        },
        {
          question: this.reviewQuestions.nc,
          type: "nc",
          user: "Kyle",
          average: this.review.averages && this.review.averages.nc,
        },
        {
          question: this.reviewQuestions.ps,
          type: "ps",
          user: "Kyle",
          average: this.review.averages && this.review.averages.ps,
        },
        {
          question: this.reviewQuestions.impact,
          type: "impact",
          user: "Kyle",
          average: this.review.averages && this.review.averages.impact,
        },
        {
          question: this.reviewQuestions.scale_phase,
          type: "scale_phase",
          user: "Kyle",
          average: this.review.averages && this.review.averages.scale_phase,
        },
      ];
    },
  },
  methods: {
    ...mapActions({
      setScoreDialog: "portfolio/setScoreDialog",
      addScore: "portfolio/addScore",
    }),
    handleScoreSubmit() {
      this.addScore({ id: this.review.id, data: { ...this.score } });
    },
    handleScoreFeed() {
      this.score = {
        psa: this.review.psa,
        rnci: this.review.rnci,
        ratp: this.review.ratp,
        ra: this.review.ra,
        ee: this.review.ee,
        nst: this.review.nst,
        nc: this.review.nc,
        ps: this.review.ps,
        impact: this.review.impact,
        scale_phase: this.review.scale_phase,
      };
    },
    statements(arr) {
      return this.problemStatements.filter((i) => arr.includes(i.id));
    },
  },
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.dialog-score {
  .el-dialog__body {
    padding: 40px 60px 60px 60px;
  }
  .dialog-footer {
    display: flex;
    justify-content: space-between;
  }
  .score-content {
    background-color: #e8f6fd;
  }
  .score-average {
    background-color: #a8a8a9 !important;
  }
  .average {
    font-size: 14px;
    text-align: center;
    margin: 18px 0 !important;
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
  .el-table__row:nth-last-child(2),
  .el-table__row:nth-last-child(1) {
    .question {
      background-color: #e8f6fd;
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
        .statement {
          text-align: center;
          font-weight: 100 !important;
          margin: 12px 0;
          width: 100%;
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
        .psa-list {
          margin: 0;
          padding: 0;
          list-style: none;
          li {
            font-size: 12px;
            margin-bottom: 4px;
          }
        }
        .select-psa {
          input {
            width: 250px;
          }
        }
        .question-icon {
          cursor: pointer;
          color: #a8a8a9;
          font-size: 18px;
          &:hover {
            color: @colorTextPrimary;
          }
        }
        .triangle-icon {
          color: #a8a8a9;
          margin-right: 5px;
        }
      }
    }
  }
}
</style>
