<template>
  <article class="portfolio-main-info">
    <div />
    <div>
      <h3>What is a Portfolio?</h3>
      <p>
        <translate>
          Petierunt uti sibi concilium totius Galliae in diem certam indicere.
          Contra legem facit qui id facit quod lex prohibet. Nec dubitamus multa
          iter quae et nos invenerat. Qui ipsorum lingua Celtae, nostra Galli
          appellantur. Tu quoque, Brute, fili mi, nihil timor populi, nihil! At
          nos hinc posthac, sitientis piros Afros.
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
