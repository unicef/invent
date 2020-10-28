<template>
  <el-col class="Breadcrumb">
    <el-row type="flex" align="middle">
      <el-col class="Home">
        <nuxt-link
          :to="localePath({ name: 'organisation', params: $route.params })"
        >
          <fa icon="home" />
        </nuxt-link>
      </el-col>
      <template v-if="subPageName">
        <el-col class="Sep">
          <fa icon="angle-right" size="sm" />
        </el-col>
        <el-col :key="subPageName" class="Page">
          {{ subPageName }}
        </el-col>
      </template>
    </el-row>
  </el-col>
</template>

<script>
export default {
  computed: {
    pureRoute() {
      if (this.$route && this.$route.name) {
        return this.$route.name.split('___')[0]
      }
      return null
    },
    subPageName() {
      const noSubPage = {
        organisation: true,
        'organisation-login': true,
        'organisation-signup': true,
        'organisation-reset-key': true,
        'organisation-portfolio-management-new': false,
        'organisation-portfolio-management-id': true,
      }
      const pages = {
        'organisation-edit-profile': this.$gettext('Admin'),
        'organisation-admin-country': this.$gettext('Admin'),
        'organisation-admin-donor': this.$gettext('Admin'),
        'organisation-admin-import': this.$gettext('Admin'),
        'organisation-admin-import-id': this.$gettext('Admin'),
        'organisation-inventory': this.$gettext('TIIP Inventory'),
        'organisation-inventory-list': this.$gettext('TIIP Inventory'),
        'organisation-initiatives': this.$gettext('My initiatives'),
        'organisation-initiatives-id-published': this.$gettext(
          'Published Initiative'
        ),
        'organisation-initiatives-id-edit': this.$gettext('Edit Initiative'),
        'organisation-initiatives-id': this.$gettext('Drafted Initiative'),
        'organisation-cms': this.$gettext('Planning and Guidance'),
        'organisation-initiatives-create': this.$gettext('New Initiative'),
        'organisation-initiatives-id-assessment': this.$gettext('Assessment'),
        'organisation-initiatives-id-toolkit': this.$gettext('Toolkit'),
        'organisation-initiatives-id-toolkit-scorecard': this.$gettext(
          'Toolkit'
        ),
        'organisation-portfolio-innovation': this.$gettext(
          'Innovation Portfolio'
        ),
        'organisation-portfolio-management': this.$gettext('Portfolio Manager'),
        'organisation-portfolio-management-new': this.$gettext(
          'Create a new portfolio'
        ),
        'organisation-portfolio-management-id': this.$gettext('Edit portfolio'),
        'organisation-portfolio-management-edit-id': this.$gettext(
          'Edit portfolio'
        ),
      }
      const match = pages[this.pureRoute]
      if (this.pureRoute && !match && !noSubPage[this.pureRoute]) {
        console.warn(
          `Potential missing subpage key for breadcrumb ${this.pureRoute}`
        )
      }
      return match
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
.Breadcrumb {
  width: auto;
  height: @actionBarHeight;
  color: @colorWhite;

  .Home {
    a {
      line-height: @actionBarHeight;
      text-decoration: none;
      color: @colorWhite;
      transition: @transitionFade;

      &:hover {
        opacity: 0.7;
      }
    }
  }

  .Sep {
    margin: 0 5px;
    padding: 0 10px;
    transform: translateY(1px);
  }

  .Page {
    font-size: @fontSizeBase;
    line-height: @actionBarHeight;
    font-weight: 100;
    white-space: nowrap;
  }
}
</style>
