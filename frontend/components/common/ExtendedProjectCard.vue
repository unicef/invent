<template>
  <el-card :body-style="{ padding: '0px' }" class="ExtendedProjectCard rounded">
    <div>
      <review-card-stripe v-if="type === 'review'" />
      <el-row
        type="flex"
        align="middle"
        class="FirstRow"
        justify="space-between"
      >
        <el-col class="ProjectName">
          <el-row class="FirstSubRow">
            <el-col>
              {{ projectData.name }}
            </el-col>
          </el-row>
          <el-row type="flex" align="middle" class="SecondSubRow">
            <country-item :id="projectData.country" :show-flag="true" />
            <organisation-item :id="projectData.organisation" />
            <organisation-item :id="projectData.organisation" />
          </el-row>
        </el-col>
        <el-row type="flex" align="center" justify="end">
          <el-col class="ProjectMeta">
            <div class="Donors">
              <div>
                {{ donors }}
              </div>
              <span><translate>Investor(s)</translate></span>
            </div>
          </el-col>
          <el-col class="ProjectMeta">
            <div class="LastChange">
              <div>
                {{ lastChange }}
              </div>
              <span><translate>Last updated</translate></span>
            </div>
          </el-col>
          <el-col>
            <project-legend :id="id" />
          </el-col>
        </el-row>
      </el-row>
      <el-row type="flex" justify="space-between" class="SecondRow">
        <el-col>
          <div v-if="!project.isPublished" class="ProjectStatus Draft">
            <translate key="draft"> Draft </translate>
          </div>
          <div v-if="project.isPublished" class="ProjectStatus Published">
            <translate key="published"> Published </translate>
          </div>
          <div
            v-if="projectData.approved"
            class="ProjectStatus approved-by-country"
          >
            <translate key="approved"> Approved by MOH </translate>
          </div>
        </el-col>
        <el-col>
          <project-card-actions :project="project" :force-show="false" />
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { format } from 'date-fns'

import ReviewCardStripe from '@/components/review/ReviewCardStripe'
import CountryItem from './CountryItem'
import OrganisationItem from './OrganisationItem'
import ProjectCardActions from './ProjectCardActions'
import ProjectLegend from './ProjectLegend'

export default {
  components: {
    CountryItem,
    OrganisationItem,
    ProjectCardActions,
    ProjectLegend,
    ReviewCardStripe,
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
    type: {
      type: String,
      default: 'regular',
    },
  },
  computed: {
    ...mapGetters({
      getUserProjectDetails: 'projects/getUserProjectDetails',
    }),
    project() {
      return this.getUserProjectDetails(this.id)
    },
    projectData() {
      return this.project.isPublished
        ? this.project.published
        : this.project.draft
    },
    donors() {
      return this.projectData && this.projectData.donors
        ? this.projectData.donors.length
        : 0
    },
    lastChange() {
      return format(this.projectData.modified, 'DD/MM/YYYY')
    },
  },
  methods: {},
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.ExtendedProjectCard {
  margin: 0 auto 20px;

  .FirstRow {
    position: relative;
    padding: 20px 30px 20px;

    .FirstSubRow {
      margin-bottom: 16px;
      font-size: @fontSizeLarger;
      font-weight: 700;
      color: @colorTextPrimary;
    }

    .SecondSubRow {
      .OrganisationItem {
        font-size: @fontSizeBase;
        font-weight: 400;
        color: @colorBrandGrayDark!important;
        padding: 0px 12px;
        border-left: 1px solid #ddd7d0;
      }
    }

    .ProjectName {
      width: 100%;
      padding-right: 40px;
    }

    .ProjectMeta {
      // min-width: 140px;
      border-left: 1px solid @colorGrayLight;
      padding: 0 24px 0px;

      .Donors,
      .LastChange {
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
      .svg-inline--fa {
        font-size: 14px;
      }
    }
  }

  .SecondRow {
    height: 54px;
    padding: 0 30px;
    align-items: center;
    background-color: #e8f6fd;

    .ProjectStatus {
      display: inline-block;
      height: 24px;
      min-width: 86px;
      margin-right: 10px;
      padding: 0 10px;
      font-size: @fontSizeSmall - 1;
      font-weight: 700;
      line-height: 24px;
      text-transform: uppercase;
      color: @colorWhite;
      border-radius: 12px;
      text-align: center;
      &.Draft {
        background-color: @colorDraft;
        color: @colorTextPrimary;
      }

      &.Published {
        background-color: @colorPublished;
      }

      &.approved-by-country {
        background-color: @colorApproved;
      }
    }
  }
}
</style>
