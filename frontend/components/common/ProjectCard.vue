<template>
  <el-card
    :body-style="{ padding: hideBorders ? '0px' : '12px' }"
    :class="['ProjectCard', 'rounded', { hovered, HideBorders: hideBorders }]"
    :shadow="cardShadow"
  >
    <div
      @click="goToProject"
      @mouseenter="mouseEnterHandler"
      @mouseleave="mouseLeaveHandler"
    >
      <el-row type="flex">
        <el-col :span="22">
          <el-row class="ProjectName">
            <el-col>
              {{ project.name }}
            </el-col>
          </el-row>

          <el-row type="flex" class="ProjectCountryOrg">
            <el-col v-show="showCountry" class="Country">
              <country-item :id="project.country" />
            </el-col>
            <el-col v-show="showOrganisation" class="Organisation">
              <organisation-item :id="project.organisation" />
            </el-col>
            <el-col v-show="verified" class="Verified">
              <fa icon="check-circle" />
              <translate>Approved by MOH</translate>
            </el-col>
          </el-row>

          <el-row v-if="showFoundIn" type="flex" class="FoundIn">
            <el-col>
              <fa icon="search" size="xs" />
              <span>
                <translate :parameters="{ found }">
                  Found in "{found}"
                </translate>
              </span>
            </el-col>
          </el-row>
        </el-col>

        <el-col :span="2">
          <transition name="el-fade-in">
            <fa v-show="showArrow" icon="arrow-right" />
          </transition>
          <project-legend
            :id="project.id"
            :donors="project.donors"
            :country="project.country"
          />
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import ProjectLegend from './ProjectLegend'
import CountryItem from './CountryItem'
import OrganisationItem from './OrganisationItem'

export default {
  components: {
    ProjectLegend,
    CountryItem,
    OrganisationItem,
  },
  props: {
    project: {
      type: Object,
      default: () => ({}),
    },
    foundIn: {
      type: Array,
      default: () => [],
    },
    showCountry: {
      type: Boolean,
      default: false,
    },
    showOrganisation: {
      type: Boolean,
      default: false,
    },
    showFoundIn: {
      type: Boolean,
      default: false,
    },
    showVerified: {
      type: Boolean,
      default: false,
    },
    hideBorders: {
      type: Boolean,
      default: false,
    },
    showArrowOnOver: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      hovered: false,
    }
  },
  computed: {
    cardShadow() {
      return this.hideBorders ? 'never' : 'always'
    },
    showArrow() {
      return this.hovered && this.showArrowOnOver
    },
    verified() {
      return this.showVerified && this.project.approved
    },
    found() {
      const nameMApping = {
        country: this.$gettext('Country'),
        donor: this.$gettext('Investor'),
        loc: this.$gettext('Location'),
        name: this.$gettext('Name'),
        org: this.$gettext('Organisation'),
        overview: this.$gettext('Implementation Overview'),
        partner: this.$gettext('Partners'),
        region: this.$gettext('Region'),
      }
      if (this.foundIn && this.showFoundIn) {
        return this.foundIn.map((f) => nameMApping[f]).join(',')
      }
      return ''
    },
  },
  methods: {
    goToProject() {
      const path = this.localePath({
        name: 'organisation-initiatives-id-published',
        params: { ...this.$route.params, id: this.project.id },
      })
      this.$router.push(path)
    },
    mouseEnterHandler() {
      this.hovered = true
    },
    mouseLeaveHandler() {
      this.hovered = false
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.ProjectCard {
  cursor: pointer;

  // for MainTable
  // TODO
  // we might need a better name for this... 'InlineTableData'
  &.HideBorders {
    border: none;
    background-color: transparent;

    .ProjectName {
      color: @colorBrandPrimary;
      font-size: @fontSizeSmall;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 16px;
    }

    .ProjectCountryOrg {
      margin: 0;
    }
  }

  &.hovered {
    border-color: @colorTextMuted;

    .ProjectName {
      color: @colorBrandPrimary;
    }

    .ProjectCountryOrg {
      color: @colorTextPrimary;
    }

    .ProjectLegend {
      opacity: 0;
    }
  }

  .el-col {
    position: relative;
  }

  .ProjectName {
    padding-right: 16px;
    font-size: @fontSizeBase;
    line-height: 20px;
    font-weight: 700;
    color: @colorTextPrimary;
    transition: @transitionAll;
  }

  .ProjectCountryOrg {
    margin-top: 8px;
    font-size: @fontSizeSmall;
    color: @colorTextSecondary;
    white-space: nowrap;
    transition: @transitionAll;

    .Country {
      width: auto;
      padding-right: 21px;

      .CountryItem {
        .CountryFlag {
          img {
            height: 12px;
            width: auto;
          }
        }

        .CountryName {
          width: auto;
          margin-left: 6px;
          font-size: @fontSizeSmall;
          line-height: 14px;
          font-weight: 400;
        }
      }

      &::after {
        content: '';
        position: absolute;
        top: 50%;
        right: 10px;
        transform: translateY(-50%);
        display: inline-block;
        width: 1px;
        height: 12px;
        margin-top: -1px;
        background-color: @colorTextSecondary;
      }
    }

    .Organisation {
      position: relative;
      width: 100%;
    }

    .Verified {
      color: @colorApproved;
      font-size: @fontSizeSmall - 2;
      font-weight: 700;
      text-transform: uppercase;

      .svg-inline--fa {
        position: relative;
        top: 1px;
        margin-right: 1px;
      }
    }
  }

  .FoundIn {
    margin-top: 6px;
    font-size: @fontSizeSmall;
    color: @colorTextMuted;

    .svg-inline--fa {
      position: relative;
      top: -1px;
      margin-right: 4px;
    }
  }

  .ProjectLegend {
    position: absolute;
    top: 0;
    right: 6px;
  }

  .fa-arrow-right {
    position: absolute;
    top: 50%;
    right: 6px;
    transform: translateY(-50%);
    color: @colorBrandPrimary;
  }
}
</style>
