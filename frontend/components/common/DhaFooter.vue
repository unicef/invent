<template>
  <div class="FooterBg">
    <div class="Footer">
      <el-row
        type="flex"
        justify-content="start"
        align="middle"
      >
        <el-col class="LogoWHO">
          <img
            src="/logo-who-gray-notext.svg"
            alt="WHO"
          >
        </el-col>
        <el-col class="Separator">
          <div />
        </el-col>
        <el-col class="Text">
          <span><translate>Disclaimer:</translate>&nbsp;</span>
          <span>
            <translate>All reasonable precautions have been taken by the World Health Organization to verify the information contained in this publication. However, the published material is being distributed without warranty of any kind, either expressed or implied. The responsibility for the interpretation and use of the material lies with the reader. In no event shall the World Health Organization be liable for damages arising from its use.</translate>
          </span>
          <nuxt-link :to="localePath({name: 'organisation-terms', params: $route.params})">
            <translate>Terms of use</translate>
          </nuxt-link>
        </el-col>
      </el-row>
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

  .FooterBg {
    display: flex;
    align-items: center;
    height: @appFooterHeight;
    background-color: @colorBrandGrayDark;

    .Footer {
      padding: 0 120px 0 40px;
      width: 100%;

      .LogoWHO {
        width: auto;

        img {
          height: 30px;
          transform: translateY(2px);
        }
      }

      .Separator {
        width: auto;
        height: 30px;

        > div {
          .SeparatorStyle();
          height: 100%;
          margin: 0 10px;
          background-color: fade(@colorGray, 35%);
        }
      }

      .Text {
        width: 100%;
        font-size: @fontSizeSmall - 1;
        line-height: 16px;
        color: @colorTextMuted;

        @media only screen and (max-width: 1360px) {
          font-size: @fontSizeSmall - 2;
          line-height: 15px;
        }
      }

      a {
        color: inherit;
        margin: 0 6px;
      }
    }
  }
</style>
