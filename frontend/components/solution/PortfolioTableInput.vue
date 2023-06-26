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
        <tr v-for="(row, index) in innerValue" :key="index" :data-test="`portfolio-row-${index}`">
          <td>
            <PortfolioSelectSingle
              v-model.number="row.portfolio_id"
              :portfoliosList="innerValue"
              v-validate="rules.portfolioSingleSelect"
              name="portfolio-single-select"
              :data-test="`portfolio-select-single-${index}`"
            />
          </td>
          <td>
            <ProblemStatementsSelector
              v-model="row.problem_statements"
              :portfolio="row.portfolio_id"
              v-validate="rules.problemStatementSelect"
              name="problem-statement-select"
              :data-test="`problem-statement-${index}`"
            />
          </td>
          <td>
            <el-button
              type="text"
              class="IconLeft"
              @click="() => deleteRow(index)"
              :data-test="`delete-portfolio-row-${index}`"
            >
              <translate>Delete</translate>
            </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-show="error" class="error">
      <translate>At least one Innovation Portfolio and Problem Statement are required.</translate>
    </p>
    <p v-show="errors.first('portfolio-single-select')" class="error">
      <translate>Innovation Portfolio, cannot be empty.</translate>
    </p>
    <p v-show="errors.first('problem-statement-select')" class="error">
      <translate>Problem Statements, cannot be empty.</translate>
    </p>
    <el-button type="text" class="IconLeft" @click="addRow" data-test="add-portfolio-row-button">
      <fa icon="plus" /> <translate>Add Portfolio</translate>
    </el-button>
  </div>
</template>

<script>
//import { uuidv4 } from '~/utilities/dom'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '@/components/mixins/ProjectFieldsetMixin.js'
import PortfolioSelectSingle from './PortfolioSelectSingle.vue'
import { mapGetters } from 'vuex'
import ProblemStatementsSelector from './ProblemStatementsSelector.vue'
import { draftRules, publishRules } from '~/utilities/projects'

export default {
  components: {
    PortfolioSelectSingle,
    ProblemStatementsSelector,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  model: {
    prop: 'value',
    event: 'change',
  },
  props: ['value', 'error', 'rules', 'publishRules', 'draftRules', 'apiErrors'],
  $_veeValidate: {
    value() {
      return this.innerValue
    },
    //  rejectsFalse: true,
  },
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
      let arr = [...this.value]
      arr.splice(id, 1)

      this.$emit('change', arr)
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
.error {
  color: red;
  font-size: @fontSizeBase;
}
</style>
