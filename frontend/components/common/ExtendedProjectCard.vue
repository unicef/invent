<template>
  <el-card
    :body-style="{ padding: '0px' }"
    class="ExtendedProjectCard rounded"
  >
    <div>
      <el-row
        type="flex"
        align="center"
        class="FirstRow"
      >
        <el-col
          :span="15"
          class="ProjectName"
        >
          <el-row class="FirstSubRow">
            <el-col>
              {{ projectData.name }}
            </el-col>
          </el-row>
          <el-row
            type="flex"
            justify="start"
            class="SecondSubRow"
          >
            <el-col>
              <country-item
                :id="projectData.country"
                :show-flag="true"
              />
            </el-col>
            <el-col>
              <organisation-item :id="projectData.organisation" />
            </el-col>
          </el-row>
        </el-col>

        <el-col
          :span="4"
          class="ProjectMeta"
        >
          <div class="Donors">
            <div>
              {{ donors }}
            </div>
            <span><translate>Investor(s)</translate></span>
          </div>
        </el-col>
        <el-col
          :span="4"
          class="ProjectMeta"
        >
          <div class="LastChange">
            <div>
              {{ lastChange }}
            </div>
            <span><translate>Updated on</translate></span>
          </div>
          <project-legend :id="id" />
        </el-col>
      </el-row>

      <el-row
        type="flex"
        justify="space-between"
        align="center"
        class="SecondRow"
      >
        <el-col>
          <div
            v-if="!project.isPublished"
            class="ProjectStatus Draft"
          >
            <translate key="draft">
              Draft
            </translate>
          </div>
          <div
            v-if="project.isPublished"
            class="ProjectStatus Published"
          >
            <translate key="published">
              Published
            </translate>
          </div>
          <div
            v-if="projectData.approved"
            class="ProjectStatus ApprovedByCountry"
          >
            <translate key="approved">
              Approved by MOH
            </translate>
          </div>
        </el-col>
        <el-col>
          <project-card-actions
            :project="project"
            :force-show="true"
          />
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { format } from 'date-fns';

import CountryItem from './CountryItem';
import OrganisationItem from './OrganisationItem';
import ProjectCardActions from './ProjectCardActions';
import ProjectLegend from './ProjectLegend';

export default {
  components: {
    CountryItem,
    OrganisationItem,
    ProjectCardActions,
    ProjectLegend
  },
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  computed: {
    ...mapGetters({
      getUserProjectDetails: 'projects/getUserProjectDetails'
    }),
    project () {
      return this.getUserProjectDetails(this.id);
    },
    projectData () {
      return this.project.isPublished ? this.project.published : this.project.draft;
    },
    donors () {
      return this.projectData && this.projectData.donors ? this.projectData.donors.length : 0;
    },
    lastChange () {
      return format(this.projectData.modified, 'DD/MM/YYYY');
    }
  },
  methods: {}
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

.ExtendedProjectCard {
  max-width: @cardSizeMedium;
  margin: 0 auto 20px;

  .FirstRow {
    position: relative;
    padding: 20px 50px 20px 30px;

    .FirstSubRow {
      margin-bottom: 16px;
      font-size: @fontSizeLarger;
      font-weight: 700;
      color: @colorTextPrimary;
    }

    .SecondSubRow {
      .el-col {
        &:first-child {
          width: auto;
        }

        &:last-child {
          width: 100%;
        }
      }

      .CountryItem {
        .CountryFlag {
          img {
            height: 14px;
            width: auto;
            margin: 1px 0;
          }
        }

        .CountryName {
          width: auto;
          font-size: @fontSizeBase;
          font-weight: 400;
        }
      }

      .OrganisationItem {
        position: relative;
        padding-left: 21px;
        font-size: @fontSizeBase;
        font-weight: 400;

        &::before {
          content: "";
          position: absolute;
          top: 50%;
          left: 10px;
          transform: translateY(-50%);
          display: inline-block;
          width: 1px;
          height: 14px;
          background-color: @colorTextSecondary;
        }
      }
    }

    .ProjectName {
      width: 100%;
      padding-right: 40px;
    }

    .ProjectMeta {
      min-width: 140px;
      max-width: 2000px;
      border-left: 1px solid @colorGrayLight;

      .Donors,
      .LastChange {
        padding: 0 20px;
        text-align: center;

        > div {
          margin: 8px 0 12px;
          font-size: @fontSizeMedium;
          font-weight: 700;
          color: @colorTextPrimary;
        }

        > span {
          display: block;
          font-size: @fontSizeSmall;
          color: @colorTextSecondary;
          white-space: nowrap;
        }
      }
    }

    .ProjectLegend {
      position: absolute;
      top: 26px;
      right: 26px;

      .svg-inline--fa {
        font-size: 14px;
      }
    }
  }

  .SecondRow {
    padding: 16px 30px;
    background-color: @colorBrandBlueLight;

    .ProjectStatus {
      display: inline-block;
      height: 24px;
      margin-right: 10px;
      padding: 0 10px;
      font-size: @fontSizeSmall - 1;
      font-weight: 700;
      line-height: 24px;
      text-transform: uppercase;
      color: @colorWhite;
      border-radius: 12px;

      &.Draft {
        background-color: @colorDraft;
        color: @colorTextPrimary;
      }

      &.Published {
        background-color: @colorPublished;
      }

      &.ApprovedByCountry {
        background-color: @colorApproved;
      }
    }

    .ProjectCardActions {}
  }
}

</style>
