<template>
  <el-dialog
    :visible="dialogReview"
    modal
    width="800px"
    top="8vh"
    custom-class="review-dialog"
    @close="resetForm(false)"
    @open="handleReviewFeed()"
  >
    <!-- header -->
    <template slot="title">
      <div class="dialog-header">
        <p class="title"><translate>New reviewer</translate></p>
        <div class="info-wrapper">
          <review-state-info
            :complete="currentProjectReview.reviewed"
            portfolio="Portfolio Name B"
          />
        </div>
      </div>
    </template>
    <!-- content -->
    <div class="info-box">
      <fa class="info-icon" icon="info-circle" />
      <p>
        <b><translate>Brief Text Comes Here</translate>{{ ` ` }}</b>
        <translate>
          — Contra legem facit qui id facit quod lex prohibet. At nos hinc
          posthac, sitientis piros Afros. Fabio vel iudice vincam, sunt in culpa
          qui officia. Ab illo tempore, ab est sed immemorabili. Nihil hic
          munitissimus habendi senatus locus, nihil horum?
        </translate>
      </p>
    </div>
    <div
      v-for="(question, idx) in questionType"
      :key="question"
      class="question"
    >
      <p class="label">
        {{ `${idx + 1}/A: ` }}
        <translate>{{ reviewQuestions[question].name }}</translate>
      </p>
      <p class="sub-label">
        <translate>{{ reviewQuestions[question].text }}</translate>
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
        </info-popover>
      </div>
      <p class="label">
        {{ `${idx + 1}/B: ` }}<translate>Add comment (optional)</translate>
      </p>
      <el-input
        v-model="score[`${question}_comment`]"
        type="textarea"
        :rows="3"
        :placeholder="$gettext('Type here...') | translate"
      />
    </div>
    <!-- footer -->
    <span
      v-if="!currentProjectReview.reviewed"
      slot="footer"
      class="dialog-footer"
    >
      <el-button type="info" @click="resetForm(false)">Cancel</el-button>
      <el-button
        type="primary"
        :loading="loadingReview"
        :disabled="disabled"
        @click="handleSubmit"
      >
        <translate>Send</translate>
      </el-button>
    </span>
  </el-dialog>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'

import ReviewStateInfo from '@/components/review/ReviewStateInfo'
import InfoPopover from '@/components/common/InfoPopover'

export default {
  components: {
    ReviewStateInfo,
    InfoPopover,
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
        psa_comment: '',
        rnci_comment: '',
        ratp_comment: '',
        ra_comment: '',
        ee_comment: '',
        nst_comment: '',
        nc_comment: '',
        ps_comment: '',
        impact_comment: '',
        scale_phase_comment: '',
      },
    }
  },
  computed: {
    ...mapState({
      dialogReview: (state) => state.projects.dialogReview,
      currentProjectReview: (state) => state.projects.currentProjectReview,
      loadingReview: (state) => state.projects.loadingReview,
      questionType: (state) => state.portfolio.questionType,
      problemStatements: (state) => state.projects.problemStatements,
      reviewQuestions: (state) => state.system.review_questions,
    }),
    ...mapGetters({
      reviewersList: 'system/getUserProfilesNoFilter',
    }),
    disabled() {
      let disabled = false
      for (let i = 0; i < this.questionType.length; i++) {
        if (
          this.questionType[i] === 'psa' &&
          (!Array.isArray(this.score[this.questionType[i]]) ||
            !this.score[this.questionType[i]].length)
        ) {
          disabled = true
          break
        }
        if (
          this.score[this.questionType[i]] === null ||
          this.score[this.questionType[i]] === ''
        ) {
          disabled = true
          break
        }
      }
      return disabled
    },
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'projects/setReviewDialog',
      getProjects: 'projects/getProjects',
      // addReview: 'projects/addReview',
    }),
    resetForm(val) {
      this.setReviewDialog(val)
      this.reviewers = []
      this.message = ''
    },
    handleSubmit() {
      // this.addReview({
      //   id: this.currentProjectId,
      //   reviewers: this.reviewers,
      //   message: this.message,
      // })
    },
    handleReviewFeed() {
      // todo: use dynamic portfolio to get data
      this.getProjects(1)
      this.score = {
        psa: [2],
        rnci: 3,
        ratp: 5,
        ra: 1,
        ee: 2,
        nst: 4,
        nc: 1,
        ps: 2,
        impact: 3,
        scale_phase: 4,
        psa_comment: 'new comment',
        rnci_comment: 'new comment',
        ratp_comment: 'new comment',
        ra_comment: 'new comment',
        ee_comment: 'new comment',
        nst_comment: 'new comment',
        nc_comment: 'new comment',
        ps_comment: 'new comment',
        impact_comment: 'new comment',
        scale_phase_comment: 'new comment',
      }
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';

.el-dialog {
  .el-dialog__header {
    height: auto;
  }
  .el-dialog__body {
    max-height: 462px;
    overflow-y: scroll;
    padding: 40px 60px;
    // &::-webkit-scrollbar {
    //   display: none;
    // }
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
  .dialog-footer {
    display: flex;
    justify-content: space-between;
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
