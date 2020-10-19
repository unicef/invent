<template>
  <section class="portfolio-main">
    <h1>
      <translate>What is UNICEF’s Approach of Portfolio Management</translate>
    </h1>
    <h2>
      <translate>Explore Our Portfolio-Driven Portfolios</translate>
    </h2>
    <p>
      <translate>
        Our priority portfolios for innovation are driven by the key problems we
        seek to solve for children. Please select a problem statement from one
        of the portfolios below to learn more.
      </translate>
    </p>
    <p>
      <translate>
        Dynamically populated based on the portfolio data set.
      </translate>
    </p>

    <el-collapse v-model="activeNames" accordion class="MainAccordion">
      <el-collapse-item v-for="index in ['1', '2']" :key="index" :name="index">
        <div slot="title" class="AccordionTitle">
          <span class="accordion-status"></span>
          <span class="icon-circle icon-tiip-innovation">&nbsp;</span>
          <span class="portfolio-title">Consistency</span>
          <nuxt-link to="/">
            <translate>View Portfolio</translate>
          </nuxt-link>
        </div>
        <div class="AccordionContent">
          <el-row>
            <el-col :span="12" class="col-container">
              <div class="col-title">
                <translate>Problem Statements</translate>
              </div>
              <el-collapse
                v-model="activeNamesTemp"
                accordion
                class="SubAccordion"
              >
                <el-collapse-item name="1">
                  <div slot="title" class="SubAccordionTitle">
                    Addressing Management challenges
                  </div>
                  <div class="SubAccordionContent">
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                  </div>
                </el-collapse-item>
                <el-collapse-item name="2">
                  <div slot="title" class="SubAccordionTitle">
                    Addressing Management challenges
                  </div>
                  <div class="SubAccordionContent">
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                    Lore ipsumLore ipsumLore ipsumLore ipsumLore ipsumLore ipsum
                  </div>
                </el-collapse-item>
              </el-collapse>
            </el-col>
            <el-col :span="12" class="col-container">
              <div class="col-title">
                <translate>Summary</translate>
              </div>
              <p class="summary">
                Quid securi etiam tamquam eu fugiat nulla pariatur. Vivamus
                sagittis lacus vel augue laoreet rutrum faucibus. Contra legem
                facit qui id facit quod lex prohibet. Gallia est omnis divisa in
                partes tres, quarum. Pellentesque habitant morbi tristique
                senectus et netus. Donec sed odio operae, eu vulputate felis
                rhoncus.Curabitur est gravida et libero vitae dictum. Cum
                ceteris in veneratione tui montes, nascetur mus. Ab illo
                tempore, ab est sed immemorabili. Lorem ipsum dolor sit amet,
                consectetur adipisici elit, sed eiusmod tempor incidunt ut
                labore et dolore magna aliqua. Qui ipsorum lingua Celtae, nostra
                Galli appellantur.
              </p>
              <div class="col-title">
                <translate>Contact person</translate>
              </div>
              <div class="contact">
                Edson Monteiro <br />
                <a href="mailto:emonterio@unicef.org">emonterio@unicef.org</a>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-collapse-item>
    </el-collapse>
  </section>
</template>

<script>
export default {
  data() {
    return {
      activeNames: '1',
      activeNamesTemp: '1',
    }
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

h1 {
  color: @colorBrandPrimary;
  font-size: 36px;
  letter-spacing: -1px;
  line-height: 45px;
  font-weight: 100;
}
h2 {
  height: 30px;
  color: @colorTextPrimary;
  font-size: 24px;
  letter-spacing: -0.67px;
  line-height: 30px;
  font-weight: normal;
}
p {
  color: @colorTextPrimary;
  font-size: 18px;
  letter-spacing: -0.25px;
  line-height: 27px;
}
.portfolio-main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 1242px;
  margin: 50px auto 170px;

  &::v-deep {
    .SubAccordion {
      .el-collapse-item__content {
        padding-bottom: 0 !important;
      }
    }
  }
  .SubAccordion {
    border-width: 0;
    .SubAccordionTitle {
      height: 21px;
      color: #404041;
      font-size: 14px;
      font-weight: normal;
      letter-spacing: -0.25px;
      line-height: 21px;
      &::before {
        content: '+';
        font-size: 22px;
        font-weight: normal;
        letter-spacing: -2px;
        padding-right: 10px;
      }
    }
    .SubAccordionContent {
      padding-left: 40px;
      height: 80px;
      color: @colorBrandGrayDark;
      font-size: 13px;
      letter-spacing: 0;
      line-height: 20px;
    }
    .el-collapse-item.is-active {
      .SubAccordionTitle {
        font-weight: bold;
        &::before {
          content: '--';
        }
      }
    }
  }
  .AccordionContent {
    border-top: 1px solid @colorGrayLight;
    padding: 20px 0;
    .col-container {
      color: @colorTextPrimary;
      padding-left: 32px;
      .col-title {
        margin: 3px 0 16px 0;
        padding: 0;
        height: 23px;
        font-size: 18px;
        letter-spacing: -0.5px;
        line-height: 23px;
      }
      .summary {
        height: 189px;
        color: @colorTextPrimary;
        font-size: 14px;
        letter-spacing: -0.25px;
        line-height: 21px;
        margin-bottom: 32px;
      }
      .contact {
        font-size: 14px;
        a {
          color: @colorBrandPrimary;
        }
      }
    }
  }
  .AccordionTitle {
    width: 100%;
    display: flex;
    align-items: center;
    color: @colorBrandPrimary;
    a {
      margin-left: auto;
      margin-right: 12px;
      background-color: @colorBrandPrimary;
      color: @colorWhite;
      height: 22px;
      padding: 11px 24px 13px 24px;
      font-size: 16px;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 20px;
      text-align: center;
      text-decoration: none;
    }
    .accordion-status {
      font-size: 30px;
      width: 68px;
      height: 76px;
      line-height: 76px;
      border-right: 1px solid #ace0f7;
      text-align: center;
      font-weight: lighter;
      letter-spacing: -3px;
      &::before {
        content: '+';
      }
    }
    .portfolio-title {
      height: 24px;
      font-size: 22px;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 24px;
      text-transform: uppercase;
    }
    .icon-circle {
      font-size: 36px;
      border-radius: 48px;
      align-self: center;
      width: 48px;
      height: 48px;
      line-height: 48px;
      border: 2px dotted @colorBrandPrimary;
      margin: 0 16px 0 30px;
      &:before {
        display: block;
        width: 48px;
        text-align: center;
      }
    }
  }
  &::v-deep {
    .MainAccordion.el-collapse {
      border-width: 0;
      & > .el-collapse-item {
        box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.12);
        margin-bottom: 20px;
        background-color: #c6eafa;
        transition: background-color 0.3s linear;
        &.is-active {
          background-color: white;
          .accordion-status {
            border-right: 1px solid @colorGrayLight;
            &:before {
              content: '--' !important;
            }
          }
        }
        .el-collapse-item__arrow {
          display: none;
        }
        & > div > .el-collapse-item__header {
          height: 76px;
        }
        .el-collapse-item__header,
        .el-collapse-item__wrap {
          border-width: 0;
          background-color: transparent;
        }
      }
    }
  }
}
</style>
