<template>
  <div class="SubLevelItem">
    <el-row>
      <simple-field :header="levelName" :content="subLevel.name" />
    </el-row>
    <el-row>
      <coverage-field :coverage="localCoverageData" />
    </el-row>
  </div>
</template>

<script>
import SimpleField from './SimpleField'
import CoverageField from './CoverageField'

export default {
  components: {
    SimpleField,
    CoverageField,
  },
  props: {
    levelName: {
      type: String,
      required: true,
    },
    subLevels: {
      type: Array,
      default: () => [],
    },
    coverage: {
      type: [String, Number],
      default: null,
    },
    coverageData: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    subLevel() {
      const level = this.subLevels.find(
        (s) => s.id === this.coverage || s.name === this.coverage
      )
      if (level) {
        return level
      }
      console.error('Misisng sub level, probable corrupt map data')
      return {}
    },
    localCoverageData() {
      return this.coverageData[this.coverage]
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SubLevelItem {
}

.SubLevelItemDropdown {
}
</style>
