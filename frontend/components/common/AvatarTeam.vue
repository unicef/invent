<template>
  <div class="Team">
    <Avatar
      v-for="(member, index) in displayTeam"
      :key="member.id"
      :user="member"
      :show-hint="true"
      class="stacked"
      :style="`left: -${index * 8}px; z-index: ${100 - index}`"
    />
    <Avatar
      v-if="truncatedTeam"
      :user="additionalMembers"
      :show-hint="false"
      :show-initial="false"
      class="stacked"
      :style="`left: -${maxAvatars * 8}px; z-index: ${100 - maxAvatars}`"
    />
  </div>
</template>

<script>
import Avatar from '@/components/common/Avatar.vue'

export default {
  components: {
    Avatar,
  },
  props: {
    team: {
      type: Array,
      required: true,
    },
    maxAvatars: {
      type: Number,
      default: 3,
    },
    showHint: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    truncatedTeam() {
      const truncate = this.maxAvatars < this.team.length ? this.team.length - this.maxAvatars : 0
      return truncate
    },
    displayTeam() {
      return this.truncatedTeam ? this.team.slice(0, this.maxAvatars) : this.team
    },
    additionalMembers() {
      return {
        id: 0,
        name: `+${this.truncatedTeam}`,
        email: '',
        colorScheme: {
          text: '#7995A2',
          background: '#FFF',
          border: '1px solid #EAE6E1',
        },
      }
    },
  },
}
</script>

<style lang="less" scoped>
.Team {
  display: flex;
  .stacked {
    position: relative;
    &:hover {
      z-index: 1000 !important;
    }
  }
}
</style>
