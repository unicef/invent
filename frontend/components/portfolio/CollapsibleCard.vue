<template>
  <div class="CollapsibleCard">
    <el-card :body-style="{ padding: '0px' }">
      <div slot="header" class="CollapsibleHeader">
        <span class="CardTitle">
          {{ title }}
        </span>
        <el-button type="text" class="CollapseToggle" @click="toggleCard">
          <fa v-show="open" icon="minus" size="lg" />
          <fa v-show="!open" icon="plus" size="lg" />
        </el-button>
      </div>

      <transition name="slide-fade">
        <div v-show="open" class="ContentContainer">
          <slot />
        </div>
      </transition>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      open: true,
    }
  },
  methods: {
    toggleCard() {
      this.open = !this.open
    },
    expandCard() {
      this.open = true
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.CollapsibleCard {
  margin: 0 0 20px;

  .el-card {
    // box-shadow: inset 0 -1px 0 0 #eae6e1;
    .el-card__header {
      padding: 0 20px 0 40px;
      height: 58px;
      line-height: 58px;
      background-color: @colorWhite!important;
      font-size: @fontSizeLarger;
      border-bottom: 1px solid #eae6e1;
    }
  }

  .CollapsibleHeader {
    .clearfix();

    .CardTitle {
      float: left;
      color: @colorBrandPrimary;
    }

    .CollapseToggle {
      width: 58px;
      height: 58px;
      float: right;
      color: @colorBrandPrimary!important;

      .svg-inline--fa {
        width: 12px;
        transform: rotateX(0deg);
        transition: @transitionAll;
      }

      &:hover {
        .svg-inline--fa {
          opacity: 0.8;
        }
      }
    }
  }

  .ContentContainer {
    padding: 40px 80px 60px 40px;
  }

  .slide-fade-enter-active {
    transition: @transitionAll;
  }

  .slide-fade-leave-active {
    transition: @transitionAll;
  }

  .slide-fade-enter,
  .slide-fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
  }
}
</style>
