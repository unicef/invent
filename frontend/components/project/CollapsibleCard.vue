<template>
  <div class="CollapsibleCard">
    <el-card :body-style="{ padding: '0px' }">
      <div slot="header" class="CollapsibleHeader">
        <span class="CardTitle">
          {{ title }}
        </span>
        <el-button type="text" class="CollapseToggle" @click="toggleCard">
          <fa v-show="open" icon="angle-down" size="lg" />
          <fa v-show="!open" icon="angle-up" size="lg" />
        </el-button>
      </div>

      <transition name="slide-fade">
        <div v-show="open" class="ContentContainer">
          <div v-if="showLegend" class="Legend">
            <div>
              <span class="Required Draft">
                <span> * </span>
              </span>
              <span class="Text">
                <translate ref="draft_required">
                  Required to save draft
                </translate>
              </span>
            </div>
            <div>
              <span class="Required Publish">
                <span> * </span>
              </span>
              <span class="Text">
                <translate ref="publish_required">
                  Required to publish
                </translate>
              </span>
            </div>
          </div>
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
    showLegend: {
      type: Boolean,
      default: false,
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

  .Legend {
    text-align: right;

    .Text {
      font-size: @fontSizeSmall;
    }

    .Required {
      display: inline-block;
      width: 12px;
      height: 12px;
      font-size: 16px;
      line-height: 12px;
      font-weight: 900;
      text-align: center;
      border-radius: 50%;

      > span {
        position: relative;
        top: 3px;
      }
    }

    .Draft {
      color: @colorTextPrimary;
      background-color: @colorDraft;
    }

    .Publish {
      color: @colorWhite;
      background-color: @colorPublished;
    }
  }

  .el-card {
    .el-card__header {
      padding: 0 20px 0 40px;
      height: 58px;
      line-height: 58px;
      background-color: @colorBrandPrimaryDark;
      font-size: @fontSizeLarger;
    }
  }

  .CollapsibleHeader {
    .clearfix();

    .CardTitle {
      float: left;
    }

    .CollapseToggle {
      width: 58px;
      height: 58px;
      float: right;
      color: @colorWhite;

      .svg-inline--fa {
        width: 12px;
        transform: rotateX(0deg);
        transition: @transitionAll;
      }

      &:hover {
        .svg-inline--fa {
          opacity: 0.8;
          transform: rotateX(180deg);
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
    .slide-fade-leave-to
    /* .slide-fade-leave-active below version 2.1.8 */ {
    transform: translateY(-20px);
    opacity: 0;
  }
}
</style>
