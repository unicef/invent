<template>
  <div class="InitiativeCard" :class="{ Small: minimal }">
    <div v-if="project.thumbnail" class="cover" :style="background"></div>
    <div class="project">
      <nuxt-link :to="projectUrl">
        <h1>{{ title }}</h1>
      </nuxt-link>
      <div v-if="minimal" class="updated"><translate>Updated: </translate> {{ lastChange }}</div>
      <div class="left-top">
        <div v-if="project.is_draft" class="draft">
          <translate>draft</translate>
        </div>
        <div class="popup-menu" v-if="showActions">
          <i class="el-icon-more rotate-90 more-icon" @click="toggleMiniMenu()"></i>
        </div>
        <div tabindex="0" ref="popover" @focusout="menuVisible = false" v-if="showActions">
          <el-popover placement="top-end" width="170" v-model="menuVisible">
            <nuxt-link
              v-if="!project.is_draft"
              :to="
                localePath({
                  name: 'organisation-initiatives-id-published',
                  params: {
                    id: project.id,
                    organisation: $route.params.organisation,
                  },
                })
              "
              class="NuxtLink IconLeft popover-button"
            >
              <fa icon="arrow-right" />
              <translate>View Published</translate>
            </nuxt-link>
            <nuxt-link
              :to="
                localePath({
                  name: 'organisation-initiatives-id',
                  params: {
                    id: project.id,
                    organisation: $route.params.organisation,
                  },
                })
              "
              class="NuxtLink IconLeft popover-button"
            >
              <fa icon="arrow-right" />
              <translate>View Draft</translate>
            </nuxt-link>
            <nuxt-link
              v-if="showActions"
              :to="
                localePath({
                  name: 'organisation-initiatives-id-edit',
                  params: {
                    id: project.id,
                    organisation: $route.params.organisation,
                  },
                })
              "
              class="NuxtLink IconLeft popover-button"
            >
              <fa icon="edit" />
              <translate>Edit</translate>
            </nuxt-link>
          </el-popover>
        </div>
      </div>

      <Location :location-info="locationInfo" :size="locationSize" />

      <div v-if="!minimal" class="bottom">
        <AvatarTeam :team="team" :max-avatars="10" />
        <div class="updated"><translate>Updated: </translate> {{ lastChange }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns'
import { mapGetters } from 'vuex'
import Location from '@/components/landing/parts/Location.vue'
import AvatarTeam from '@/components/common/AvatarTeam.vue'

export default {
  components: {
    Location,
    AvatarTeam,
  },
  data() {
    return {
      menuVisible: false,
    }
  },
  props: {
    project: {
      type: Object,
      required: true,
    },
    minimal: {
      type: Boolean,
      default: false,
    },
    showActions: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    toggleMiniMenu() {
      this.menuVisible = !this.menuVisible
      if (this.menuVisible) {
        this.$refs.popover.focus()
      }
    },
  },
  computed: {
    ...mapGetters({
      currentUser: 'user/getProfile',
    }),
    background() {
      return this.project.thumbnail ? `background-image: url(${this.project.thumbnail})` : ''
    },
    title() {
      return this.project?.name
    },
    team() {
      const team = this.project.team.map((member) => {
        if (member.id === this.currentUser.id) {
          return {
            ...member,
            colorScheme: {
              text: '#FFFFFF',
              background: '#CB7918',
              border: '2px solid #FFF',
            },
          }
        } else return member
      })
      return team
    },
    locationInfo() {
      return {
        countryCode: this.project.country?.code,
        country: this.project.country?.name,
        office: this.project.unicef_office?.name,
        region: this.project.country?.unicef_region?.name,
      }
    },
    locationSize() {
      return this.minimal ? 'tiny' : 'small'
    },
    lastChange() {
      return format(this.project.modified, 'DD/MM/YYYY')
    },
    projectUrl() {
      const status = this.project.is_draft ? 'edit' : 'published'
      return this.localePath({
        name: `organisation-initiatives-id-${status}`,
        params: {
          id: this.project.id,
          organisation: this.$route.params.organisation,
        },
      })
    },
    showViewDraft() {
      return this.project.isViewer || this.project.isMember
    },
    showEditDraft() {
      return this.project.isMember
    },
    showViewPublished() {
      return this.project.isPublished
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.InitiativeCard {
  display: flex;
  height: 160px;
  background-color: @colorWhite;
  box-shadow: 1px 2px 4px #0000001f;
  margin-bottom: 20px;
  &.Small {
    height: 78px;
    margin-bottom: 15px;
    .thumbnail {
      flex-basis: 104px;
    }
    .project {
      a h1 {
        margin: 0 0 8px 0;
        font-size: @fontSizeMedium;
        -webkit-line-clamp: 1;
      }
      .updated {
        position: absolute;
        right: 0;
        bottom: 0;
        color: #7995a2;
        font-size: @fontSizeSmall;
      }
      .location {
        font-size: @fontSizeSmall;
      }
    }
  }

  .cover {
    flex-basis: 213px;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center bottom;
  }

  .project {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
    margin: 16px 24px;
    margin-right: 16px;
    .left-top {
      position: absolute;
      top: 0;
      right: 0;
      display: inline-block;
      width: auto;
    }
    /deep/ .el-popover {
      top: 0;
      right: 0;
      border: 0px;
      box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.18);
      border-radius: 0px;
      padding: 0;
    }
    .popover-button {
      display: block;
      padding: 10px;
      padding-left: 15px;
      text-decoration: none;
    }
    .popover-button:hover {
      background-color: #e8f6fd;
      text-decoration: none;
    }
    .popup-menu {
      display: inline-block;
    }
    .rotate-90 {
      transform: rotate(90deg);
    }
    .more-icon {
      color: #7995a2;
    }
    .more-icon:hover {
      color: black;
      cursor: pointer;
    }
    .draft {
      vertical-align: top;
      display: inline-block;
      padding: 5px 9px 3px 9px;
      color: @colorTextPrimary;
      font-weight: bold;
      font-size: @fontSizeExtraSmall;
      text-transform: uppercase;
      background-color: @colorDraft;
      border-radius: 12px;
    }
    a {
      color: @colorBrandPrimary;
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
      h1 {
        margin: 0 0 12px 0;
        // max-width: 418px;
        max-width: 90%;
        font-size: 20px;
        line-height: 25px;
        letter-spacing: -0.31px;
        max-height: 50px;
        color: @colorBrandPrimary;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
    }
    .location {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      color: #7995a2;
      font-size: @fontSizeBase;
      margin-bottom: 14px;
      span {
        color: @colorBrandGrayLight;
      }
    }
    .bottom {
      position: absolute;
      width: 100%;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      .updated {
        color: #7995a2;
        font-size: @fontSizeSmall;
      }
    }
  }
  &.small {
    height: 78px;
    gap: 15px;
  }
}
</style>
