<template>
  <article class="portfolio-main-info">
    <div />
    <div>
      <h3>What is UNICEF’s portfolio approach to innovation?</h3>
      <p>
        <translate>
          Successful engagement in innovation requires focus and prioritization
          based on the greatest challenges facing children and young people.
          UNICEF’s portfolio approach makes evidence-based decisions about which
          problems to tackle based on programme-led analysis of areas most in
          need of acceleration solutions through new or significantly improved
          interventions. Innovations are then assessed against key criteria to
          identify solutions best suited to solving these challenges, resulting
          in portfolios that enable UNICEF to balance resources between scaling
          up tried-and-tested solutions and developing nascent solutions from
          the early stages.
        </translate>
      </p>
    </div>
  </article>
</template>

<script>
export default {
  methods: {},
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.portfolio-main-info {
  display: flex;
  background-color: @colorWhite;
  h3,
  p {
    margin: 0;
  }
  h3 {
    color: @colorBrandPrimary;
    font-size: 20px;
    letter-spacing: -0.5px;
    line-height: 24px;
    font-weight: 100;
    margin-bottom: 16px;
  }
  p {
    color: @colorTextPrimary;
    font-size: 16px;
    letter-spacing: -0.25px;
    line-height: 24px;
  }
  div:first-child {
    width: calc(1239px - 735px);
    background-image: url('~static/dashboard-info.jpg');
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    min-height: 100%;
  }
  div:last-child {
    width: 735px;
    padding: 35px 39px 40px;
  }
}
</style>
