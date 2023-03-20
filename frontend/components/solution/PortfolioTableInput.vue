<template>
  <div>
    <table data-test="portfolio-table-input" class="SimpleTable">
      <thead>
        <tr>
          <th><translate>Innovation Portfolio</translate></th>
          <th><translate>Problem Statements</translate></th>
          <th>&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in innerValue" :key="row.portfolio_id">
          <td>
            <PortfolioSelectSingle v-model.number="row.portfolio_id" :portfoliosList="innerValue" />
          </td>
          <td>
            <ProblemStatementsSelector v-model="row.problem_statements" :portfolio="row.portfolio_id" />
          </td>
          <td>
            <el-button type="text" class="IconLeft" @click="() => deleteRow(row.portfolio_id)">
              <translate>Delete</translate>
            </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <el-button type="text" class="IconLeft" @click="addRow">
      <fa icon="plus" /> <translate>Add Portfolio</translate>
    </el-button>
  </div>
</template>

<script>
//import { uuidv4 } from '~/utilities/dom'
import PortfolioSelectSingle from './PortfolioSelectSingle.vue'
import { mapGetters } from 'vuex'
import ProblemStatementsSelector from './ProblemStatementsSelector.vue'

export default {
  components: {
    PortfolioSelectSingle,
    ProblemStatementsSelector,
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: ['value'],
  computed: {
    ...mapGetters({
      getStatements: 'solution/getProblemStatementList',
    }),
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
  },

  methods: {
    addRow: function () {
      const newValue = [...this.value, { portfolio_id: null, problem_statements: [] }]
      this.$emit('change', newValue)
    },
    deleteRow: function (id) {
      const newValue = this.value.filter((row) => row.portfolio_id !== id)
      this.$emit('change', newValue)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SimpleTable {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  thead {
    background-color: gray;
    color: white;
    text-align: left;

    th {
      padding-left: 10px;
    }
  }
  td {
    padding-left: 10px;
  }
  th:nth-child(1) {
    width: 30%;
  }
  th:nth-child(2) {
    width: 60%;
  }
  th:nth-child(3) {
    width: 10%;
  }
  tr:nth-child(even) {
    background-color: lightgrey;
  }
}
</style>
