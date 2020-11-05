<template>
  <section class="portfolio-main">
    <h1>
      <translate>UNICEF’s Global Innovation Portfolios</translate>
    </h1>
    <h2>
      <translate>Explore the Portfolios</translate>
    </h2>
    <p>
      <translate>
        UNICEF's portfolio approach to innovation ensures that innovation is
        applied to the toughest, most pressing problems faced by some of the
        most vulnerable children and young people. Our innovation portfolios are
        curated sets of investments that focus on these pressing challenges to
        accelerate results where we can achieve the greatest impact.
      </translate>
    </p>
    <p>
      <translate>
        Expand the portfolios below to learn more about the key problems we seek
        to solve in our priority areas for innovation, or select “View
        Portfolio” to explore solutions.
      </translate>
    </p>

    <el-collapse v-model="activePortfolio" accordion class="MainAccordion">
      <el-collapse-item
        v-for="portfolio in portfolios"
        :key="portfolio.name"
        :name="portfolio.id"
      >
        <div slot="title" class="AccordionTitle">
          <span class="accordion-status"></span>
          <span :class="`icon-circle icon-tiip-${portfolio.icon}`">&nbsp;</span>
          <span class="portfolio-title">{{ portfolio.name }}</span>
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-portfolio-innovation-id',
                params: { organisation: '-', id: portfolio.id },
              })
            "
          >
            <translate>View Portfolio</translate>
          </nuxt-link>
        </div>
        <div class="AccordionContent">
          <el-row>
            <el-col :span="12" class="col-container">
              <div class="col-title">
                <translate>Problem Statements</translate>
              </div>
              <el-collapse v-model="activePS" accordion class="SubAccordion">
                <el-collapse-item
                  v-for="{ name, id, description } in portfolio.ps"
                  :key="name"
                  :name="id"
                >
                  <div slot="title" class="SubAccordionTitle">
                    {{ name }}
                  </div>
                  <div class="SubAccordionContent">
                    {{ description }}
                  </div>
                </el-collapse-item>
              </el-collapse>
            </el-col>
            <el-col :span="12" class="col-container">
              <div class="col-title">
                <translate>Summary</translate>
              </div>
              <p class="summary">
                {{ portfolio.description }}
              </p>
              <template
                v-if="portfolio.managers && portfolio.managers.length > 0"
              >
                <div class="col-title">
                  <translate>Contact person</translate>
                </div>
                <div
                  v-for="{ email, name } in portfolio.managers"
                  :key="portfolio.id + name"
                  class="contact"
                >
                  {{ name }} <br />
                  <a :href="`mailto:${email}`">{{ email }}</a>
                </div>
              </template>
            </el-col>
          </el-row>
        </div>
      </el-collapse-item>
    </el-collapse>
    <info-card class="InfoCard" />
  </section>
</template>

<script>
import InfoCard from '@/components/portfolio/dashboard/InfoCard'
import { mapState } from 'vuex'

export default {
  components: {
    InfoCard,
  },
  data() {
    return {
      activePortfolio: undefined,
      activePS: undefined,
    }
  },
  async fetch({ store }) {
    await store.dispatch('portfolio/getPortfolios', 'active-list')
  },
  computed: {
    ...mapState({
      portfolios: (state) => state.portfolio.portfolios,
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.InfoCard {
  padding-top: 40px;
}
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
        color: @colorTextPrimary;
        font-size: 14px;
        letter-spacing: -0.25px;
        line-height: 21px;
        margin-bottom: 32px;
      }
      .contact {
        font-size: 14px;
        margin-bottom: 20px;
        a {
          text-decoration: none;
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
