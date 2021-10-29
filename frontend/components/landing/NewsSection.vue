<template>
  <div v-if="newses.length > 0" class="NewsSection">
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
import NewsCard from '@/components/landing/parts/NewsCard.vue'

export default {
  components: {
    NewsCard,
  },
  data() {
    return {
      activeSlide: 0,
      emptyImgUrl: '~static/bg-unicef-globe.svg',
      newses: [
        {
          id: 1,
          order: 1,
          imgUrl: 'https://www.unicef.org/sites/default/files/styles/hero_desktop/public/UN0502861_0.jpg',
          altText: 'Afghanistan. Internally displaced Afghan families walk past tents in Kabul.',
          title: 'Delivering for Afghanistan’s children',
          description:
            'UNICEF is continuing to work with partners to support children and their families across the country.',
          url: 'https://www.unicef.org/emergencies/delivering-support-afghanistans-children',
        },
        {
          id: 2,
          order: 2,
          imgUrl: '',
          altText: 'Hidden Heroes podcast cover art',
          title: 'Hidden Heroes',
          description:
            'In this eight-episode podcast series, travel the globe to meet women and girls taking a stand against gender injustice – and saving lives along the way. Join host Beth Murphy for intimate conversations with these hidden heroes of the COVID-19 pandemic. Each episode is followed by a “deep dive” companion piece, in which experts in equality and public health help us better understand the forces driving harmful practices, violence and other rights violations worldwide.',
          url: 'https://www.unicef.org/hidden-heroes',
        },
        {
          id: 3,
          order: 3,
          imgUrl: 'https://www.unicef.org/sites/default/files/styles/press_release_feature/public/Haiti%203_1.jpg',
          altText:
            'Les Cayes, Haiti. Staff working at the UNICEF Warehouse preparing the school bags and school kits for the school opening on the 4th of October 2021.',
          title: 'Earthquake leaves nearly 70 per cent of schools damaged or destroyed in southwestern Haiti – UNICEF',
          description: 'Over 300,000 children to resume schooling in earthquake-affected areas.',
          url:
            'https://www.unicef.org/press-releases/earthquake-leaves-nearly-70-cent-schools-damaged-or-destroyed-southwestern-haiti',
        },
        {
          id: 4,
          order: 4,
          imgUrl: 'https://www.unicef.org/sites/default/files/styles/large/public/EN_SDG-Mosaic-Tile.jpg',
          altText:
            'Les Cayes, Haiti. Staff working at the UNICEF Warehouse preparing the school bags and school kits for the school opening on the 4th of October 2021.',
          title: 'UNICEF and the Sustainable Development Goals',
          description:
            'Investing in children and young people to achieve a more equitable, just and sustainable world for all.',
          url: 'https://www.unicef.org/sdgs',
        },
      ],
    }
  },
  computed: {
    newsCarousel() {
      const res = []
      for (let i = 0; i < this.newses.length; i += 3) {
        const chunk = this.newses.slice(i, i + 3)
        res.push(chunk)
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
