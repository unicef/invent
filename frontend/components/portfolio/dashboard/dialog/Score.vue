<template>
  <el-dialog
    :title="$gettext('Scoring: Nutrition Information System') | translate"
    :visible="dialogScore"
    modal
    width="1240px"
    height="1086px"
    @close="setScoreDialog(false)"
  >
    <el-table :data="score" style="width: 100%" border>
      <el-table-column
        fixed
        prop="question"
        label="Questions"
        width="250"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="user"
        label="User"
        width="250"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="average"
        label="Average"
        width="250"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        prop="score"
        label="score"
        width="305"
        label-class-name="score-general-header"
      >
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Official Score"
        width="305"
        label-class-name="score-header"
        class-name="score-content"
      >
        <template slot-scope="scope">
          <el-button
            @click.native.prevent="deleteRow(scope.$index, score)"
            type="text"
            size="small"
          >
            Remove
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <span slot="footer" class="dialog-footer">
      <el-button @click="setScoreDialog(false)" text>
        Cancel
      </el-button>
      <el-button type="primary" @click="handleSubmit">
        <translate>Submit Score</translate>
      </el-button>
    </span>
  </el-dialog>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      // todo: nature of data is confusing and needs to be ask for it
      score: [
        {
          question: "Question 1",
          user: "Tom",
          average: 1,
          score: "N/A"
        },
        {
          question: "Question 2",
          user: "Chris",
          average: 3,
          score: "N/A"
        },
        {
          question: "Question 3",
          user: "Orsi",
          average: 2,
          score: "N/A"
        },
        {
          question: "Question 4",
          user: "Daniel",
          average: 5,
          score: "N/A"
        },
        {
          question: "Question 5",
          user: "David",
          average: 4,
          score: "N/A"
        },
        {
          question: "Question 6",
          user: "Elsa",
          average: 2,
          score: "N/A"
        },
        {
          question: "Question 7",
          user: "Kyle",
          average: 3,
          score: "N/A"
        }
      ]
    };
  },
  computed: {
    ...mapState({
      dialogScore: average => average.portfolio.dialogScore,
      currentProjectId: average => average.portfolio.currentProjectId
    })
  },
  methods: {
    ...mapActions({
      setScoreDialog: "portfolio/setScoreDialog",
      addScore: "portfolio/addScore"
    }),
    handleSubmit() {
      // todo: transform and add data
      this.addScore({ id: this.currentProjectId, data: {} });
    },
    deleteRow(index, rows) {
      rows.splice(index, 1);
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.dialog-footer {
  display: flex;
  justify-content: space-between;
}
.score-content {
  background-color: #eae6e1;
}
.score-header {
  background-color: #374ea2 !important;
}
.score-general-header {
  border-right: 1px solid @colorWhite;
}
.cell.score-general-header {
  border-right: 1px solid transparent;
}
</style>
