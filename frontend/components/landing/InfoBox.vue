<template>
  <div class="InfoBox">
    <img
      :alt="$gettext('INVENT') | translate"
      class="InfoPicture"
      src="/photo-whyusedha.jpg"
    />

    <div class="InfoArticle">
      <h3><translate>INVENT</translate></h3>
      <p>
        <translate>
          INVENT is an open, global hub for Technology for Development and
          Innovation at UNICEF. The platform provides a searchable inventory of
          initiatives as well as a portfolio tool that provides a strategic view
          of UNICEF's priority areas for innovation.
        </translate>
      </p>
      <p>
        <translate>
          INVENT provides a global inventory designed to strengthen the value
          and impact of innovation and digital development investments, improve
          coordination, and facilitate institutionalization and scale.
        </translate>
      </p>
      <p>
        <translate>
          INVENT supports UNICEF’s Innovation Portfolio Approach focusing
          innovation on the most challenging problems UNICEF is trying to solve
          for and with children and young people. INVENT helps programme teams
          map, monitor and foster digital investments designed to meet UNICEF’s
          strategic goals and align with good programme and planning governance
          processes to help country and regional offices have oversight of
          innovation pipelines and initiatives being scaled with and across
          regions.
        </translate>
      </p>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.InfoBox {
  height: 100%;
  // background-image: url(/photo-whyusedha-bottom.jpg);
  // background-size: 115% auto;
  // background-repeat: no-repeat;
  // background-position: center bottom;

  .InfoPicture {
    width: 100%;
    max-height: 172px;
  }

  .InfoArticle {
    padding: 30px 40px 40px;

    h3 {
      color: @colorBrandPrimary;
      margin: 0px 0 24px 0;
      font-size: 24px;
      letter-spacing: -0.67px;
      line-height: 30px;
      font-weight: 300;
    }

    p {
      font-size: 16px;
      line-height: 21px;
      color: @colorTextPrimary;
      margin: 0 0 20px 0;
      letter-spacing: 0;
      line-height: 25px;
    }
  }
}
</style>
