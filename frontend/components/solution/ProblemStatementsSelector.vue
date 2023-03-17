<template>
  <el-select
    v-model="statements"
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
    prop: 'value',
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
  data() {
    return {
      statements: [],
    }
  },
  computed: {
    ...mapGetters({
      //getStatements: 'solution/getProblemStatementList',
      getPortfolioList: 'solution/getPortfoliosList',
    }),
    filteredStatements: function () {
      if (this.portfolio === null) {
        return []
      } else {
        return this.getPortfolioList.find((statement) => statement.id === this.portfolio).problem_statements
      }
    },
  },
  mounted: function () {
    this.statements = this.tableData
  },

  methods: {
    changeHandler(value) {
      this.$emit('change', value)
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
