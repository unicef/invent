<template>
  <section class="portfolio-main">
    <title-card />
    <article class="portfolios">
      <portfolio-card />
    </article>
    <info-card />
  </section>
</template>

<script>
import TitleCard from "@/components/portfolio/dashboard/TitleCard";
import PortfolioCard from "@/components/portfolio/dashboard/PortfolioCard";
import InfoCard from "@/components/portfolio/dashboard/InfoCard";

export default {
  components: {
    TitleCard,
    PortfolioCard,
    InfoCard
  },
  async fetch({ store }) {},
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
    margin-bottom: 60px;
  }
}
</style>
