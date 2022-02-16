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
      <div v-for="(change, index) in shownChanges" :key="index" class="change">
        <div class="field">{{ index + 1 }}) {{ change.fieldTitle }}</div>
        <div class="value old">
          <i class="el-icon-remove-outline"></i>
          <div v-if="change.oldValue">
            {{ change.oldValue }}
          </div>
          <div v-else>N/A</div>
        </div>
        <div class="value">
          <i class="el-icon-circle-plus-outline"></i>
          <div>
            {{ change.newValue }}
          </div>
        </div>
      </div>
      <div v-if="!showAll && moreToShow > 0" class="showall" @click="showAll = !showAll">
        <translate>Show all changes (+{{ moreToShow }})</translate>
      </div>
    </div>
  </div>
</template>

<script>
import StatusBadge from '@/components/project/history/StatusBadge.vue'
import { Boolean } from 'pdfmake/build/pdfmake'

export default {
  components: {
    StatusBadge,
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

<style lang="less">
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
      &:only-child,
      &:last-child {
        border-bottom: none;
        padding-bottom: 0;
      }
      .field {
        font-weight: bold;
      }
      .value {
        display: flex;
        gap: 10px;
        margin-left: 19px;
        margin-top: 10px;
        color: @colorTextPrimary;
        &.old {
          color: @colorTextMuted;
        }
      }
      i {
        margin-top: 1px;
      }
    }
    .showall {
      cursor: pointer;
      margin-top: 1px;
      color: @colorBrandPrimary;
    }
  }
}
</style>
