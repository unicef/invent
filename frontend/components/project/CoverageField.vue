<template>
  <div class="CoverageField">
    <el-row>
      <el-col :span="8">
        <simple-field
          :content="cov.health_workers"
          :header="$gettext('# Health Workers') | translate"
        />
      </el-col>
      <el-col :span="8">
        <simple-field
          :content="cov.facilities"
          :header="$gettext('# Facilities') | translate"
        />
      </el-col>
      <el-col :span="8">
        <simple-field
          :content="cov.clients"
          :header="$gettext('# Clients') | translate"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import SimpleField from './SimpleField'
export default {
  components: {
    SimpleField,
  },
  props: {
    coverage: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    cov() {
      return this.coverage || {}
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.CoverageField {
  .SimpleField {
    margin: 10px 0 !important;

    .Header {
      font-size: @fontSizeBase !important;
    }
  }
}
</style>
