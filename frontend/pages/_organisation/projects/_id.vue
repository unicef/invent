<template>
  <div class="Project">
    <project-bar v-if="profile" />
    <nuxt-child />
  </div>
</template>

<script>
import ProjectBar from '@/components/common/ProjectBar';
import { mapGetters } from 'vuex';

export default {
  components: {
    ProjectBar
  },
  computed: {
    ...mapGetters({
      getProjectDetails: 'projects/getUserProjectDetails',
      profile: 'user/getProfile'
    }),
    currentProject () {
      return this.getProjectDetails(+this.$route.params.id);
    },
    route () {
      return this.$route.name.split('__')[0];
    }
  },
  watch: {
    currentProject: {
      immediate: true,
      handler (project) {
        if ((!project.draft || !project.draft.name) && this.profile && !this.profile.is_superuser && this.route !== 'organisation-projects-id-published') {
          this.$alert(this.$gettext('You are not authorized to access this view'), this.$gettext('Warning'), {
            confirmButtonText: 'OK',
            callback: () => {
              const path = this.localePath({ name: 'organisation-projects-id-published', params: this.$route.params });
              this.$router.replace(path);
            }
          });
        }
      }
    }
  }
};
</script>

<style>

</style>
