<template>
  <div class="UserProjectsList">
    <empty-projects v-if="!hasProjects" />
    <extended-project-card
      v-for="project in limited"
      :id="project.id"
      :key="project.id"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import EmptyProjects from './EmptyProjects';
import ExtendedProjectCard from '../common/ExtendedProjectCard';

export default {
  components: {
    EmptyProjects,
    ExtendedProjectCard
  },
  props: {
    limit: {
      type: Number,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      userProjecList: 'projects/getUserProjectList'
    }),
    limited () {
      return this.limit && this.userProjecList.length > 3 ? this.userProjecList.slice(0, this.limit) : this.userProjecList;
    },
    hasProjects () {
      return this.userProjecList.length > 0;
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .UserProjectsList {
    padding: 40px 40px 20px;
    background: url('~assets/img/squares.svg') no-repeat;
    background-position: center 0px;
  }
</style>
