<template>
  <article class="portfolio-main-title">
    <div>
      <h1>Manage your Portfolios</h1>
      <el-button
        v-if="profile.global_portfolio_owner"
        icon="el-icon-plus"
        type="primary"
        @click="handleLink"
      >
        <translate>Create a New Portfolio</translate>
      </el-button>
    </div>
    <p>
      <translate>
        Please select a Portfolio from the list above to edit its information,
        or change its status.
      </translate>
    </p>
  </article>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      profile: (state) => state.user.profile,
    }),
  },
  methods: {
    handleLink() {
      this.$router.push(
        this.localePath({ name: 'organisation-portfolio-management-new' })
      )
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.portfolio-main-title {
  width: 100%;
  margin-bottom: 60px;
  h1,
  p {
    margin: 0;
  }
  h1 {
    color: @colorBrandPrimary;
    font-size: 36px;
    letter-spacing: -1px;
    line-height: 45px;
    font-weight: 100;
  }
  p {
    color: @colorTextPrimary;
    font-size: 18px;
    letter-spacing: -0.25px;
    line-height: 27px;
  }
  div {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    button {
      align-self: center;
      height: 48px;
    }
  }
}
</style>
