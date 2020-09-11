<template>
  <div>
    <div v-for="item in items" class="reviewers">
      <div :class="`${item.completed && 'complete'}`">
        <p>
          <b>{{ item.name }}</b>
        </p>
        <p v-if="item.completed" class="uppercase">
          <translate>Complete</translate>
        </p>
        <p v-else class="uppercase pending">
          <translate>Pending</translate>
        </p>
      </div>
    </div>
    <p @click="handleReview(id)" class="assing">
      <fa icon="plus" />
      <translate>Assign Reviewers</translate>
    </p>

    <el-dialog title="Review" :visible.sync="dialogReview">
      <el-form :model="form">
        <el-form-item label="Promotion name" :label-width="formLabelWidth">
          <el-input v-model="form.name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="Zones" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="Please select a zone">
            <el-option label="Zone No.1" value="shanghai"></el-option>
            <el-option label="Zone No.2" value="beijing"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogReview = false">Cancel</el-button>
        <el-button type="primary" @click="dialogReview = false">
          Confirm
        </el-button>
      </span>
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
    items: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dialogReview: false,
      form: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: ""
      },
      formLabelWidth: "120px"
    };
  },
  methods: {
    handleReview(id) {
      console.log(`this will open item popup ${id}`);
      this.dialogReview = true;
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.reviewers {
  display: flex;
  flex-direction: column;
  & > div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }
}
.complete {
  color: #0eb455;
}
.pending {
  color: @colorBrandGrayDark;
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
