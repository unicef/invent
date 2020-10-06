<template>
  <div class="EmptyProjectList">
    <el-row type="flex">
      <el-col>
        <div class="SquareWrapper">
          <img src="~assets/img/icons-all.svg">
        </div>
      </el-col>
    </el-row>
    <el-row type="flex">
      <el-col>
        <nuxt-link
          :to="localePath({name: 'organisation-initiatives-create', params: $route.params})"
          tag="button"
          class="el-button el-button--primary el-button--medium"
        >
          <translate>Add new project</translate>
        </nuxt-link>
      </el-col>
    </el-row>
    <el-row type="flex">
      <el-col>
        <p>
          <translate>to include your project in the inventory</translate>
          <br>
          <translate>and begin tracking your performance</translate>
        </p>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {};
</script>

<style lang="less">
@import "../../assets/style/variables.less";
@import "../../assets/style/mixins.less";

.EmptyProjectList {
  text-align: center;

  img {
    margin: 20px 0 40px;
  }

  p {
    margin: 20px 0 60px;
    font-size: @fontSizeSmall;
    line-height: 18px;
    font-weight: 700;
    color: @colorTextSecondary;
  }
}
</style>
