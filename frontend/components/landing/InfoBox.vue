<template>
  <div class="InfoBox">
    <img
      :alt="$gettext('T4D and Innovation Inventory Platform') | translate"
      class="InfoPicture"
      src="/photo-whyusedha.jpg"
    />

    <div class="InfoArticle">
      <h3><translate>T4D and Innovation Inventory Platform</translate></h3>
      <p>
        <translate>
          The T4D and Innovation Inventory Platform (INVENT) is an open-source
          web platform designed to support goverments, technologists,
          implementers and donors to better coordinate digital health activities
          globally.
        </translate>
      </p>
      <p>
        <translate>
          This web platform offers users the information needed to improve the
          planning, coordination and use of digital health information systems
          for health.
        </translate>
      </p>
      <p>
        <translate>
          In addition, the INVENT supports implementers to assess the maturity
          of their digital health projects and gain access to global resources
          on current best practices in digital health.
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
