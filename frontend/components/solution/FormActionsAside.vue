<template>
  <div v-scroll-class:FixedNavigation="266" class="ProjectNavigation">
    <el-card :body-style="{ padding: '0px' }">
      <div v-if="isTeam || isNewProject || isSuper" class="NavigationActions">
        <el-button v-if="true" :disabled="!!loading" type="primary" size="medium" @click="emitAction('save')">
          <fa v-show="loading === 'publish'" icon="spinner" spin />
          <translate>Save</translate>
        </el-button>

        <el-button
          v-if="true"
          :type="isNewProject ? 'primary' : 'text'"
          :size="isNewProject ? 'medium' : ''"
          class="Cancel"
          :disabled="!!loading"
          @click="emitAction('cancel')"
        >
          <fa v-show="loading === 'draft'" icon="spinner" spin />
          <translate>Cancel</translate><br />
          <translate class="Rt-dashboard">Return to the Dashboard</translate>
        </el-button>

        <el-button v-if="true" :disabled="!!loading" type="text" class="DeleteButton" @click="emitAction('delete')">
          <fa v-show="loading === 'discard'" icon="spinner" spin />
          <translate>Delete</translate>
        </el-button>

        <el-tooltip
          v-if="isPublished"
          effect="dark"
          placement="top"
          popper-class="tooltip--width"
          :hide-after="parseInt(3200, 10)"
        >
          <div slot="content">
            {{ $gettext('The action will update the timestamp') | translate }}<br />
            {{ $gettext('of the initiative to the current date.') | translate }}
          </div>
          <el-button :disabled="!!loading" type="primary" size="medium" @click="emitAction('handleClickLatest')">
            <fa v-show="loading === 'latest'" icon="spinner" spin />
            <translate>Publish as latest</translate>
            <fa icon="question-circle" />
          </el-button>
        </el-tooltip>

        <el-button
          v-if="isPublished"
          :disabled="!!loading"
          type="danger"
          size="medium"
          class="button--danger"
          @click="emitAction('handleClickUnPublish')"
        >
          <fa v-show="loading === 'unpublish'" icon="spinner" spin />
          <translate>Unpublish</translate>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import VueScrollClass from 'vue-scroll-class'
import { mapGetters, mapActions } from 'vuex'

export default {
  directives: {
    'scroll-class': VueScrollClass,
  },
  computed: {
    ...mapGetters({
      loading: 'project/getLoading',
      user: 'user/getProfile',
      getCountryDetails: 'countries/getCountryDetails',
    }),
    active() {
      const hash = this.$route.hash
      return hash ? hash.replace('#', '') : 'general'
    },
    route() {
      return this.$route.name.split('__')[0]
    },
    isNewProject() {
      return this.route === 'organisation-initiatives-create'
    },
    isPublished() {
      return this.route === 'organisation-initiatives-id-published'
    },
    isDraft() {
      return this.route === 'organisation-initiatives-id-edit'
    },
    canEdit() {
      if (this.user) {
        return this.user.is_superuser
      }
      return false
    },
    isTeam() {
      return this.user ? this.user.member.includes(+this.$route.params.id) : false
    },
    isSuper() {
      return this.user && this.user.is_superuser
    },
  },
  mounted() {
    window.addEventListener('resize', this.setNavigationBoxLeftStyle)
    window.addEventListener('scroll', this.setNavigationBoxLeftStyle)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.setNavigationBoxLeftStyle)
    window.removeEventListener('scroll', this.setNavigationBoxLeftStyle)
  },
  methods: {
    ...mapActions({
      setLoading: 'project/setLoading',
    }),
    emitAction(action) {
      this.setLoading(true)
      setTimeout(() => {
        this.$emit(action)
      }, 100)
    },
    scrollTo(where) {
      window.location.hash = ''
      this.$nextTick(() => {
        this.$router.replace(`#${where}`)
      })
    },
    goToDraft() {
      const name =
        this.isTeam || this.isSuper
          ? 'organisation-innovation-solutions-id-edit'
          : 'organisation-innovation-solutions-id'
      const localised = this.localePath({
        name,
        params: { ...this.$route.params },
      })
      this.$router.push(localised)
    },
    goToPublished() {
      const localised = this.localePath({
        name: 'organisation-portfolio-innovation-solutions-id',
        params: { ...this.$route.params },
      })
      this.$router.push(localised)
    },
    goToDashboard() {
      const localised = this.localePath({
        name: 'organisation-dashboard-list',
        params: { ...this.$route.params },
      })
      this.$router.push(localised)
    },
    setNavigationBoxLeftStyle() {
      const leftSide = document.querySelector('#general')
      const lang = this.$nuxt.$i18n.locale
      const rtl = lang === 'ar'

      if (leftSide) {
        if (rtl) {
          const generalLeftPos = leftSide.getBoundingClientRect().left
          if (generalLeftPos) {
            this.$el.style.left = `${generalLeftPos - 320}px`
          }
        } else {
          const generalRightPos = leftSide.getBoundingClientRect().right
          if (generalRightPos) {
            this.$el.style.left = `${generalRightPos + 20}px`
          }
        }
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.button--danger {
  background-color: white !important;
  color: @colorDanger;
  &:hover {
    color: @colorDanger;
  }
}

.ProjectNavigation {
  width: @projectAsideNavWidth;

  &.FixedNavigation {
    position: fixed;
    top: 20px;
    // left specified inline via computed js
  }

  .SwitchProjectStatus {
    height: 58px;
    padding: 0 14px;
    border-bottom: 1px solid @colorGrayLight;
    box-sizing: border-box;

    .el-row {
      height: 100%;
    }

    .SwitchLabel {
      padding-right: 12px;
      font-size: @fontSizeBase;
      color: @colorTextPrimary;
    }
  }

  .Stepper {
    ul {
      position: relative;
      list-style: none;
      margin: 20px 0 25px;
      padding: 0;

      @media only screen and (max-height: 1024px) {
        margin: 20px 0;
      }

      &::after {
        z-index: 1;
        content: '';
        position: absolute;
        top: 15px;
        left: 45px;
        display: inline-block;
        width: 1px;
        height: calc(100% - 35px);
        background-color: @colorGrayLight;
      }
    }

    li {
      z-index: 2;
      position: relative;
      cursor: pointer;

      &.active,
      &:hover,
      &:active {
        .el-button {
          color: @colorTextPrimary;

          .Step {
            background-color: @colorBrandPrimaryDark;
            border-width: 4px;
            color: @colorWhite;
            transform: scale(1.2);
          }

          .svg-inline--fa {
            opacity: 1;
            transform: translate(-50%, -50%);
          }
        }
      }

      &.active {
        .el-button {
          font-weight: 700;
        }
      }
    }

    .el-button {
      position: relative;
      display: block;
      padding: 0 20px 0 70px;
      height: 62px;
      line-height: 62px;
      font-size: @fontSizeMedium;
      font-weight: 400;
      color: @colorTextSecondary;
      text-decoration: none;
      transition: color 200ms ease;

      @media only screen and (max-height: 1024px) {
        height: 48px;
        line-height: 48px;
      }

      .Step {
        position: absolute;
        top: 15px;
        left: 30px;
        overflow: hidden;
        box-sizing: border-box;
        display: inline-block;
        width: 30px;
        height: 30px;
        border: 6px solid @colorWhite;
        background-color: @colorGrayLight;
        border-radius: 30px;
        color: @colorGrayLight;
        transition: all 200ms ease;

        @media only screen and (max-height: 1024px) {
          top: 8px;
        }

        .svg-inline--fa {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-100%, -50%);
          display: inline-block;
          width: 12px;
          height: 12px;
          opacity: 0;
          transition: @transitionFadeMd;
        }
      }
    }
  }

  .NavigationActions {
    padding: 30px;
    border-top: 1px solid @colorGrayLight;
    background-color: @colorBrandBlueLight;
    text-align: center;

    .el-button--primary,
    .el-button--danger {
      width: 100%;
      margin: 0 0 20px;
    }

    .el-button--text {
      width: 100%;
      margin: 0;
      font-size: @fontSizeMedium;
    }

    .fa-spin {
      margin-right: 2px;
    }
  }
  .DeleteButton {
    padding: 16px;
    color: @colorWhite;
    background-color: #1cabe2;
    text-align: center;
  }
  .Cancel {
    color: gray;
    :hover {
      color: lightgray;
    }
    .Rt-dashboard {
      padding-top: 4px;
      font-size: @fontSizeSmall;
    }
  }
}
</style>
