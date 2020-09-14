<template>
  <el-dialog
    :title="$gettext('Scoring: Nutrition Information System') | translate"
    :visible="dialogScore"
    modal
    @close="setScoreDialog(false)"
  >
    <el-table :data="gridData">
      <el-table-column
        property="date"
        label="Date"
        width="150"
      ></el-table-column>
      <el-table-column
        property="name"
        label="Name"
        width="200"
      ></el-table-column>
      <el-table-column property="address" label="Address"></el-table-column>
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
      gridData: [
        {
          date: "2016-05-02",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        },
        {
          date: "2016-05-04",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        },
        {
          date: "2016-05-01",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        },
        {
          date: "2016-05-03",
          name: "John Smith",
          address: "No.1518,  Jinshajiang Road, Putuo District"
        }
      ]
    };
  },
  computed: {
    ...mapState({
      dialogScore: state => state.portfolio.dialogScore,
      currentProjectId: state => state.portfolio.currentProjectId
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
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.dialog-footer {
  display: flex;
  justify-content: space-between;
}
</style>
