<template>
  <div class="portfolio">
    <div class="title">
      <nuxt-link
        :to="localePath({ name: 'organisation-portfolio-management' })"
      >
        <fa icon="angle-left" size="sm" />
        <translate>Back</translate>
      </nuxt-link>
      <h2><translate>Create new portfolio</translate></h2>
    </div>
    <new-portfolio-form />
  </div>
</template>

<script>
import NewPortfolioForm from '@/components/portfolio/form/NewPortfolioForm'

export default {
  components: {
    NewPortfolioForm,
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.portfolio {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 1032px;
  margin: 50px auto 160px;
  .title {
    display: flex;
    align-items: center;
    margin-bottom: 50px;
    h2 {
      color: @colorBrandPrimary;
      font-size: 36px;
      letter-spacing: -1px;
      line-height: 45px;
      font-weight: 100;
      flex-grow: 2;
      text-align: center;
    }
    a {
      font-size: @fontSizeBase;
      text-decoration: none;
    }
  }
}
</style>
