<template>
  <div :class="style">
    <div class="header">
      <div>
        <span>{{ actions[version.status] }}</span>
        <span v-if="version.user" class="user">{{ version.user.name }}</span>
      </div>
      <StatusBadge v-if="teamMember" :status="version.status" />
    </div>
    <div v-if="showChanges" class="changes">
      <transition-group tag="div" name="version">
        <component
          :is="changes.component"
          v-for="(changes, i) in shownChanges"
          :key="changes.key"
          :index="i"
          :changes="changes"
        />
      </transition-group>
      <div v-if="!showAll && moreToShow > 0" class="showall" @click="showAll = !showAll">
        <translate>Show all changes</translate> (+{{ moreToShow }})
      </div>
    </div>
  </div>
</template>

<script>
import StatusBadge from '@/components/project/history/StatusBadge.vue'
import ValueText from '@/components/project/history/values/ValueText.vue'
import ValuePhases from '@/components/project/history/values/ValuePhases.vue'
import ValueWebsites from '@/components/project/history/values/ValueWebsites.vue'
import ValueTags from '@/components/project/history/values/ValueTags.vue'
import ValuePartners from '@/components/project/history/values/ValuePartners.vue'
import ValueSpecial from '@/components/project/history/values/ValueSpecial.vue'
import SimpleMessage from '@/components/project/history/values/SimpleMessage.vue'
import ValueCoverImage from '@/components/project/history/values/ValueCoverImage.vue'

export default {
  components: {
    StatusBadge,
    ValueText,
    ValuePhases,
    ValueWebsites,
    ValueTags,
    ValuePartners,
    ValueSpecial,
    SimpleMessage,
    ValueCoverImage,
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
  },
  data() {
    return {
      actions: {
        // Additional states.. will implement on integration
        // created
        // a draft version was present
        // a published version was found
        // no data
        noversion: this.$gettext('A published version was found'),
        draft: this.$gettext('Saved draft by'),
        published: this.$gettext('Published by'),
        unpublished: this.$gettext('Unpublished by'),
      },
      showAll: false,
    }
  },
  computed: {
    style() {
      return this.teamMember ? `TimeLineItemBody ${this.version.status}` : 'TimeLineItemBody draft'
    },
    shownChanges() {
      return this.showAll ? this.version.changes : this.version.changes.slice(0, 2)
    },
    showChanges() {
      return this.version.changes && this.version.changes.length > 0
    },
    moreToShow() {
      return this.version.changes && this.version.changes.length > 2 ? this.version.changes.length - 2 : 0
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.TimeLineItemBody {
  box-sizing: border-box;
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 20px;
  margin-left: 18px;
  margin-bottom: 20px;
  border-radius: 8px;
  min-height: 60px;
  max-width: 480px;
  &::before {
    content: '';
    position: absolute;
    top: 15px;
    left: -15px;
    width: 0;
    height: 0;
    border-top: 14px solid transparent;
    border-bottom: 14px solid transparent;
  }
  &::after {
    content: '';
    position: absolute;
    top: 15px;
    left: -14px;
    width: 0;
    height: 0;
    border-top: 14px solid transparent;
    border-bottom: 14px solid transparent;
  }
  &.draft,
  &.noversion {
    background-color: #f5f3ef;
    &::before {
      border-right: 14px solid #f5f3ef;
    }
    &::after {
      border-right: 14px solid #f5f3ef;
    }
  }
  &.published {
    background-color: white;
    border: 1px solid #7ecea0;
    &::before {
      border-right: 14px solid #7ecea0;
    }
    &::after {
      border-right: 14px solid white;
    }
  }
  &.unpublished {
    background-color: #feedec;
    border: 1px solid #f8beba;
    &::before {
      border-right: 14px solid #f8beba;
    }
    &::after {
      border-right: 14px solid #feedec;
    }
  }

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    .user {
      margin-left: 4px;
      font-weight: bold;
    }
  }

  .changes {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding-top: 15px;
    .change {
      border-bottom: 1px solid #eae6e1;
      padding-bottom: 15px;
      margin-bottom: 15px;
      &:only-child,
      &:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
      }
    }
    .showall {
      cursor: pointer;
      margin-top: 1px;
      color: @colorBrandPrimary;
    }
  }
  .version-enter {
    opacity: 0;
    transform: translateY(-20px);
  }
  .version-enter-active {
    transition: all 0.4s ease;
  }
}
</style>
