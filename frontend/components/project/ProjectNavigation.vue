<template>
  <div v-scroll-class:FixedNavigation="266" class="ProjectNavigation">
    <el-card :body-style="{ padding: '0px' }">
      <div v-if="!isNewProject" class="SwitchProjectStatus">
        <el-row type="flex" justify="space-between" align="middle">
          <div class="SwitchLabel">Switch view:</div>
          <el-button-group class="SwitchButtons">
            <el-button
              :class="['DraftButton', { Active: isDraft || isReadOnlyDraft }]"
              :disabled="isDraft || anon"
              @click="goToDraft"
            >
              <translate>Draft</translate>
            </el-button>
            <el-button
              :class="[
                'PublishedButton',
                { Active: isPublished && published.name },
              ]"
              :disabled="isPublished || !published.name"
              @click="goToPublished"
            >
              <translate>Published</translate>
            </el-button>
          </el-button-group>
        </el-row>
      </div>

      <div class="Stepper">
        <ul>
          <li :class="{ active: active === 'general' }">
            <el-button type="text" @click="scrollTo('general')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>General</translate>
            </el-button>
          </li>
          <li :class="{ active: active === 'implementation' }">
            <el-button type="text" @click="scrollTo('implementation')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Implementation</translate>
            </el-button>
          </li>
          <li :class="{ active: active === 'stages' }">
            <el-button type="text" @click="scrollTo('stages')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Stages</translate>
            </el-button>
          </li>
          <li :class="{ active: active === 'partners' }">
            <el-button type="text" @click="scrollTo('partners')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Partners</translate>
            </el-button>
          </li>
          <li :class="{ active: active === 'categorization' }">
            <el-button type="text" @click="scrollTo('categorization')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Categorization</translate>
            </el-button>
          </li>
          <li :class="{ active: active === 'technology' }">
            <el-button type="text" @click="scrollTo('technology')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Technology</translate>
            </el-button>
          </li>
          <li
            v-show="showDonorFieldsLink"
            :class="{ active: active === 'donorcustom' }"
          >
            <el-button type="text" @click="scrollTo('donorcustom')">
              <span class="Step">
                <fa icon="arrow-right" />
              </span>
              <translate>Investor fields</translate>
            </el-button>
          </li>
        </ul>
      </div>

      <div v-if="isTeam || isNewProject" class="NavigationActions">
        <el-button
          v-if="isDraft"
          :disabled="!!loading"
          type="primary"
          size="medium"
          @click="$emit('publishProject')"
        >
          <fa v-show="loading === 'publish'" icon="spinner" spin />
          <translate>Publish</translate>
        </el-button>

        <el-button
          v-if="isNewProject || isDraft"
          :type="isNewProject ? 'primary' : 'text'"
          :size="isNewProject ? 'medium' : ''"
          :class="['SaveDraft', { NewProject: isNewProject, Draft: isDraft }]"
          :disabled="!!loading"
          @click="$emit('saveDraft')"
        >
          <fa v-show="loading === 'draft'" icon="spinner" spin />
          <translate>Save draft</translate>
        </el-button>

        <el-button
          v-if="isDraft"
          :disabled="!!loading"
          type="text"
          class="DiscardDraft DeleteButton"
          @click="$emit('discardDraft')"
        >
          <fa v-show="loading === 'discard'" icon="spinner" spin />
          <translate>Discard draft</translate>
        </el-button>

        <el-tooltip
          v-if="isPublished"
          effect="dark"
          placement="top"
          popper-class="tooltip--width"
          :hide-after="parseInt(3200, 10)"
        >
          <div slot="content">
            {{ $gettext('This action will update the timestamp') | translate
            }}<br />
            {{ $gettext('of the project to the current date.') | translate }}
          </div>
          <el-button
            :disabled="!!loading"
            type="primary"
            size="medium"
            @click="$emit('handleClickLatest')"
          >
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
          @click="$emit('handleClickUnPublish')"
        >
          <fa v-show="loading === 'unpublish'" icon="spinner" spin />
          <translate>Unpublish</translate>
        </el-button>

        <el-button
          v-if="isPublished || isReadOnlyDraft"
          type="text"
          class="GoToDashboard"
          @click="goToDashboard"
        >
          <translate>Go to Dashboard</translate>
        </el-button>

        <el-button
          v-if="isNewProject"
          type="text"
          class="CancelButton WithHint"
          @click="goToDashboard"
        >
          <translate>Cancel</translate>
          <span class="ButtonHint">
            <translate>Return to the Dashboard</translate>
          </span>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import VueScrollClass from 'vue-scroll-class'
import { mapGetters } from 'vuex'

export default {
  directives: {
    'scroll-class': VueScrollClass,
  },
  computed: {
    ...mapGetters({
      loading: 'project/getLoading',
      user: 'user/getProfile',
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails',
      draft: 'project/getProjectData',
      published: 'project/getPublished',
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
    isReadOnlyDraft() {
      return this.route === 'organisation-initiatives-id'
    },
    anon() {
      if (this.user) {
        return (
          !this.user.is_superuser &&
          ![...this.user.member, ...this.user.viewer].includes(
            +this.$route.params.id
          )
        )
      }
      return true
    },
    isTeam() {
      if (this.user) {
        return this.user.member.includes(+this.$route.params.id)
      }
      return false
    },
    project() {
      return this.isDraft || this.isReadOnlyDraft || this.isNewProject
        ? this.draft
        : this.published
    },
    showCountryFieldsLink() {
      const country = this.getCountryDetails(this.project.country)
      if (country) {
        return country.country_questions && country.country_questions.length > 0
      }
      return false
    },
    showDonorFieldsLink() {
      if (this.project && this.project.donors) {
        for (const donor of this.project.donors) {
          const details = this.getDonorDetails(donor)
          if (
            details &&
            details.donor_questions &&
            details.donor_questions.length > 0
          ) {
            return true
          }
        }
      }
      return false
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
    scrollTo(where) {
      window.location.hash = ''
      this.$nextTick(() => {
        this.$router.replace(`#${where}`)
      })
    },
    goToDraft() {
      const name = this.isTeam
        ? 'organisation-initiatives-id-edit'
        : 'organisation-initiatives-id'
      const localised = this.localePath({
        name,
        params: { ...this.$route.params },
      })
      this.$router.push(localised)
    },
    goToPublished() {
      const localised = this.localePath({
        name: 'organisation-initiatives-id-published',
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

    .SwitchButtons {
      .el-button {
        margin: 0 !important;
        padding: 0 10px;
        height: 29px;
        line-height: 29px;
        border: 0 !important;
        background-color: @colorGrayLighter;
        color: @colorTextSecondary;
        font-size: @fontSizeSmall + 1;
        text-transform: uppercase;

        &:not(.Active) {
          &:hover {
            background-color: darken(@colorGrayLighter, 5%);
            color: @colorTextPrimary;
          }
        }
      }

      .DraftButton {
        &.Active {
          color: @colorTextPrimary;
          background-color: @colorDraft;
        }
      }

      .PublishedButton {
        &.Active {
          color: @colorWhite;
          background-color: @colorPublished;
        }
      }
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
}
</style>
