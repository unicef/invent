<template>
  <div class="InfoBox">
    <img
      :alt="$gettext('Why use the Digital Health Atlas') | translate"
      class="InfoPicture"
      src="/photo-whyusedha.jpg"
    >

    <div class="InfoArticle">
      <h3><translate>Why use the Digital Health Atlas?</translate></h3>
      <!-- <p class="Lead"><translate>This web platform supports issuing unique IDs for curating the range of digital health products and projects globally. Governments and communities of technologists, implementers, and donors will be equipped to better coordinate and plan, monitor the growth of implementations, and reduce redundancy of investments.</translate></p> -->
      <p><translate>The Digital Health Atlas (DHA) is an open-source web platform designed to support goverments, technologists, implementers and donors to better coordinate digital health activities globally.</translate></p>
      <!-- <p><translate>The Digital Health Atlas (DHA) offers governments, technologists, implementers, and donors a platform of tools and guidance to improve the use of, and planning coordination for digital information systems for health.</translate></p> -->
      <p><translate>This web platform offers users the information needed to improve the planning, coordination and use of digital health information systems for health. </translate></p>
      <!-- <p><translate>The DHA facilitates implementers to assess the maturity of their digital health implementations, gain personalized guidance, benefit from other’s implementation experiences, and gain access to global resources from leading technical institutions.</translate></p> -->
      <p><translate>In addition, the DHA supports implementers to assess the maturity of their digital health projects  and gain access to global resources on current best practices in digital health.</translate></p>
    </div>
  </div>
</template>

<script>
export default {

};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .InfoBox {
    height: 100%;
    background-image: url(/photo-whyusedha-bottom.jpg);
    background-size: 115% auto;
    background-repeat: no-repeat;
    background-position: center bottom;

    .InfoPicture {
      width: 100%;
      height: auto;
    }

    .InfoArticle {
      padding: 20px 40px;

      h3 {
        color: @colorTextPrimary;
        margin: 0 0 20px;
      }

      p {
        font-size: @fontSizeBase;
        line-height: 21px;
        color: @colorTextPrimary;
        margin: 0 0 20px;
      }
    }
  }
</style>
