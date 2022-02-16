<template>
  <el-dialog :visible.sync="visible" top="30vh" width="800px" @opened="showTimeline = true">
    <template #title>
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
        </div>
      </div>
    </template>
    <Timeline v-if="showTimeline">
      <TimeLineItem
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
import TimeLineItem from '@/components/project/history/TimeLineItem'

export default {
  components: {
    Timeline,
    StatusBadge,
    TimeLineItem,
  },
  data() {
    return {
      visible: false,
      showTimeline: false,
      projectHistory: {
        title: 'EduTrac - Online Information Platform',
        currentVersion: 5,
        changed: '2022-01-23',
        status: 'draft',
        teamMember: false,
        versions: [
          {
            status: 'unpublished',
            version: 5,
            changed: '2022-01-23',
            user: {
              name: 'Ian Doe',
              email: 'id@pulilab.com',
              colorScheme: {
                text: '#FFFFFF',
                background: '#CB7918',
                border: 'none',
              },
            },
            changes: [
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
            ],
          },
          {
            status: 'draft',
            version: 4,
            changed: '2022-01-23',
            user: {
              name: 'Joe Doe',
              email: 'jd@pulilab.com',
              colorScheme: {
                text: '#FFFFFF',
                background: '#CB7918',
                border: 'none',
              },
            },
            changes: [
              {
                field: '',
                fieldTitle: 'Completion of initiative phases',
                oldValue: '‘Opportunity and Ideation’ on 06-06-2021', // N/A
                newValue: '‘Piloting and Evidence Generation’ on 20-10-2021',
              },
              {
                field: '',
                fieldTitle: 'UNICEF Office',
                oldValue: '', // N/A
                newValue: 'UNICEF Uganda, Kampala, Uganda, ESAR',
              },
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
            ],
          },
          {
            status: 'published',
            version: 3,
            changed: '2022-01-23',
            user: {
              name: 'Joe Doe',
              email: 'jd@pulilab.com',
              colorScheme: {
                text: '#FFFFFF',
                background: '#CB7918',
                border: 'none',
              },
            },
            changes: [
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
            ],
          },
          {
            status: 'draft',
            version: 2,
            changed: '2022-01-23',
            user: {
              name: 'Joe Doe',
              email: 'jd@pulilab.com',
              colorScheme: {
                text: '#FFFFFF',
                background: '#CB7918',
                border: 'none',
              },
            },
            changes: [
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
            ],
          },
          {
            status: 'draft',
            version: 1,
            changed: '2022-01-23',
            user: {
              name: 'Joe Doe',
              email: 'jd@pulilab.com',
              colorScheme: {
                text: '#FFFFFF',
                background: '#CB7918',
                border: 'none',
              },
            },
            changes: [
              {
                field: '',
                fieldTitle: 'Overview of the digital health implementation',
                oldValue: '', // N/A
                newValue:
                  'The ministry is using EduTrac to monitor education indicators that need to be collected on a more frequent basis… More',
              },
            ],
          },
          {
            status: 'noversion',
            version: 0,
            changed: '2022-01-23',
            changes: [],
          },
        ],
      },
    }
  },
  methods: {
    open() {
      this.visible = true
    },
    timelineStack(row) {
      return {
        row,
        rows: this.projectHistory.versions.length,
      }
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
