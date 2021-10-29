<template>
  <a
    :href="news.url"
    target="_blank"
    class="NewsCard"
    :class="{ noImg: !news.imgUrl }"
    :style="`background-image: url(${imgUrl})`"
  >
    <div class="content">
      <div class="title">
        {{ news.title }}
      </div>
      <div class="desc">
        {{ news.description }}
      </div>
      <div class="read">
        <translate>Read the Story</translate>
        <fa class="right" icon="chevron-right" size="sm" />
      </div>
    </div>
  </a>
</template>

<script>
export default {
  props: {
    news: {
      type: Object,
      required: true,
    },
  },
  computed: {
    imgUrl() {
      return this.news.imgUrl ? this.news.imgUrl : '/bg-unicef-globe.svg'
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.NewsCard {
  position: relative;
  width: 480px;
  height: 360px;
  color: @colorWhite;
  background-color: @colorWhite;
  border-radius: 3px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.08), 1px 2px 4px 0 rgba(0, 0, 0, 0.12);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
  text-decoration: none;
  transition: all 0.2s ease;
  &::after {
    content: '';
    position: absolute;
    z-index: -1;
    inset: 0;
    background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #00000038 100%);
  }
  &:hover::after {
    z-index: 2;
  }

  &.noImg {
    background-size: 82%;
    background-color: #1cabe2;
  }

  .content {
    position: absolute;
    z-index: 5;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    bottom: 0;
    height: 213px;
    padding: 24px;
    background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #00000082 100%);

    .title {
      margin-bottom: 8px;
      font-size: @fontSizeLarge;
      font-weight: bold;
      line-height: 24px;
      max-height: 72px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
    }

    .desc {
      margin-bottom: 16px;
      font-size: @fontSizeBase;
      line-height: 21px;
      max-height: 42px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

    .read {
      font-size: @fontSizeBase;
      svg {
        margin-left: 4px;
      }
    }
  }
}
</style>
