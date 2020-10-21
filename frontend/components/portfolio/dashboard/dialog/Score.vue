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
        <translate :parameters="{ name }"> Scoring: {name} </translate>
      </span>
      <button type="button" aria-label="Close" class="el-dialog__headerbtn">
        <i class="el-dialog__close el-icon el-icon-close"></i>
      </button>
    </template>
    <el-table :data="scoreTable" style="width: 100%" border>
      <el-table-column
        fixed
        prop="question"
        :label="$gettext('Questions') | translate"
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
              <p>{{ scope.row.question.text }}</p>
            </el-popover>
            <p>{{ scope.row.question.name }}</p>
            <fa
              v-popover:question
              class="question-icon"
              :icon="['fas', 'question-circle']"
            />
          </div>
        </template>
      </el-table-column>
      <!-- reviewers -->
      <el-table-column
        v-for="reviewer in reviewersName"
        :key="reviewer"
        :label="reviewer"
        :prop="reviewer"
        width="240"
        label-class-name="score-general-header"
        class-name="user-row"
      >
        <template slot-scope="scope">
          <template v-if="scope.row.type === 'psa'">
            <psa-list
              v-if="
                Array.isArray(scope.row[reviewer][scope.row.type]) &&
                scope.row[reviewer][scope.row.type].length
              "
              :items="scope.row[reviewer][scope.row.type]"
              :problem-statements="problemStatements"
            />
            <p v-else class="na psa">N/A</p>
          </template>
          <p v-else-if="scope.row[reviewer][scope.row.type]" class="user-score">
            {{ scope.row[reviewer][scope.row.type] }}
          </p>
          <p v-else class="na">N/A</p>
          <el-popover
            v-if="
              scope.row[reviewer][`${scope.row.type}_comment`] &&
              scope.row.type !== 'psa'
            "
            placement="right"
            :title="$gettext('Comment') | translate"
            width="360"
            trigger="hover"
            popper-class="score-popover"
          >
            <p>{{ scope.row[reviewer][`${scope.row.type}_comment`] }}</p>
            <fa
              v-if="scope.row[reviewer][`${scope.row.type}_comment`]"
              slot="reference"
              class="comment-icon"
              :icon="['fas', 'comment-alt']"
            />
          </el-popover>
        </template>
      </el-table-column>
      <!-- fake columns (if needed)  -->
      <el-table-column
        v-for="example in examples"
        :key="example"
        :label="$gettext(example) | translate"
        width="240"
        label-class-name="score-general-header"
        class-name="user-row"
      >
        <p class="na"></p>
      </el-table-column>
      <!-- reviewers -->
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
        :label="$gettext('Official Score') | translate"
        width="305"
        label-class-name="score-official"
        class-name="score-content score"
      >
        <template slot-scope="scope">
          <div :class="`content ${scope.row.type === 'psa' ? '' : 'center'}`">
            <template v-if="review.reviewed">
              <template v-if="scope.row.type === 'psa'">
                <psa-list
                  :items="score[scope.row.type]"
                  :problem-statements="problemStatements"
                />
              </template>
              <template v-else>
                <p class="statement">{{ reviewScoreText(scope.row.type) }}</p>
              </template>
            </template>
            <template v-else>
              <el-popover
                ref="guidance"
                placement="left"
                :title="$gettext('Scoring Guidance') | translate"
                width="360"
                trigger="hover"
                popper-class="score-popover left"
              >
                <p>{{ scope.row.question.guidance }}</p>
              </el-popover>
              <el-select
                v-if="scope.row.type === 'psa'"
                v-model="score[scope.row.type]"
                class="select-psa"
                multiple
                filterable
                clearable
                :disabled="review.reviewed"
              >
                <el-option
                  v-for="i in problemStatements"
                  :key="i.id"
                  :label="i.name"
                  :value="i.id"
                />
              </el-select>
              <el-select
                v-else-if="scope.row.type === 'scale_phase'"
                v-model="score[scope.row.type]"
                class="select-psa"
                clearable
                :disabled="review.reviewed"
              >
                <el-option
                  v-for="sp in scalePhases"
                  :key="sp.id"
                  :label="sp.name"
                  :value="sp.id"
                />
              </el-select>
              <el-select
                v-else
                v-model="score[scope.row.type]"
                clearable
                :disabled="review.reviewed"
              >
                <el-option v-for="i in points" :key="i" :label="i" :value="i" />
              </el-select>
              <fa
                v-popover:guidance
                class="question-icon"
                :icon="['fas', 'question-circle']"
              />
            </template>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <template v-if="!review.reviewed">
      <span slot="footer" class="dialog-footer">
        <el-button type="info" text @click="setScoreDialog(false)">
          <translate>Cancel</translate>
        </el-button>
        <el-button
          type="primary"
          :loading="loadingScore"
          :disabled="disabled"
          @click="handleScoreSubmit"
        >
          <translate>Submit Score</translate>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import PsaList from '@/components/portfolio/dashboard/table/PsaList'

export default {
  components: {
    PsaList,
  },
  data() {
    return {
      points: [1, 2, 3, 4, 5],
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
    }
  },
  computed: {
    ...mapState({
      dialogScore: (state) => state.portfolio.dialogScore,
      reviewQuestions: (state) => state.system.review_questions,
      name: (state) => state.portfolio.projectName,
      review: (state) => state.portfolio.review,
      loadingScore: (state) => state.portfolio.loadingScore,
      problemStatements: (state) => state.portfolio.problemStatements,
      questionType: (state) => state.portfolio.questionType,
      scalePhases: (state) => state.system.scalePhases,
    }),
    disabled() {
      if (this.review.reviewed) {
        return true
      }
      if (this.score.impact === null || this.score.impact === '') {
        return true
      }
      if (this.score.scale_phase === null || this.score.scale_phase === '') {
        return true
      }
      return (
        Object.values(this.score)
          .filter((i) => i !== null)
          .filter((i) => i !== '').length === 1 &&
        Object.values(this.score).filter((i) => Array.isArray(i) && i.length)
          .length === 0
      )
    },
    scoreTable() {
      return this.questionType.map((type) => {
        // will generate custom reviwers rows
        const reviewers = []
        if (this.review.review_scores) {
          this.review.review_scores.map((i) => {
            reviewers[i.reviewer.name] = {
              [type]: i[type],
              [`${type}_comment`]: i[`${type}_comment`],
            }
          })
        }
        // will return the custom score table
        return {
          question: this.reviewQuestions[type],
          type,
          ...reviewers,
          average: this.review.averages && this.review.averages[type],
        }
      })
    },
    reviewersName() {
      if (this.review.review_scores) {
        return this.review.review_scores.map((i) => i.reviewer.name)
      }
      return []
    },
    examples() {
      switch (this.reviewersName.length) {
        case 0:
          return ['', '']
        case 1:
          return ['']
        default:
          return []
      }
    },
  },
  methods: {
    ...mapActions({
      setScoreDialog: 'portfolio/setScoreDialog',
      addScore: 'portfolio/addScore',
    }),
    handleScoreSubmit() {
      this.addScore({ id: this.review.id, data: { ...this.score } })
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
      }
    },
    reviewScoreText(type) {
      if (type === 'scale_phase') {
        return this.scalePhases.find((i) => i.id === this.score[type]).name
      }
      return this.score[type] === null ? 'N/A' : this.score[type]
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

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
  .el-table__row:nth-last-child(2),
  .el-table__row:nth-last-child(1) {
    .question {
      background-color: #e8f6fd;
    }
  }
  .el-table td {
    &.question,
    &.score {
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
      }
    }
    &.user-row {
      .user-score {
        // display: inline-block;
        font-size: 14px;
        letter-spacing: 0;
        line-height: 21px;
        text-align: center;
        margin: 17px 0;
      }
      .na {
        text-align: center;
        color: #a8a8a9;
        font-size: 14px;
        letter-spacing: 0;
        line-height: 21px;
        margin: 17px 0;
        &.psa {
          margin-top: 0;
        }
      }
      .comment-icon {
        position: absolute;
        top: 29px;
        right: 35%;
        cursor: pointer;
        color: @colorBrandPrimary;
        font-size: 18px;
        &:hover {
          color: @colorTextPrimary;
        }
      }
    }
  }
}
</style>
