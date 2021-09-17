<template>
  <div class="InitiativeCard" :class="{ Small: minimal }">
    <div v-if="project.thumbnail" class="cover" :style="`background-image: url(${project.thumbnail})`"></div>
    <div class="project">
      <nuxt-link :to="projectUrl">
        <h1>{{ title }}</h1>
      </nuxt-link>
      <div v-if="minimal" class="updated"><translate>Updated: </translate> {{ lastChange }}</div>
      <div v-if="project.is_draft" class="draft">
        <translate>draft</translate>
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
  props: {
    project: {
      type: Object,
      required: true,
    },
    minimal: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      currentUser: 'user/getProfile',
    }),
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
        top: 4px;
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
    .draft {
      position: absolute;
      top: 0;
      right: 0;
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
