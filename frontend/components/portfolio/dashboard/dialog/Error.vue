<template>
  <el-dialog
    :title="$gettext('Unable to proceed action') | translate"
    :visible="dialogError"
    modal
    width="610px"
    custom-class="error"
    @close="setErrorDialog(false)"
  >
    <div class="content">
      <p>
        <translate>
          You are not able to move the selected project(s) to portfolio, because
          some of them have not been reviewd yet.
        </translate>
      </p>
      <p>
        <translate>
          Please complete your scores and try again!
        </translate>
      </p>
    </div>
  </el-dialog>
</template>

<script>
import { mapGetters, mapState, mapActions } from "vuex";
import PortfolioSelect from "@/components/portfolio/form/inputs/PortfolioSelect";

export default {
  components: {
    PortfolioSelect
  },
  data() {
    return {
      reviewers: [],
      message: ""
    };
  },
  computed: {
    ...mapState({
      dialogError: state => state.portfolio.dialogError
    })
  },
  methods: {
    ...mapActions({
      setErrorDialog: "portfolio/setErrorDialog"
    })
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";

.error {
  .el-dialog__header .el-dialog__title {
    color: @colorDanger;
  }
  .content {
    padding: 10px 30px calc(80px - 16px - 30px);
    p {
      margin: 0 0 16px;
      font-size: 14px;
      letter-spacing: 0;
      line-height: 21px;
    }
  }
}
</style>
