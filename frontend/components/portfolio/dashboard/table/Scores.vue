<template>
  <div>
    <p @click="handleScore(id)" class="assing mb-10">
      <fa icon="list" />
      <translate>Change / view score</translate>
    </p>
    <p v-if="scores.completed" class="complete uppercase">
      <translate>Completed</translate>
    </p>

    <el-dialog title="Shipping address" :visible.sync="dialogScores">
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
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: true
    },
    scores: {
      type: Object,
      required: true
    }
  },
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
      ],
      dialogScores: false
    };
  },
  methods: {
    handleScore(id) {
      console.log(`this will open score popup ${id}`);
      this.dialogScores = true;
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.complete {
  color: #0eb455;
}
.uppercase {
  text-transform: uppercase;
  font-size: 10px !important;
}
.assing {
  display: flex;
  align-items: center;
  color: @colorBrandPrimary;
  cursor: pointer;
  &.mb-10 {
    margin-bottom: 10px !important;
  }
}
</style>
