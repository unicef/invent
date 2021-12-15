<template>
  <div class="FeaturedCards">
    <Header>
      <template #title>
        <translate>Featured Initiatives</translate>
      </template>

      <template #action>
        <LinkAction chevron="left" :disabled="firstProject" @click="prev">
          <translate>Prev</translate>
        </LinkAction>
        <LinkAction chevron="right" :disabled="lastProject" @click="next">
          <translate>Next</translate>
        </LinkAction>
      </template>
    </Header>
    <transition-group tag="div" name="card" class="content" appear>
      <div
        v-for="(card, index) in showCards"
        :key="card.id"
        class="card"
        :style="`z-Index: ${(showCards.length - index) * 10};
                 inset: ${index * 5}px;
                 transform: translateX(${(index - 0) * 6}px);
                 ${background(card.thumbnail)}`"
      >
        <div v-if="card.thumbnail" class="details">
          <div class="title" @click="openProject(card)">{{ card.name }}</div>
          <div class="team">
            <Location :location-info="locationInfo(card)" class="bright" />
            <AvatarTeam :team="team(card)" :max-avatars="10" />
          </div>
        </div>
        <div v-if="!card.thumbnail" class="title">
          {{ card.name }}
        </div>
        <div v-if="!card.thumbnail" class="team">
          <Location :location-info="locationInfo(card)" />
          <AvatarTeam :team="team(card)" :max-avatars="10" />
        </div>
        <div v-if="!card.thumbnail">
          <p class="desc">
            {{ card.description }}
          </p>
          <nuxt-link :to="projectUrl(card)" class="link">
            <translate>Learn more</translate>
            <fa icon="chevron-right" size="sm" />
          </nuxt-link>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Header from '@/components/landing/parts/Header.vue'
import LinkAction from '@/components/common/LinkAction.vue'
import Location from '@/components/landing/parts/Location.vue'
import AvatarTeam from '@/components/common/AvatarTeam.vue'

export default {
  components: {
    Header,
    LinkAction,
    Location,
    AvatarTeam,
  },
  props: {
    projects: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      currentCard: 0,
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'user/getProfile',
    }),
    showCards() {
      const toSlice = this.projects.length - this.currentCard > 3 ? this.currentCard + 3 : this.projects.length
      return this.projects.slice(this.currentCard, toSlice)
    },
    firstProject() {
      return this.currentCard === 0
    },
    lastProject() {
      return this.currentCard === this.projects.length - 1
    },
  },
  methods: {
    background(thumbnail) {
      return thumbnail ? `background-image: url(${thumbnail});` : ''
    },
    team(project) {
      const team = project.team.map((member) => {
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
    locationInfo(project) {
      return {
        countryCode: project.country?.code,
        country: project.country?.name,
        office: project.unicef_office?.name,
        region: project.country?.unicef_region?.name,
      }
    },
    projectUrl(project) {
      const status = project.is_draft ? 'edit' : 'published'
      return this.localePath({
        name: `organisation-initiatives-id-${status}`,
        params: {
          id: project.id,
          organisation: this.$route.params.organisation,
        },
      })
    },
    openProject(project) {
      const status = project.is_draft ? 'edit' : 'published'
      this.$router.push({
        path: this.localePath({
          name: `organisation-initiatives-id-${status}`,
          params: {
            id: project.id,
            organisation: this.$route.params.organisation,
          },
        }),
      })
    },
    next() {
      if (this.lastProject) return
      this.currentCard++
    },
    prev() {
      if (this.firstProject) return
      this.currentCard--
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.FeaturedCards {
  .bright {
    color: #f5f3ef;
    margin-bottom: 14px;
  }
  .content {
    position: relative;
    height: 520px;
    .card {
      position: absolute;
      box-sizing: border-box;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 30px;
      padding: 38px 34px;
      width: 590px;
      border-radius: 6px;
      background-color: @colorWhite;
      box-shadow: 1px 2px 4px #0000001f;
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center;
      .title {
        font-size: @fontSizeHeadline;
        color: @colorBrandPrimary;
        letter-spacing: -1px;
        line-height: 42px;
        max-height: 126px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
      }
      .desc {
        margin: 2px 0 24px 0;
        color: @colorTextPrimary;
        font-size: @fontSizeLarge;
        line-height: 27px;
        max-height: 108px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
      }
      .details {
        box-sizing: border-box;
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 0 36px 32px 36px;
        background-image: linear-gradient(transparent, #000000b8);
        .title {
          cursor: pointer;
          color: @colorWhite;
          font-size: @fontSizeHeadline;
          letter-spacing: -1px;
          line-height: 42px;
          max-height: 84px;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          margin-bottom: 24px;
        }
      }
      .link {
        font-size: @fontSizeBase;
        color: @colorBrandPrimary;
        font-weight: bold;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        svg {
          font-size: 1em;
          margin-left: 8px;
        }
      }
    }
  }
}

.card {
  transition: all 0.3s;
}
.card-enter,
.card-leave-to {
  opacity: 0;
  transform: scale(0.5);
}
.card-enter-to {
  opacity: 1;
  transform: scale(1);
}
.card-move {
  opacity: 1;
  transition: all 0.3s;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active {
  transition-delay: 0.2s;
}
</style>
