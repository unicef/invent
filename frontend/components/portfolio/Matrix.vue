<template>
  <div class="Matrix">
    <div class="ArrowRight" />
    <div class="ArrowTop" />
    <div class="MColumns">
      <div class="MColumn">
        <div class="Yaxis">
          <span
            v-for="text in left"
            :key="text"
          >{{ text }}</span>
        </div>
        <div class="Xaxis">
          <span
            v-for="text in bottom"
            :key="text"
          >{{ text }}</span>
        </div>
        <div class="Elements">
          <matrix-element
            v-for="(element, index) in elements"
            :key="`${element.x}_${element.y}`"
            :state="getState(index)"
            v-bind="element"
            @click="activeIndex = index"
          />
        </div>
      </div>
      <div class="MColumn">
        <div
          v-if="active"
          class="Overlay"
        >
          <div
            class="el-icon-close"
            @click="activeIndex = undefined"
          />
          <div class="Content">
            <h4>List of projects ({{ active.projects.length }})</h4>
            <p>{{ left[1] }}: {{ active.y }}&nbsp; &nbsp; {{ bottom[1] }}: {{ active.x }}</p>
          </div>
          <div class="List">
            <el-scrollbar
              class="Scroll"
              :native="false"
              :noresize="false"
            >
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
          <h4>Summary</h4>
          <p>Quid securi etiam tamquam eu fugiat nulla pariatur. Vivamus sagittis lacus vel augue laoreet rutrum faucibus. Contra legem facit qui id facit quod lex prohibet. Gallia est omnis divisa in partes tres, quarum. Pellentesque habitant morbi tristique senectus et netus. Donec sed odio operae, eu vulputate felis rhoncus. Curabitur est gravida et libero vitae dictum. Cum ceteris in veneratione tui montes, nascetur mus. Ab illo tempore, ab est sed immemorabili. Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Qui ipsorum lingua Celtae, nostra Galli appellantur.</p>
          <h4>Contact Person</h4>
          <p>
            Edson Monterio <br>
            <a href="mailto:emonterio@unicef.org">emonterio@unicef.org</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MatrixElement from '@/components/portfolio/Matrix-element';
export default {
  name: 'Matrix',
  components: {
    MatrixElement
  },
  props: {
    elements: {
      type: Array,
      required: true
    },
    left: {
      type: Array,
      required: true
    },
    bottom: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      activeIndex: undefined
    };
  },
  computed: {
    active () {
      return this.activeIndex !== undefined ? this.elements[this.activeIndex] : undefined;
    }
  },
  methods: {
    getPath (project) {
      return this.localePath({ name: 'organisation-projects-id-published', params: { organisation: '-', id: project.id } });
    },
    getState (index) {
      if (this.activeIndex === undefined) {
        return 'normal';
      }
      if (this.activeIndex === index) {
        return 'active';
      }
      return 'inactive';
    }
  }
};
</script>

<style lang="less" scoped>
.Matrix {
  color: #404041;
  background-color: white;
  margin: 5px;
  //&::v-deep .el-scrollbar__bar.is-vertical {
  //  opacity: 1 !important;
  //}
  .MColumns {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    .MColumn:first-child {
      position: relative;
      flex: 0 0 600px;
      width: 600px;
      height: 600px;
      border-left: 1px solid #A8A8A9;
      border-bottom: 1px solid #A8A8A9;
    }
    .MColumn + .MColumn {
      position: relative;
      h4 {
        font-size: 18px;
        letter-spacing: -0.5px;
        line-height: 23px;
        font-weight: normal;
      }
      a {
        color: #1CABE2;
        text-decoration: none;
      }
      p {
        font-size: 14px;
        letter-spacing: -0.25px;
        line-height: 21px;
      }
      .Content {
        padding: 5px 20px 20px 40px;
      }
      .Overlay {
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: white;
        box-shadow: 5px 5px 20px 0 rgba(0,0,0,0.12);
        &:after {
          content:"";
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
          top: 27px;
          padding: 10px;
          font-size: 16px;
          position: absolute;
          color: #A8A8A9;
          cursor: pointer;
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
          border-top: 1px solid #EAE6E1;
          .ListLink {
            a {
              text-decoration: none;
            }
            padding: 24px 40px;
            color: #1CABE2;
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
    background-image: url('/bg-ambition_matrix.svg');
  }
  .Yaxis, .Xaxis {
    position: absolute;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    font-size: 12px;
    line-height: 40px;
    span {
      text-transform: uppercase;
      color: #A8A8A9;
    }
    span:first-child + span{
      color: #404041;
    }
  }
  .Yaxis {
    padding: 10px 0;
    width: 40px;
    height: 540px;
    writing-mode: vertical-lr;
    transform: rotate(180deg);
  }
  .Xaxis {
    padding: 0 10px;
    width: 540px;
    height: 40px;
    left: 40px;
    bottom: 0;
  }
  .ArrowTop, .ArrowRight {
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
    bottom: 0;
  }
}
</style>
