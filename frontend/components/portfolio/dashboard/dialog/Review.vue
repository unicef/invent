<template>
  <el-dialog
    :title="$gettext('Assign Reviewer') | translate"
    :visible="dialogReview"
    modal
    width="610px"
    @close="resetForm(false)"
  >
    <div class="content">
      <p class="label"><translate>Send Questionnaires to:</translate></p>
      <el-select
        v-model="reviewers"
        multiple
        filterable
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

    <span slot="footer" class="dialog-footer">
      <el-button text @click="resetForm(false)">Cancel</el-button>
      <el-button
        type="primary"
        :loading="loadingAddReviewers"
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

export default {
  data() {
    return {
      reviewers: [],
      message: '',
    }
  },
  computed: {
    ...mapState({
      dialogReview: (state) => state.portfolio.dialogReview,
      currentProjectId: (state) => state.portfolio.currentProjectId,
      loadingAddReviewers: (state) => state.portfolio.loadingAddReviewers,
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
      setReviewDialog: 'portfolio/setReviewDialog',
      addReview: 'portfolio/addReview',
    }),
    resetForm(val) {
      this.setReviewDialog(val)
      this.reviewers = []
      this.message = ''
    },
    handleSubmit() {
      this.addReview({
        id: this.currentProjectId,
        reviewers: this.reviewers,
        message: this.message,
      })
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

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
