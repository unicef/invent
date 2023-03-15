<template>
  <el-select v-model="statements" multiple placeholder="Select" class="TeamSelector">
    <el-option v-for="item in getStatements" :key="item.id" :label="item.name" :value="item.id"> </el-option>
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
  },
  data() {
    return {
      statements: [],
    }
  },
  computed: {
    ...mapGetters({
      getStatements: 'solution/getProblemStatementList',
    }),
  },
  mounted: function () {
    this.statements = this.tableData
    console.log(this.getStatements)
  },
  methods: {
    changeHandler(value) {
      this.$emit('change', value)
    },
    statements: function (statementsArray) {
      console.log(this.getStatements)
      const st = statementsArray
        .map((statementId) => this.getStatements.find((statement) => statement.id === statementId).name)
        .toString()
      return st === '' ? 'N/A' : st
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.TeamSelector {
  width: 100%;
}
</style>
