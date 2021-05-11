<template>
  <el-popover v-model="visible" v-bind="{ ...$props, ...$attrs }">
    <div>
      <p class="confirm-text">
        <translate>
          Be aware that removing the reviewer, also deletes all scores the
          reviewer saved. Are you sure you want to remove all review data?
        </translate>
      </p>
      <div>
        <el-button text size="mini" @click="visible = false">
          <translate>Cancel</translate>
        </el-button>
        <el-button type="danger" text size="mini" @click="confirm">
          <translate>Yes, remove all</translate>
        </el-button>
      </div>
    </div>
    <el-button
      slot="reference"
      icon="el-icon-close"
      circle
      class="header-icon-btn"
    ></el-button>
  </el-popover>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
    }
  },
  methods: {
    confirm() {
      this.$emit('confirmed')
      this.visible = false
    },
  },
}
</script>

<style lang="less" scoped>
.confirm-text {
  margin-top: 0;
  font-size: 0.9em;
  font-weight: 500;
  text-align: left !important;
}
</style>
