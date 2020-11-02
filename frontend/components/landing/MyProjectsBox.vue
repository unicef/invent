<template>
  <div class="MyProjectsBox">
    <el-row type="flex" align="middle" class="ProjectsBoxHeadline">
      <el-col>
        <h2><translate>My Initiatives</translate></h2>
        <h6>
          <translate>Here are your initiatives updated most recently</translate>
        </h6>
      </el-col>
    </el-row>

    <user-projects-list :limit="3" landing />

    <div v-if="projects.length > 0" class="initiative-link">
      <el-button type="primary" @click="handleLink">
        <translate>View all Initiatives</translate>
        <fa icon="angle-right" />
      </el-button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

import UserProjectsList from '@/components/common/UserProjectsList'
export default {
  components: {
    UserProjectsList,
  },
  computed: {
    ...mapState({
      projects: (state) => state.projects.userProjects,
    }),
  },
  async mounted() {
    await this.setTab(1)
  },
  methods: {
    ...mapActions({
      setTab: 'projects/setTab',
    }),
    handleLink() {
      this.$router.push(
        this.localePath({
          name: 'organisation-initiatives',
          params: this.$route.params,
        })
      )
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.MyProjectsBox {
  height: 100%;
  background-color: @colorWhite;

  .ProjectsBoxHeadline {
    position: relative;
    height: 172px;
    text-align: center;
    background-color: @colorBrandPrimary;

    &::after {
      content: '';
      z-index: 100;
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      display: block;
      width: 0;
      height: 0;
      border-left: 24px solid transparent;
      border-right: 24px solid transparent;
      border-top: 24px solid @colorBrandPrimary;
    }

    h2 {
      color: @colorWhite;
      margin: 0 0 16px;
    }

    h6 {
      color: @colorWhite;
      margin: 0;
    }
  }

  .initiative-link {
    margin-bottom: 30px;
    display: flex;
    justify-content: center;
    button {
      height: 48px;
      font-size: 16px;
      svg {
        margin-left: 8px;
      }
    }
  }
}
</style>
