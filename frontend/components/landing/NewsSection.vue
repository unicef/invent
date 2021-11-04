<template>
  <div v-if="newsFeed.length > 0" class="NewsSection">
    <div class="header">
      <translate>Latest news</translate>
      <div v-if="showPageControls" class="actions">
        <fa icon="chevron-left" :class="{ active: !firstSlide }" @click="$refs.newSlider.prev()" />
        <fa icon="chevron-right" :class="{ active: !lastSlide }" @click="$refs.newSlider.next()" />
      </div>
    </div>
    <el-carousel
      ref="newSlider"
      :autoplay="false"
      :loop="false"
      height="360px"
      arrow="never"
      indicator-position="none"
      @change="checkActive"
    >
      <el-carousel-item v-for="(carousel, carouselIndex) in newsCarousel" :key="carouselIndex" class="cards">
        <NewsCard v-for="carouselItem in carousel" :key="carouselItem.id" :news="carouselItem" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import NewsCard from '@/components/landing/parts/NewsCard.vue'

export default {
  components: {
    NewsCard,
  },
  data() {
    return {
      activeSlide: 0,
    }
  },
  computed: {
    ...mapGetters({
      newsFeed: 'landing/getNewsFeed',
    }),
    newsCarousel() {
      const res = []
      if (this.newsFeed) {
        for (let i = 0; i < this.newsFeed.length; i += 3) {
          const chunk = this.newsFeed.slice(i, i + 3)
          res.push(chunk)
        }
      }
      return res
    },
    showPageControls() {
      return this.newsCarousel.length > 1
    },
    firstSlide() {
      return this.activeSlide === 0
    },
    lastSlide() {
      return this.activeSlide === this.newsCarousel.length - 1
    },
  },
  methods: {
    checkActive(index) {
      this.activeSlide = index
    },
  },
}
</script>

<style lang="less" scoped>
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.action {
  font-size: @fontSizeBase;
}

.NewsSection {
  padding: 45px 100px 60px 100px;
  background-color: white;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: @fontSizeLarge;
    margin-bottom: 35px;
    .actions {
      display: flex;
      justify-content: space-between;
      width: 68px;
      color: @colorGray;
      .active {
        cursor: pointer;
        color: @colorBrandPrimary;
      }
    }
  }
  .cards {
    display: flex;
    gap: 20px;
  }
}
</style>
