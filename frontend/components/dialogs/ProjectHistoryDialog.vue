<template>
  <el-dialog :visible.sync="visible" top="30vh" width="800px" @opened="showTimeline = true">
    <template v-if="projectHistory" #title>
      <div class="header">
        <div class="title">
          <translate :parameters="{ title: projectHistory.title }"> History of ’{title}’ </translate>
        </div>
        <div class="status">
          <StatusBadge :status="projectHistory.status" large />
          <translate
            :parameters="{ currentVersion: projectHistory.currentVersion, changed: projectHistory.changed }"
            class="change"
            >Version {currentVersion} on {changed}
          </translate>
          <el-switch v-model="projectHistory.teamMember" active-text="Team member" style="margin-left: auto;" />
        </div>
      </div>
    </template>
    <Timeline v-if="showTimeline">
      <!-- 
        As each timeline item can be totally different structure, it's very clean
        if we provide the component dynamically based on the prepared data from 
        the backend.
        -->
      <component
        :is="version.component"
        v-for="(version, index) in projectHistory.versions"
        :key="version.version"
        :version="version"
        :team-member="projectHistory.teamMember"
        :stack="timelineStack(index)"
      />
    </Timeline>
    <div v-else class="skeleton-wrapper">
      <div class="event skeleton"></div>
      <div class="avatar skeleton"></div>
      <div class="changes skeleton"></div>
    </div>
  </el-dialog>
</template>

<script>
import Timeline from '@/components/project/history/Timeline'
import StatusBadge from '@/components/project/history/StatusBadge'
import TimelineItem from '@/components/project/history/TimelineItem'
import TimelineItemNoData from '@/components/project/history/TimelineItemNoData'

export default {
  components: {
    Timeline,
    StatusBadge,
    TimelineItem,
    TimelineItemNoData,
  },
  loading: false,
  data() {
    return {
      visible: false,
      showTimeline: false,
      projectHistory: {},
    }
  },
  methods: {
    open(id) {
      this.getProjectHistory(id)
      this.visible = true
    },
    timelineStack(row) {
      return {
        row,
        rows: this.projectHistory.versions.length,
      }
    },
    async getProjectHistory(id) {
      const { data } = await this.$axios.get('mock/project.versions.json')
      this.projectHistory = data.projects.find((p) => (p.id = id))
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

::v-deep .el-dialog {
  margin: 50px auto 50px !important;
}

::v-deep .el-dialog .el-dialog__header .el-dialog__headerbtn {
  top: 30px;
}

::v-deep .el-dialog .el-dialog__body {
  padding: 0;
  overflow-y: auto;
  max-height: calc(100vh - 228px);
}

.header {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 14px 0;
  .title {
    font-size: 20px;
    line-height: 32px;
    color: #1cace3;
  }
  .status {
    display: flex;
    align-items: center;
    gap: 10px;
    .change {
      font-size: 14px;
      line-height: 20px;
      color: @colorTextMuted;
    }
  }
}

.skeleton-wrapper {
  display: flex;
  gap: 8px;
  padding: 1em;
  .event {
    width: 128px;
    height: 128px;
  }
  .avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
  }
  .changes {
    flex: 1;
    height: 128px;
  }

  .skeleton {
    background-image: linear-gradient(
      90deg,
      #eeeeee 0%,
      #eeeeee 40%,
      #dddddd 50%,
      #dddddd 55%,
      #eeeeee 65%,
      #eeeeee 100%
    );
    background-size: 400%;
    animation: shimmer 1500ms infinite;
  }
  @keyframes shimmer {
    from {
      background-position: 100% 100%;
    }
    to {
      background-position: 0 0;
    }
  }
}
</style>
