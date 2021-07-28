<template>
  <el-popover
    v-model="visible"
    v-bind="{ ...$props, ...$attrs }"
    popper-class="score-popover"
    @show="handleSummaryFeed"
  >
    <div class="title-wrapper">
      <translate>Add Overall Summary</translate>
      <div class="close-btn" @click="visible = false">
        <i class="el-icon-close"></i>
      </div>
    </div>
    <div class="input-wrapper">
      <el-input
        v-model="overalSummary"
        type="textarea"
        maxlength="1024"
        show-word-limit
        :rows="8"
        :placeholder="$gettext('Type here...') | translate"
      />
    </div>
    <div class="action-wrapper">
      <el-button type="primary" size="small" @click="handleScoreSummarySubmit">
        <translate>Submit</translate>
      </el-button>
    </div>
    <el-button
      slot="reference"
      type="text"
      :icon="review.overall_reviewer_feedback ? 'el-icon-edit' : 'el-icon-plus'"
    >
      <translate v-if="review.overall_reviewer_feedback" key="edit">
        Edit feedback
      </translate>
      <translate v-else key="add">Add feedback</translate>
    </el-button>
  </el-popover>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      visible: false,
      overalSummary: '',
    }
  },
  computed: {
    ...mapState({
      review: (state) => state.portfolio.review,
    }),
  },
  methods: {
    ...mapActions({
      updateScoreSummary: 'portfolio/updateScoreSummary',
    }),
    handleSummaryFeed() {
      this.overalSummary = this.review.overall_reviewer_feedback
    },
    async handleScoreSummarySubmit() {
      try {
        await this.updateScoreSummary({
          id: this.review.id,
          overall_reviewer_feedback:
            this.overalSummary.trim() !== '' ? this.overalSummary : null,
        })
        this.visible = false
      } catch (error) {
        console.error(error)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.title-wrapper {
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  letter-spacing: -0.5px;
  line-height: 23px;
  padding: 20px;
  margin-bottom: 0;
  border-bottom: 1px solid #eae6e2;
  .close-btn {
    width: 16px;
    height: 16px;
    cursor: pointer;
    &:hover {
      color: #777779;
    }
  }
}
.input-wrapper {
  padding: 16px 20px;
  ::v-deep textarea {
    resize: none;
    word-break: normal;
  }
  ::v-deep .el-input__count {
    bottom: -32px;
    right: 0;
  }
}
.action-wrapper {
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  margin-bottom: 16px;
}
.normalized {
  cursor: pointer;
  font-weight: normal !important;
  font-size: 12px !important;
  line-height: 15px !important;
  white-space: pre-line;
}
</style>
