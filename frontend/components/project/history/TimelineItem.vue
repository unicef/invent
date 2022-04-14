<template>
  <div v-if="showInternalInfo" class="TimeLineItem">
    <div class="event">
      <translate
        v-if="version.version && teamMember"
        tag="div"
        :parameters="{ version: version.version }"
        class="version"
      >
        Version {version}
      </translate>
      <div>{{ version.changed }}</div>
      <translate
        v-if="version.changes.length > 0"
        tag="div"
        :parameters="{ changes: version.changes.length }"
        class="changed"
      >
        {changes} changes
      </translate>
    </div>
    <div :class="`divider ${dividerStyle}`">
      <Avatar :user="versionCreator" :show-hint="false" class="avatar" />
    </div>
    <TimelineItemBody :version="version" :team-member="teamMember" />
  </div>
</template>

<script>
import Avatar from '@/components/common/Avatar.vue'
import TimelineItemBody from '@/components/project/history/TimelineItemBody.vue'

export default {
  name: 'TimeLineItem',
  components: {
    Avatar,
    TimelineItemBody,
  },
  props: {
    version: {
      type: Object,
      required: true,
    },
    teamMember: {
      type: Boolean,
      default: true,
    },
    stack: {
      type: Object,
      default() {
        return {
          row: 0,
          rows: 1,
        }
      },
    },
  },
  computed: {
    showInternalInfo() {
      return (this.version?.version && this.teamMember) || this.version.status === 'published'
    },
    versionCreator() {
      return this.version.status === 'noversion' || this.version.user !== null
        ? {
            ...this.version.user,
            colorScheme: {
              text: '#FFFFFF',
              background: '#CB7918',
              border: 'none',
            },
          }
        : {
            name: null,
            email: null,
            icon: 'el-icon-s-tools',
            colorScheme: {
              text: '#FFFFFF',
              background: '#1CABE2',
              border: 'none',
            },
          }
    },
    dividerStyle() {
      if (this.stack.rows === 1) return 'onlyone'
      if (this.stack.row === 0) return 'first'
      if (this.stack.row === this.stack.rows - 1) return 'last'
      return ''
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.TimeLineItem {
  display: flex;
  .event {
    display: flex;
    flex-direction: column;
    font-size: 14px;
    line-height: 20px;
    color: @colorTextPrimary;
    padding-top: 14px;
    .version {
      font-weight: bold;
    }
    .changed {
      font-size: 12px;
      line-height: 16px;
      color: @colorTextMuted;
    }
  }
  .divider {
    position: relative;
    display: flex;
    justify-content: center;
    width: 90px;
    &::before {
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      border-left: 1px solid #eae6e1;
    }
    &.onlyone {
      &::before {
        border-left: 1px solid transparent;
      }
    }
    &.first {
      &::before {
        top: 30px;
      }
    }
    &.last {
      &::before {
        bottom: 48px;
      }
    }
    .avatar {
      position: relative;
      z-index: 1;
      top: 15px;
      width: 30px;
      height: 30px;
      line-height: 30px;
    }
  }
}
</style>
