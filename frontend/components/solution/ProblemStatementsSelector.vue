<template>
  <el-select
    v-model="inputVal"
    multiple
    :placeholder="$gettext('Select Problem Statements') | translate"
    class="TeamSelector"
  >
    <el-option v-for="item in filteredStatements" :key="item.id" :label="item.name" :value="item.id"> </el-option>
  </el-select>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  model: {
    prop: 'tableData',
    event: 'change',
  },
  props: {
    tableData: {
      type: Array,
      default: [],
    },
    portfolio: {
      type: Number,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      getPortfolioList: 'solution/getPortfoliosList',
    }),
    filteredStatements: function () {
      if (this.portfolio === null) {
        return []
      } else {
        return this.getPortfolioList.find((statement) => statement.id === this.portfolio).problem_statements
      }
    },
    inputVal: {
      get() {
        return this.tableData
      },
      set(val) {
        this.$emit('change', val)
      },
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.TeamSelector {
  width: 100%;
  word-wrap: normal;
  el-select__tags {
    max-width: 200px;
  }
  .el-tag {
    height: fit-content;
    word-wrap: normal;
    white-space: normal;
  }
}
</style>
