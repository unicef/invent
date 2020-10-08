<template>
  <el-dialog
    :visible="dialogReview"
    modal
    width="800px"
    custom-class="review-dialog"
    @close="resetForm(false)"
  >
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
    <div class="content">
      <p class="label"><translate>Send Questionnaires to:</translate></p>
      <el-select
        v-model="reviewers"
        multiple
        :placeholder="
          $gettext('Type emails (separate with commas)') | translate
        "
      >
        <el-option
          v-for="item in reviewersList"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        >
        </el-option>
      </el-select>
      <p class="label"><translate>Add Message:</translate></p>
      <el-input
        v-model="message"
        type="textarea"
        :rows="8"
        :placeholder="$gettext('Type here...') | translate"
      />
    </div>

    <span
      v-if="!currentProjectReview.reviewed"
      slot="footer"
      class="dialog-footer"
    >
      <el-button text @click="resetForm(false)">Cancel</el-button>
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

export default {
  components: {
    ReviewStateInfo,
  },
  data() {
    return {
      reviewers: [],
      message: '',
    }
  },
  computed: {
    ...mapState({
      dialogReview: (state) => state.projects.dialogReview,
      currentProjectReview: (state) => state.projects.currentProjectReview,
      loadingReview: (state) => state.projects.loadingReview,
    }),
    ...mapGetters({
      reviewersList: 'system/getUserProfilesNoFilter',
    }),
    disabled() {
      if (this.reviewers.length > 0) {
        return false
      }
      return true
    },
  },
  methods: {
    ...mapActions({
      setReviewDialog: 'projects/setReviewDialog',
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
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.el-dialog .el-dialog__header {
  height: auto;
}

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

.label {
  font-size: 14px;
  font-weight: bold;
  letter-spacing: 0;
  line-height: 18px;
  margin: 0 0 20px;
}

.el-select,
input {
  width: 100%;
  margin-bottom: 40px;
}

.content {
  padding: 10px 30px !important;
}
.dialog-footer {
  display: flex;
  justify-content: space-between;
}
</style>
