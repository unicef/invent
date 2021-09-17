<template>
  <div class="InitiativesSection">
    <div class="initiative-wrapper">
      <Header v-if="landingProjects.my_initiatives.length > 0">
        <template #title>
          <translate>My Initiatives</translate>
        </template>

        <template #action>
          <LinkAction :url="myInitiativesUrl" chevron="right">
            <translate :parameters="{ num: landingProjects.my_initiatives_count }"> See all ({num}) </translate>
          </LinkAction>
        </template>
      </Header>
      <div class="content">
        <InitiativeCard v-for="project in landingProjects.my_initiatives" :key="project.id" :project="project" />
        <Header v-if="showRecents.length > 0" :postion="recentHeaderPosition">
          <template #title>
            {{ recentTitle }}
          </template>
        </Header>
        <InitiativeCard
          v-for="project in showRecents"
          :key="project.id"
          :project="project"
          :minimal="landingProjects.my_initiatives.length > 0"
        />
      </div>
    </div>
    <FeaturedCards class="featured-wrapper" :projects="landingProjects.featured" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Header from '@/components/landing/parts/Header.vue'
import LinkAction from '@/components/common/LinkAction.vue'
import InitiativeCard from '@/components/landing/parts/InitiativeCard.vue'
import FeaturedCards from '@/components/landing/FeaturedCards.vue'

export default {
  components: {
    Header,
    LinkAction,
    InitiativeCard,
    FeaturedCards,
  },
  data() {
    return {
      recentCounts: [3, 3, 1, 0],
    }
  },
  computed: {
    ...mapGetters({
      landingProjects: 'projects/getLandingProjects',
    }),
    myInitiativesUrl() {
      return this.localePath({
        name: 'organisation-initiatives',
      })
    },
    showRecents() {
      return this.landingProjects.recents.slice(0, this.recentCounts[this.landingProjects.my_initiatives.length])
    },
    recentHeaderPosition() {
      return this.landingProjects.my_initiatives.length === 0 ? 'top' : 'between'
    },
    recentTitle() {
      return this.landingProjects.my_initiatives.length === 0
        ? this.$gettext('Recently Updated Initiatives')
        : this.$gettext('Recently Updated')
    },
  },
}
</script>

<style lang="less" scoped>
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.action {
  font-size: @fontSizeBase;
}

.InitiativesSection {
  display: flex;
  gap: 60px;
  padding: 50px 83px 60px 100px;

  .link {
    text-decoration: none;
    svg {
      font-size: 1em;
      margin-left: 4px;
    }
  }

  .initiative-wrapper {
    flex: 1;
    .content {
      display: flex;
      flex-direction: column;
    }
  }
  .featured-wrapper {
    width: 607px;
  }
}
</style>
