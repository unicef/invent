<template>
  <div class="LoginComponent">
    <el-card :body-style="{ padding: '0px' }">
      <div slot="header">
        <translate>Email confirmation</translate>
      </div>

      <p class="VerifyInstruction">
        <translate>Congratulations your email address is verified, you can now </translate>
        <span
          class="TextLink"
          @click="toLogin"
        >
          <translate>login</translate>
        </span>
        <translate>and use the system.</translate>
      </p>
    </el-card>
  </div>
</template>

<script>
export default {
  methods: {
    toLogin () {
      this.$router.push(this.localePath({ name: 'organisation-login', params: this.$route.params }));
    }
  }
};
</script>

<style lang="less">
  @import "../assets/style/variables.less";
  @import "../assets/style/mixins.less";

  .LoginComponent {
    width: @cardSizeSmall;
    margin: 80px auto;

    .VerifyInstruction {
      font-size: @fontSizeMedium;
      line-height: 24px;
      text-align: center;
      color: @colorTextPrimary;
      padding: 40px 80px;

      .TextLink {
        display: inline-block;
        margin: 0 5px;
        color: @colorBrandPrimary;
        cursor: pointer;
      }
    }
  }
</style>
