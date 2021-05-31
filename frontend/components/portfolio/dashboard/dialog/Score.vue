<template>
  <el-dialog
    :visible="dialogScore"
    modal
    width="1240px"
    height="490px"
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
    <el-table :data="scoreTable" style="width: 100%" height="490px" border>
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
            <p>{{ scope.row.question.name }}</p>
            <info-popover
              ref="question"
              placement="right"
              :title="$gettext('Question Description') | translate"
              width="360"
            >
              <p>{{ scope.row.question.text }}</p>
              <p>
                <b>{{ scope.row.question.text_bold }}</b>
              </p>
            </info-popover>
          </div>
        </template>
      </el-table-column>
      <!-- reviewers -->
      <el-table-column
        v-for="reviewHeader in reviewHeaders"
        :key="reviewHeader.id"
        :label="reviewHeader.reviewer"
        :prop="reviewHeader.reviewer"
        width="240"
        label-class-name="score-general-header"
        class-name="user-row"
      >
        <template slot="header">
          <span>{{ reviewHeader.reviewer }}</span>
          <span class="to-right">
            <el-tooltip
              :content="
                $gettext(reviewStatuses[reviewHeader.status].title) | translate
              "
              placement="top"
            >
              <fa
                class="header-status-icon"
                :class="reviewStatuses[reviewHeader.status].class"
                :icon="reviewStatuses[reviewHeader.status].icon"
                size="lg"
              />
            </el-tooltip>

            <el-tooltip
              :content="$gettext('Delete Review Data') | translate"
              placement="top"
            >
              <confirm-popover
                placement="bottom"
                width="240"
                trigger="click"
                @confirmed="handleScoreDelete(reviewHeader)"
              />
            </el-tooltip>
          </span>
        </template>
        <template slot-scope="scope">
          <template v-if="scope.row.type === 'psa'">
            <psa-list
              v-if="
                Array.isArray(
                  scope.row[reviewHeader.reviewer][scope.row.type]
                ) && scope.row[reviewHeader.reviewer][scope.row.type].length
              "
              :items="scope.row[reviewHeader.reviewer][scope.row.type]"
              :problem-statements="problemStatements"
            />
            <!-- N/A -->
            <p v-else class="na psa"></p>
          </template>
          <p
            v-else-if="scope.row[reviewHeader.reviewer][scope.row.type]"
            class="user-score"
          >
            {{ scope.row[reviewHeader.reviewer][scope.row.type] }}
          </p>
          <!-- N/A -->
          <p v-else class="na"></p>
          <el-popover
            v-if="scope.row[reviewHeader.reviewer][`${scope.row.type}_comment`]"
            placement="right"
            :title="$gettext('Comment') | translate"
            width="360"
            trigger="hover"
            popper-class="score-popover"
          >
            <div class="text-info">
              <p>
                {{
                  scope.row[reviewHeader.reviewer][`${scope.row.type}_comment`]
                }}
              </p>
            </div>
            <fa
              v-if="
                scope.row[reviewHeader.reviewer][`${scope.row.type}_comment`]
              "
              slot="reference"
              :class="`comment-icon ${
                scope.row.type === 'psa' && 'comment-psa'
              }`"
              :icon="['fas', 'comment-alt']"
            />
          </el-popover>
        </template>
      </el-table-column>
      <!-- fake columns (if needed)  -->
      <el-table-column
        v-for="example in examples"
        :key="example"
        label=""
        width="240"
        label-class-name="score-general-header"
        class-name="user-row"
      >
        <p class="na"></p>
      </el-table-column>
      <!-- average -->
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
            <template v-if="review.approved">
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
              <el-select
                v-if="scope.row.type === 'psa'"
                v-model="score[scope.row.type]"
                class="select-psa"
                multiple
                filterable
                clearable
                :disabled="review.approved"
              >
                <el-option
                  v-for="i in problemStatements"
                  :key="i.id"
                  :label="i.name"
                  :value="i.id"
                  class="statement-options"
                />
              </el-select>
              <el-select
                v-else-if="scope.row.type === 'scale_phase'"
                v-model="score[scope.row.type]"
                class="select-psa"
                clearable
                :disabled="review.approved"
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
                :disabled="review.approved"
              >
                <el-option v-for="i in points" :key="i" :label="i" :value="i" />
              </el-select>
              <info-popover
                ref="guidance"
                placement="left"
                :title="$gettext('Scoring Guidance') | translate"
                width="360"
                popper-class="score-popover"
              >
                <p>{{ scope.row.question.guidance }}</p>
                <p>
                  <b>{{ scope.row.question.guidance_bold }}</b>
                </p>
              </info-popover>
            </template>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <template v-if="!review.approved">
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
import InfoPopover from '@/components/common/InfoPopover'
import ConfirmPopover from '@/components/common/ConfirmPopover'

export default {
  components: {
    PsaList,
    InfoPopover,
    ConfirmPopover,
  },
  data() {
    return {
      points: [1, 2, 3, 4, 5],
      reviewStatuses: {
        PD: {
          icon: ['fas', 'clock'],
          class: 'pending',
          title: 'Pending',
        },
        DR: {
          icon: ['fas', 'pen'],
          class: 'draft',
          title: 'Draft',
        },
        CMP: {
          icon: ['fas', 'clipboard-check'],
          class: 'complete',
          title: 'Completed',
        },
      },
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
      if (this.review.approved) {
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
          this.review.review_scores.forEach((i) => {
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
    reviewHeaders() {
      console.log(this.review.review_scores)
      if (this.review.review_scores) {
        return this.review.review_scores.map((i) => {
          return {
            reviewer: i.reviewer.name,
            status: i.status,
            id: i.id,
          }
        })
      }
      return []
    },
    examples() {
      switch (this.reviewHeaders.length) {
        case 0:
          return ['user example 1', 'user example 2']
        case 1:
          return ['user example 1']
        default:
          return []
      }
    },
  },
  methods: {
    ...mapActions({
      setScoreDialog: 'portfolio/setScoreDialog',
      addScore: 'portfolio/addScore',
      removeScore: 'portfolio/removeScore',
    }),
    handleScoreSubmit() {
      this.addScore({ id: this.review.id, data: { ...this.score } })
    },
    handleScoreDelete(reviewHeader) {
      console.log('reviewHeader', reviewHeader)
      this.removeScore({ ...reviewHeader })
        .then((res) => {
          this.$message({
            message: this.$gettext('Reviewer removed'),
            type: 'success',
          })
        })
        .catch((error) => {
          console.log(error)
          this.$message({
            message: this.$gettext('Error removing reviewer'),
            type: 'error',
          })
        })
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
      return this.score[type] === null ? ' ' : this.score[type] // N/A
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.dialog-score {
  top: 50%;
  transform: translateY(-50%);
  margin-top: 0 !important;

  .el-dialog__body {
    padding: 40px 60px 60px 60px !important;
    overflow: hidden !important;
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

  .to-right {
    float: right;
  }

  .header-status-icon {
    width: 16px;
    height: 16px;
    opacity: 0.8;
    position: relative;
    top: 0;
  }

  .header-status-icon:hover {
    opacity: 1;
  }

  .header-status-icon.pending {
    color: #b6e5f6;
  }

  .header-status-icon.draft {
    color: #fbde88;
  }

  .header-status-icon.complete {
    color: #71f4a9;
  }

  .header-icon-btn {
    background-color: white !important;
    color: red !important;
    padding: 2px !important;
    font-size: 12px;
    opacity: 0.8;
    margin-left: 8px;
  }

  .header-icon-btn:hover {
    opacity: 1;
  }

  .header-icon {
    width: 28px !important;
    height: 28px !important;
    cursor: pointer;
    opacity: 0.8;
    position: relative;
    top: 6px;
  }

  .header-icon:hover {
    opacity: 1;
  }

  .remove-icon {
    background-color: white;
    color: red;
    cursor: pointer;
    opacity: 0.8;
    outline: none;
    border-radius: 50%;
    padding: 2px;
  }

  .remove-icon:focus {
    outline-width: 0;
  }

  .remove-icon:hover {
    opacity: 1;
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
          .el-select__tags-text {
            max-width: 80px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            display: inline-block;
            vertical-align: middle;
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
        &.comment-psa {
          position: relative;
          top: 0;
          right: 0;
          margin: 6px 0;
          width: 100%;
          text-align: center;
        }
      }
    }
  }
}
</style>
