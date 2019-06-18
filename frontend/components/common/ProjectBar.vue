<template>
  <div class="ProjectBar">
    <div class="ProjectBarWrapper">
      <el-row
        type="flex"
        justify="space-between"
      >
        <el-col
          :span="12"
          class="ProjectName"
        >
          <div>
            {{ project.name }}
            <project-legend :id="project.id" />
          </div>
        </el-col>

        <el-col
          :span="12"
          class="ProjectInfo"
        >
          <el-row
            type="flex"
            justify="end"
          >
            <el-col
              :span="8"
              class="InfoSection"
            >
              <div class="Label">
                <translate>Last Updated</translate>
              </div>
              <div class="Info">
                {{ modified }}
              </div>
            </el-col>
            <el-col
              :span="8"
              class="InfoSection"
            >
              <div class="Label">
                <translate>Organisation</translate>
              </div>
              <div class="Info">
                <organisation-item :id="project.organisation" />
              </div>
            </el-col>
            <el-col
              :span="8"
              class="InfoSection"
            >
              <div class="Label">
                <translate>Contact person</translate>
              </div>
              <div class="Info">
                <a
                  :href="`mailto:${project.contact_email}`"
                  class="NuxtLink Small IconRight"
                >
                  {{ project.contact_name }}
                  <fa icon="envelope" />
                </a>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>

      <div class="ProjectMenu">
        <nuxt-link
          v-if="isTeam"
          :class="{'Active': isProjectActive}"
          :to="localePath({name: 'organisation-projects-id-edit', params: {id, organisation: $route.params.organisation}})"
        >
          <translate>Project</translate>
        </nuxt-link>
        <nuxt-link
          v-if="isViewer && !isTeam"
          :class="{'Active': isProjectActive}"
          :to="localePath({name: 'organisation-projects-id', params: {id, organisation: $route.params.organisation}})"
        >
          <translate>Project</translate>
        </nuxt-link>
        <nuxt-link
          v-if="anon"
          :class="{'Active': isProjectActive}"
          :to="localePath({name: 'organisation-projects-id-published', params: {id, organisation: $route.params.organisation}})"
        >
          <translate>Project</translate>
        </nuxt-link>
        <nuxt-link :to="localePath({name: 'organisation-projects-id-assessment', params: {id, organisation: $route.params.organisation}})">
          <translate>Assessment</translate>
        </nuxt-link>
        <nuxt-link
          v-if="isTeam"
          :class="{'Active': isUpdateScoreActive}"
          :to="localePath({name: 'organisation-projects-id-toolkit', params: {id, organisation: $route.params.organisation}})"
        >
          <translate>Update score</translate>
        </nuxt-link>
        <nuxt-link
          v-if="isTeam"
          :class="{'Active': isScorecardActive}"
          :to="localePath({name: 'organisation-projects-id-toolkit-scorecard', params: {id, organisation: $route.params.organisation}})"
        >
          <translate>Summary score</translate>
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns';
import { mapGetters } from 'vuex';
import OrganisationItem from './OrganisationItem';
import ProjectLegend from './ProjectLegend';

export default {
  components: {
    OrganisationItem,
    ProjectLegend
  },
  computed: {
    ...mapGetters({
      draft: 'project/getProjectData',
      published: 'project/getPublished',
      user: 'user/getProfile'
    }),
    project () {
      return this.published && this.published.name ? this.published : this.draft;
    },
    id () {
      return +this.$route.params.id;
    },
    route () {
      return this.$route.name.split('__')[0];
    },
    isProjectActive () {
      return this.route === 'organisation-projects-id-published' ||
      this.route === 'organisation-projects-id-edit' ||
      this.route === 'organisation-projects-id';
    },
    isUpdateScoreActive () {
      return this.route === 'organisation-projects-id-toolkit';
    },
    isScorecardActive () {
      return this.route === 'organisation-projects-id-toolkit-scorecard';
    },
    isTeam () {
      if (this.user) {
        return this.user.member.includes(+this.$route.params.id);
      }
      return false;
    },
    isViewer () {
      if (this.user) {
        return this.user.is_superuser || this.user.viewer.includes(+this.$route.params.id);
      }
      return true;
    },
    anon () {
      return !this.isViewer && !this.isTeam;
    },
    modified () {
      if (this.project) {
        return format(this.project.modified, 'DD-MM-YYYY');
      }
      return null;
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .ProjectBar {
    background-color: @colorWhite;
    border-bottom: 1px solid @colorGrayLight;

    .ProjectBarWrapper {
      overflow: hidden;
      .limitPageWidth();
    }

    .ProjectName {
      margin: 14px 0 0;
      font-size: @fontSizeLarge;
      line-height: 22px;
      font-weight: 700;

      > div {
        position: relative;
        display: inline-block;
        max-width: 100%;
        padding-right: 50px;
        .textTruncate();
      }

      .ProjectLegend {
        position: absolute;
        top: -2px;
        right: 25px;
      }
    }

    .ProjectInfo {
      width: auto;

      .InfoSection {
        width: auto;
        white-space: nowrap;
        margin: 10px 0 0;
        padding: 2px 20px;
        border-left: 1px solid @colorGrayLighter;

        &:last-of-type {
          padding-right: 10px;
        }

        .Label {
          margin: 0 0 4px;
          font-size: @fontSizeSmall - 1;
          color: @colorGray;
        }

        .Info {
          font-size: @fontSizeSmall;
          font-weight: 700;
          color: @colorTextPrimary;
        }
      }
    }

    .ProjectMenu {
      a {
        position: relative;
        display: inline-block;
        margin-right: 10px;
        line-height: 40px;
        padding: 0 10px;
        font-size: @fontSizeBase;
        font-weight: 700;
        color: @colorTextSecondary;
        text-decoration: none;
        transform: translateY(-4px);
        transition: @transitionAll;

        &.Active, &.nuxt-link-exact-active {
          color: @colorBrandPrimary !important;

          &::before {
            background-color: @colorBrandPrimary;
            transform: translateY(3px);
          }
        }

        &::before {
          content: "";
          position: absolute;
          bottom: -1px;
          left: 0;
          display: inline-block;
          width: 100%;
          height: 4px;
          background-color: @colorGray;
          transform: translateY(7px);
          transition: @transitionAll;
        }

        &:hover {
          color: @colorTextPrimary;

          // &::before {
          //   transform: translateY(3px);
          // }
        }
      }
    }
  }
</style>
