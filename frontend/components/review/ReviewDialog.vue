<template>
  <el-dialog
    :visible="dialogReview"
    modal
    width="800px"
    top="8vh"
    custom-class="review-dialog"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    @close="resetForm(false)"
    @open="handleReviewFeed()"
  >
    <!-- header -->
    <template slot="title">
      <div class="dialog-header">
        <p class="title">{{ currentProjectReview.name }}</p>
        <div class="info-wrapper">
          <review-state-info
            :complete="currentProjectReview.complete"
            :portfolio="
              currentProjectReview.portfolio
                ? currentProjectReview.portfolio.name
                : ''
            "
          />
        </div>
      </div>
    </template>
    <!-- content -->
    <!-- review view -->
    <template v-if="currentProjectReview.complete">
      <div
        v-for="question in questionType"
        :key="question"
        class="question question-info"
      >
        <template v-if="!(question === 'impact' || question === 'scale_phase')">
          <div class="score-line">
            <p key="label" class="label">
              {{ reviewQuestions[question].name }}
            </p>
            <div class="divider"></div>
            <p v-if="question !== 'psa'" class="label">{{ score[question] }}</p>
          </div>
          <div v-if="question === 'psa'" class="statements-wrapper">
            <psa-list
              :items="score[question]"
              :problem-statements="problemStatements"
              big
            />
          </div>
          <p key="comment" class="comment">
            <template v-if="handleCommentShow(score, question)">
              <translate>(no comment)</translate>
            </template>
            <template v-else>
              <fa :icon="['fas', 'comment-alt']" />
              {{ score[`${question}_comment`] }}
            </template>
          </p>
        </template>
      </div>
    </template>
    <!-- review form -->
    <template v-else>
      <div class="info-box">
        <fa class="info-icon" icon="info-circle" />
        <p>
          <b><translate>Instructions</translate>{{ ` ` }}</b>
          <translate>
            — Please consult the detailed project information for this
            initiative in INVENT before completing the questionnaire. Carefully
            review each question and associated scoring guidance by hovering
            over the question mark icon. NOTE: Once questionnaire is submitted,
            it can no longer be changed. Please reach out to the portfolio
            manager with any questions.
          </translate>
        </p>
      </div>
      <div
        v-for="(question, idx) in questionType"
        :key="question"
        class="question"
      >
        <template v-if="!(question === 'impact' || question === 'scale_phase')">
          <p class="label">
            {{ `${idx + 1}/A: ` }}
            {{ reviewQuestions[question].name }}
            <translate>(optional)</translate>
          </p>
          <p class="sub-label">
            {{ reviewQuestions[question].text }}
          </p>
          <div class="select-box">
            <el-select
              v-if="question === 'psa'"
              v-model="score[question]"
              class="select-psa"
              multiple
              filterable
              clearable
            >
              <el-option
                v-for="i in problemStatements"
                :key="i.id"
                :label="i.name"
                :value="i.id"
              />
            </el-select>
            <el-select v-else v-model="score[question]" clearable>
              <el-option v-for="i in points" :key="i" :label="i" :value="i" />
            </el-select>
            <info-popover
              placement="right"
              :title="$gettext('Scoring Guidance') | translate"
              width="360"
            >
              <p>{{ reviewQuestions[question].guidance }}</p>
              <p>
                <b>{{ reviewQuestions[question].guidance_bold }}</b>
              </p>
            </info-popover>
          </div>
          <p class="label">
            {{ `${idx + 1}/B: ` }}<translate>Add comment (optional)</translate>
          </p>
          <el-input
            v-model="score[`${question}_comment`]"
            type="textarea"
            maxlength="255"
            show-word-limit
            :rows="4"
            :placeholder="$gettext('Type here...') | translate"
          />
        </template>
      </div>
    </template>
    <!-- footer -->
    <template
      v-if="!currentProjectReview.complete"
      slot="footer"
      class="dialog-footer"
    >
      <div v-if="!confirmPublishing" class="footer-wrapper">
        <span>
          <el-button type="info" @click="resetForm(false)">Cancel</el-button>
        </span>
        <span>
          <el-button type="primary" @click="handleSubmit('DR')">
            <translate>Save as Draft</translate>
          </el-button>
          <el-button type="success" @click="confirmPublishing = true">
            <translate>Save and Publish</translate>
          </el-button>
        </span>
      </div>
      <div v-else class="footer-wrapper confirm">
        <span class="confirm-text">
          <strong>Are you sure you want to publish?</strong> <br />
          Once submitted, the review can't be changed.
        </span>
        <span>
          <el-button text @click="confirmPublishing = false">Cancel</el-button>
          <el-button
            type="success"
            :loading="loadingReview"
            :disabled="disabled"
            @click="handleSubmit('CMP')"
          >
            <translate>Submit</translate>
          </el-button>
        </span>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'

import ReviewStateInfo from '@/components/review/ReviewStateInfo'
import InfoPopover from '@/components/common/InfoPopover'
import PsaList from '@/components/portfolio/dashboard/table/PsaList'

export default {
  components: {
    ReviewStateInfo,
    InfoPopover,
    PsaList,
  },
  data() {
    return {
      confirmPublishing: false,
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
        psa_comment: '',
        rnci_comment: '',
        ratp_comment: '',
        ra_comment: '',
        ee_comment: '',
        nst_comment: '',
        nc_comment: '',
        ps_comment: '',
      },
    }
  },
  computed: {
    ...mapState({
      dialogReview: (state) => state.projects.dialogReview,
      currentProjectReview: (state) => state.projects.currentProjectReview,
      loadingReview: (state) => state.projects.loadingReview,
      errorReview: (state) => state.projects.errorReview,
      questionType: (state) => state.portfolio.questionType,
      reviewQuestions: (state) => state.system.review_questions,
    }),
    ...mapGetters({
      reviewersList: 'system/getUserProfilesNoFilter',
    }),
    disabled() {
      const disabled = false
      // this.questionType.forEach((type) => {
      //   // we allow that psa is optional
      //   if (type !== 'psa') {
      //     if (this.score[type] === null || this.score[type] === '') {
      //       disabled = true
      //     }
      //   }
      // })
      return disabled
    },
    problemStatements() {
      return this.currentProjectReview.portfolio
        ? this.currentProjectReview.portfolio.problem_statements
        : []
    },
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'projects/setReviewDialog',
      addReview: 'projects/addReview',
    }),
    handleCommentShow(score, question) {
      return (
        score[`${question}_comment`] === '' ||
        score[`${question}_comment`] === null
      )
    },
    resetForm(val) {
      this.setReviewDialog(val)
      this.score = {
        psa: [],
        rnci: null,
        ratp: null,
        ra: null,
        ee: null,
        nst: null,
        nc: null,
        ps: null,
        psa_comment: '',
        rnci_comment: '',
        ratp_comment: '',
        ra_comment: '',
        ee_comment: '',
        nst_comment: '',
        nc_comment: '',
        ps_comment: '',
      }
    },
    async handleSubmit(status = 'DR') {
      await this.addReview({
        ...this.score,
        id: this.currentProjectReview.reviewId,
        status,
      })
      if (this.errorReview) {
        this.$message.error(
          this.$gettext('Opps, it seems your review have some errors.')
        )
      }
    },
    handleReviewFeed() {
      const {
        psa,
        rnci,
        ratp,
        ra,
        ee,
        nst,
        nc,
        ps,
        psa_comment,
        rnci_comment,
        ratp_comment,
        ra_comment,
        ee_comment,
        nst_comment,
        nc_comment,
        ps_comment,
      } = this.currentProjectReview
      this.score = {
        psa,
        rnci,
        ratp,
        ra,
        ee,
        nst,
        nc,
        ps,
        psa_comment,
        rnci_comment,
        ratp_comment,
        ra_comment,
        ee_comment,
        nst_comment,
        nc_comment,
        ps_comment,
      }
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.el-popconfirm__main {
  width: 250px;
}

.el-dialog {
  .el-dialog__header {
    height: auto;
  }
  .el-dialog__body {
    max-height: 462px;
    overflow-y: scroll;
    padding: 40px 60px;
  }
}

.review-dialog {
  .dialog-header {
    .title {
      font-size: 20px;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 32px;
      color: @colorBrandPrimary;
      padding-top: 20px;
      margin-bottom: 8px;
    }
    .info-wrapper {
      height: 20px;
      margin-bottom: 16px;
    }
  }
  .el-dialog__footer {
    padding: 0 !important;

    .footer-wrapper {
      display: flex;
      justify-content: space-between;
      flex: 1;
      padding: 12px;
    }
    .footer-wrapper.confirm {
      background-color: #fff2cc;
    }
    .confirm-text {
      font-size: 14px;
      text-align: left;
      padding-left: 12px;
    }
  }

  .info-box {
    display: flex;
    padding-bottom: 35px;
    border-bottom: 1px solid #eae6e1;
    p {
      margin: 0;
      color: @colorBrandGrayDark;
      font-size: 14px;
      letter-spacing: 0;
      line-height: 21px;
    }
    .info-icon {
      color: #a8a8a9;
      font-size: 18px;
      margin-top: 2px;
      margin-right: 6px;
    }
  }
  .question {
    margin-top: 40px;
    &.question-info {
      margin: 0 0 30px;
    }
    .label,
    .sub-label {
      font-size: 14px;
      letter-spacing: 0;
      line-height: 18px;
      margin: 0 0 20px;
    }
    .label {
      font-weight: bold;
    }
    .score-line {
      display: flex;
      justify-content: space-between;
      .divider {
        flex-grow: 1;
        height: 1px;
        border-bottom: 1px solid #eae6e1;
        align-self: flex-end;
        margin: 0 10px 22px;
      }
    }
    .statements-wrapper {
      padding: 0 16px 15px;
    }
    .comment {
      color: @colorBrandGrayDark;
      font-size: 14px;
      letter-spacing: 0;
      line-height: 20px;
      margin: 0;
      padding: 0 16px;
      svg {
        color: #a8a8a9;
        margin-right: 6px;
      }
    }
    .select-box {
      display: flex;
      align-items: center;
      margin: 0 0 20px;
      .el-select {
        width: 240px;
        margin-right: 16px;
        input {
          width: 240px;
        }
        &.select-psa {
          width: 640px;
          input {
            width: 640px;
          }
        }
      }
    }
  }
}
</style>
