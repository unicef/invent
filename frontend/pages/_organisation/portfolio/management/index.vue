<template>
  <section class="portfolio-main">
    <title-card />
    <article class="portfolios">
      <portfolio-card v-for="item in items" :key="item.id" :item="item" />
    </article>
    <info-card />
  </section>
</template>

<script>
import { mapState } from "vuex";
import TitleCard from "@/components/portfolio/dashboard/TitleCard";
import PortfolioCard from "@/components/portfolio/dashboard/PortfolioCard";
import InfoCard from "@/components/portfolio/dashboard/InfoCard";

export default {
  components: {
    TitleCard,
    PortfolioCard,
    InfoCard
  },
  data() {
    return {};
  },
  async fetch({ store }) {
    store.dispatch("portfolio/getPortfolios");
  },
  computed: {
    ...mapState({
      items: state => state.portfolio.portfolios
    })
  },
  methods: {}
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.portfolio-main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 1242px;
  margin: 50px auto 170px;
  .portfolios {
    width: 100%;
    margin-bottom: calc(60px - 16px);
    display: flex;
    flex-wrap: wrap;
    // justify-content: space-between;
  }
}
</style>
