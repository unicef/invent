<template>
  <el-card
    :class="[
      'QuestionContainer rounded',
      { Inactive: !question.is_active, Invalid: !valid, Edited: !saved },
    ]"
  >
    <!-- Actions -->
    <div class="Actions">
      <el-button
        :disabled="!valid || saved"
        type="text"
        class="IconLeft"
        @click="saveQuestion"
      >
        <fa icon="save" /> Save
      </el-button>
      <el-button
        type="text"
        class="DeleteButton IconLeft"
        @click="doDelete(id)"
      >
        <fa icon="trash" /> Delete
      </el-button>
    </div>

    <!-- Type -->
    <el-select v-model="question.type" :disabled="saved" placeholder="Type">
      <el-option :label="$gettext('Text field') | translate" :value="1" />
      <el-option :label="$gettext('Numeric field') | translate" :value="2" />
      <el-option :label="$gettext('Yes - no field') | translate" :value="3" />
      <el-option :label="$gettext('Single choice') | translate" :value="4" />
      <el-option :label="$gettext('Multiple choice') | translate" :value="5" />
    </el-select>

    <!-- Question -->
    <el-input
      v-model="question.question"
      :placeholder="$gettext('Question text') | translate"
    />

    <div class="QSwitches">
      <!-- Required -->
      <el-switch
        v-model="question.required"
        :active-text="$gettext('Required') | translate"
      />

      <el-switch
        v-model="question.is_private"
        :active-text="$gettext('Private') | translate"
      />
    </div>
    <dha-question-options
      v-if="question.type > 3"
      :disabled="saved"
      :options.sync="question.options"
    />

    <span :class="['DDHandler', { DraggingDisabled: !draggable }]">
      <fa icon="bars" />
    </span>
  </el-card>
</template>

<script>
import isEqual from 'lodash/isEqual'
import { mapGetters, mapActions } from 'vuex'
import DhaQuestionOptions from './DhaQuestionOptions'

export default {
  components: { DhaQuestionOptions },
  props: {
    id: {
      type: [String, Number],
      default: null,
    },
    draggable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      question: {
        type: '',
        question: '',
        options: [],
        required: false,
        is_private: false,
        is_active: true,
      },
    }
  },
  computed: {
    ...mapGetters({
      questionById: 'admin/questions/getQuestionById',
    }),
    stored() {
      if (this.id) {
        const stored = { ...this.questionById(+this.id) }
        stored.is_private = stored.private
        delete stored.private
        return stored
      }
      return null
    },
    valid() {
      return Boolean(
        this.question.type &&
          this.question.question.length &&
          (this.question.type < 4 || this.question.options.length)
      )
    },
    saved() {
      return isEqual(this.stored, this.question)
    },
  },
  watch: {
    stored: {
      immediate: true,
      handler(stored) {
        if (stored) {
          const options = stored.type > 3 ? [...stored.options] : []
          this.question = { ...stored, options }
        }
      },
    },
  },
  methods: {
    ...mapActions({
      createQuestion: 'admin/questions/createQuestion',
      updateQuestion: 'admin/questions/updateQuestion',
      deleteQuestion: 'admin/questions/deleteQuestion',
    }),
    async doDelete(id) {
      try {
        if (this.id) {
          await this.$confirm(
            this.$gettext('This will permanently delete the question?'),
            this.$gettext('Warning'),
            {
              confirmButtonText: this.$gettext('OK'),
              cancelButtonText: this.$gettext('Cancel'),
              type: 'warning',
            }
          )
        }
        await this.deleteQuestion(id)
        this.$message({
          type: 'success',
          message: this.$gettext('Question successfully deleted'),
        })
      } catch (e) {
        if (e === 'cancel') {
          this.$message({
            type: 'info',
            message: this.$gettext('Question deletion canceled'),
          })
        } else {
          this.$message({
            type: 'error',
            message: this.$gettext(
              'An error occured while deleting the question'
            ),
          })
        }
      }
    },
    async saveQuestion() {
      try {
        if (this.id) {
          await this.updateQuestion({ question: this.question, id: this.id })
        } else {
          await this.$confirm(
            this.$gettext(
              'This will save the question, type and options will not be editable anymore'
            ),
            this.$gettext('Warning'),
            {
              confirmButtonText: this.$gettext('OK'),
              cancelButtonText: this.$gettext('Cancel'),
              type: 'warning',
            }
          )
          await this.createQuestion(this.question)
        }
        this.$message({
          type: 'success',
          message: this.$gettext('Question successfully saved'),
        })
      } catch (e) {
        if (e === 'cancel') {
          this.$message({
            type: 'info',
            message: this.$gettext('Question saving canceled'),
          })
        } else {
          console.error(e)
          this.$message({
            type: 'error',
            message: this.$gettext(
              'An error occured while saving the question'
            ),
          })
        }
      }
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.QuestionContainer {
  position: relative;
  margin-bottom: 20px;
  padding-left: 24px;

  .Actions {
    position: absolute;
    right: 20px;
    top: 10px;

    .el-button {
      margin-left: 20px;
    }
  }

  &.Inactive {
    opacity: 0.8;
    background-color: @colorGrayLightest;
  }

  &.Edited {
    border-color: darken(@colorBrandBlueLight, 15%);
    background-color: @colorBrandBlueLight;
  }

  &.Invalid {
    border-color: @colorDanger;
    background-color: #feeceb;
  }

  .el-card__body {
    > div {
      margin-bottom: 20px;

      &:last-of-type {
        margin: 0;
      }
    }
  }

  .QSwitches {
    .el-switch {
      margin-right: 30px;
    }
  }

  .DDHandler {
    position: absolute;
    top: 0;
    left: 0;
    width: 24px;
    height: 100%;
    background-color: @colorGrayLighter;
    border-radius: 3px 0 0 3px;
    cursor: move;
    transition: @transitionAll;

    &.DraggingDisabled {
      cursor: not-allowed;
      &:hover,
      &:active {
        background-color: @colorGrayLighter;
        .svg-inline--fa {
          color: @colorGray;
        }
      }
    }

    &:hover,
    &:active {
      background-color: @colorBrandBlueLight;

      .svg-inline--fa {
        color: @colorBrandPrimary;
      }
    }

    .svg-inline--fa {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: @colorGray;
      transition: @transitionAll;
    }
  }
}

[dir='rtl'] {
  .QuestionContainer {
    padding-left: 0;
    padding-right: 24px;

    .Actions {
      left: 20px;
      right: auto;

      .el-button {
        margin-left: 0;
        margin-right: 20px;
      }
    }

    .QSwitches {
      .el-switch {
        margin-left: 30px;
        margin-right: 0;
      }
    }

    .DDHandler {
      left: auto;
      right: 0;
    }

    .el-switch__label.el-switch__label--right {
      margin-left: 0;
      margin-right: 10px;
    }
  }
}
</style>
