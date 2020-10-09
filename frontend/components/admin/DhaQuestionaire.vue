<template>
  <div>
    <div class="QuestionnaireWrapper">
      <draggable
        v-model="questions"
        :options="draggableOptions"
        :move="moveHandler"
      >
        <dha-question
          v-for="(question, index) in questions"
          :id="question.id"
          :key="index"
          :draggable="allSaved"
        />
      </draggable>
    </div>

    <el-row type="flex" align="middle" class="QActionContainer">
      <el-col class="QActionsButtons">
        <el-tooltip
          :disabled="allSaved"
          :content="
            $gettext(
              'Before adding another question please save the previous one'
            ) | translate
          "
          placement="top"
        >
          <span>
            <el-button
              :disabled="!allSaved"
              type="text"
              class="IconLeft"
              @click="addQuestion"
            >
              <fa icon="plus" />
              <translate>Add new question</translate>
            </el-button>
          </span>
        </el-tooltip>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import draggable from 'vuedraggable'
import DhaQuestion from './DhaQuestion'

export default {
  components: {
    DhaQuestion,
    draggable,
  },

  data() {
    return {
      from: null,
      to: null,
    }
  },

  computed: {
    ...mapGetters({
      getQuestions: 'admin/questions/getQuestions',
    }),
    allSaved() {
      return !!this.questions.reduce((a, c) => a && c.id, true)
    },
    draggableOptions() {
      return {
        disabled: !this.allSaved,
        handle: '.DDHandler',
      }
    },
    questions: {
      get() {
        return this.getQuestions
      },
      async set(newOrder) {
        this.$nuxt.$loading.start()
        try {
          await this.processReOrder({ from: this.from, to: this.to, newOrder })
          this.$message({
            message: this.$gettext('New order saved'),
            type: 'success',
          })
        } catch (e) {
          this.$message.error(
            this.$gettext('An error occured while processing your request')
          )
        }
        setTimeout(() => {
          this.$nuxt.$loading.finish()
        }, 500)
      },
    },
  },

  methods: {
    ...mapActions({
      addQuestion: 'admin/questions/addQuestion',
      processReOrder: 'admin/questions/processReOrder',
    }),
    moveHandler(evt, originalEvt) {
      this.from = evt.draggedContext.index
      this.to = evt.draggedContext.futureIndex
      return true
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

// .QuestionnaireWrapper {}

.QActionContainer {
  .QActionsButtons {
    width: 100%;

    .el-button {
      margin: 0 20px;
    }
  }

  .QAlerts {
    width: auto;
    text-align: right;

    .el-alert {
      .el-alert__title {
        padding-right: 20px;
        font-size: @fontSizeSmall;
        white-space: nowrap;
      }
    }
  }
}
</style>
