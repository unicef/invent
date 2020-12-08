<template>
  <div
    :class="`Matrix ${top !== false ? 'ShowOnTop' : ''} ${
      noarrow !== false ? 'HideArrow' : ''
    }`"
  >
    <div class="ArrowRight" />
    <div class="ArrowTop" />
    <div class="MColumns">
      <div class="MColumn">
        <div
          v-for="{ labels, extra, name } in allAxis"
          :key="name"
          :class="name"
        >
          <span v-for="(text, index) in labels" :key="text">
            {{ text }}
            <el-tooltip
              v-if="index === 1 && extra"
              :content="extra"
              effect="dark"
              placement="bottom"
              popper-class="SearchBoxTooltip"
            >
              <el-button type="text" class="MutedButton">
                <fa icon="question-circle" />
              </el-button>
            </el-tooltip>
          </span>
        </div>
        <div class="Elements" :style="matrixStyle">
          <matrix-element
            v-for="(element, index) in elements"
            :key="`${element.x}_${element.y}`"
            :state="getState(index)"
            :color="color"
            :reverse="top !== false"
            v-bind="element"
            @click="activeIndex = index"
          />
        </div>
      </div>
      <div class="MColumn">
        <div v-if="active" class="Overlay">
          <div class="el-icon-close" @click="clear" />
          <div class="ListTitle">
            <h4>
              <translate :parameters="{ num: active.projects.length }">
                List of initiatives ({num})
              </translate>
            </h4>
            <p>
              {{ leftText }}: {{ active.y }}&nbsp; &nbsp; {{ bottomText }}:
              {{ active.x }}
            </p>
          </div>
          <div class="List">
            <el-scrollbar class="Scroll" :native="false" :noresize="false">
              <div
                v-for="project in active.projects"
                :key="project.id"
                class="ListLink"
              >
                <nuxt-link :to="getPath(project)">
                  {{ project.title }}
                </nuxt-link>
              </div>
            </el-scrollbar>
          </div>
        </div>
        <div class="Content">
          <h4><translate>Summary</translate></h4>
          <p>
            {{ description }}
          </p>
          <template v-if="contacts && contacts.length > 0">
            <h4>
              <translate>Contact Person</translate>
            </h4>
            <p v-for="{ name, email } in contacts" :key="name">
              {{ name }} <br />
              <a :href="`mailto:${email}`">{{ email }}</a>
            </p>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MatrixElement from '@/components/portfolio/Matrix-element'
export default {
  name: 'Matrix',
  components: {
    MatrixElement,
  },
  props: {
    elements: {
      type: Array,
      required: true,
    },
    left: {
      type: Array,
      required: true,
    },
    bottom: {
      type: Array,
      required: true,
    },
    extraBottom: {
      type: String,
      default: '',
    },
    extraLeft: {
      type: String,
      default: '',
    },
    color: {
      type: String,
      default: '',
    },
    top: {
      type: Boolean,
      default: false,
    },
    noarrow: {
      type: Boolean,
      default: false,
    },
    bgColor: {
      type: String,
      default: '',
    },
    bgImage: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    contacts: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      activeIndex: undefined,
    }
  },
  computed: {
    allAxis() {
      return [
        {
          labels: this.left,
          extra: this.extraLeft,
          name: 'Yaxis',
        },
        {
          labels: this.bottom,
          extra: this.extraBottom,
          name: 'Xaxis',
        },
      ]
    },
    leftText() {
      return this.removeBracets(this.left[1])
    },
    bottomText() {
      return this.removeBracets(this.bottom[1])
    },
    active() {
      return this.activeIndex !== undefined
        ? this.elements[this.activeIndex]
        : undefined
    },
    matrixStyle() {
      if (this.bgImage) {
        return `background-image: url(${this.bgImage})`
      }
      if (this.bgColor) {
        return `background-color: ${this.bgColor}`
      }
      return ''
    },
  },
  methods: {
    clear() {
      this.activeIndex = undefined
    },
    removeBracets(text) {
      return text.replace(/.\(.*\)/, '')
    },
    getPath(project) {
      return this.localePath({
        name: 'organisation-initiatives-id-published',
        params: { organisation: '-', id: project.id },
      })
    },
    getState(index) {
      if (this.activeIndex === undefined) {
        return 'normal'
      }
      if (this.activeIndex === index) {
        return 'active'
      }
      return 'inactive'
    },
  },
}
</script>

<style lang="less" scoped>
.Matrix {
  color: #404041;
  background-color: white;
  margin: 5px;
  // some circles are way outside the graph
  // overflow: hidden;
  //&::v-deep .el-scrollbar__bar.is-vertical {
  //  opacity: 1 !important;
  //}
  &::v-deep .el-scrollbar__wrap {
    overflow-y: scroll;
    overflow-x: hidden;
  }
  &.HideArrow {
    .ArrowRight,
    .ArrowTop {
      display: none !important;
    }
  }
  &.ShowOnTop {
    .Elements {
      top: 40px;
    }
    .Yaxis {
      top: 40px;
    }
    .Xaxis {
      top: 0;
      bottom: initial;
    }
    .MColumns > .MColumn:first-child {
      border-bottom: 0 solid transparent;
      border-top: 1px solid #a8a8a9;
    }
    .ArrowRight {
      top: 40px;
    }
    .ArrowTop {
      transform: rotate(180deg);
      top: 641px;
    }
    .Overlay:after {
      top: 73px !important;
    }
  }
  .MColumns {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    .MColumn:first-child {
      position: relative;
      flex: 0 0 600px;
      width: 600px;
      height: 600px;
      border-left: 1px solid #a8a8a9;
      border-bottom: 1px solid #a8a8a9;
    }
    .MColumn + .MColumn {
      flex: 1;
      position: relative;
      h4 {
        font-size: 18px;
        letter-spacing: -0.5px;
        line-height: 23px;
        font-weight: normal;
      }
      a {
        color: #1cabe2;
        text-decoration: none;
      }
      p {
        font-size: 14px;
        letter-spacing: -0.25px;
        line-height: 21px;
      }
      .Content {
        margin: 5px 20px 20px 40px;
        height: 576px;
        overflow-y: hidden;
        overflow: scroll;
      }
      .Overlay {
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: white;
        box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.12);
        .ListTitle {
          padding: 30px 20px 30px 40px;
          h4 {
            margin: 0;
            padding-bottom: 12px;
          }
          p {
            margin: 0;
          }
        }
        &:after {
          content: '';
          border-top: 20px solid transparent;
          border-bottom: 20px solid transparent;
          position: absolute;
          border-right: 20px solid white;
          width: 0;
          height: 0;
          left: -20px;
          top: 40px;
          margin-top: -20px;
        }
        .el-icon-close {
          right: 20px;
          top: 25px;
          padding: 10px;
          font-size: 16px;
          position: absolute;
          color: #a8a8a9;
          cursor: pointer;
          &:hover {
            color: black;
          }
        }
        .Scroll {
          height: 490px;
        }
        p {
          font-size: 12px;
          color: #777779;
          text-transform: uppercase;
        }
        .List {
          border-top: 1px solid #eae6e1;
          padding-top: 24px;
          .ListLink {
            a {
              text-decoration: none;
            }
            padding: 0 40px 24px 40px;
            color: #1cabe2;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 0;
            line-height: 24px;
          }
        }
      }
    }
  }
  .Elements {
    position: absolute;
    top: 0;
    left: 40px;
    width: 560px;
    height: 560px;
    //background-image: url('/bg-ambition_matrix.svg');
  }
  .Yaxis,
  .Xaxis {
    position: absolute;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    font-size: 12px;
    line-height: 40px;
    span {
      text-transform: uppercase;
      color: #a8a8a9;
    }
    span:first-child + span {
      color: #404041;
    }
  }
  .Yaxis {
    padding: 10px 0;
    width: 40px;
    height: 540px;
    writing-mode: vertical-lr;
    transform: rotate(180deg);
    .MutedButton {
      transform: rotate(90deg);
    }
  }
  .Xaxis {
    padding: 0 10px;
    width: 540px;
    height: 40px;
    left: 40px;
    bottom: 0;
  }
  .ArrowTop,
  .ArrowRight {
    position: absolute;
    width: 11px;
    height: 10px;
    background-image: url('/arrowhead-tl.svg');
  }
  .ArrowTop {
    left: 0;
  }
  .ArrowRight {
    transform: rotate(90deg);
    left: 599px;
    top: 641px;
  }
}
</style>
