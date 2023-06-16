<template>
  <div class="Project">
    <project-bar v-if="profile" />
    <nuxt-child v-if="allowed" />
    <div v-if="!allowed" class="empty-screen"></div>
  </div>
</template>

<script>
import ProjectBar from '@/components/common/ProjectBar'
import { mapGetters } from 'vuex'

export default {
  components: {
    ProjectBar,
  },
  computed: {
    ...mapGetters({
      getProjectDetails: 'projects/getUserProjectDetails',
      profile: 'user/getProfile',
      project: 'project/getProjectData',
      published: 'project/getPublished',
    }),
    currentProject() {
      return this.getProjectDetails(this.$route.params.id)
    },
    allowed() {
      const allowed =
        this.profile.is_superuser ||
        this.profile.member.includes(parseInt(this.$route.params.id, 10)) ||
        this.profile.manager_of.includes(this.project.country_office) ||
        this.$route.name.split('__')[0] === 'organisation-initiatives-id-published' ||
        this.$route.name.split('__')[0] === 'organisation-initiatives-id-published-stages'
      return allowed
    },
  },
  watch: {
    currentProject: {
      immediate: true,
      handler() {
        if (!this.allowed) {
          this.$alert(this.$gettext('You are not authorized to access this view'), this.$gettext('Warning'), {
            confirmButtonText: 'OK',
            callback: () => {
              const path = this.localePath({
                name: 'organisation-initiatives-id-published',
                params: this.$route.params,
              })
              this.$router.replace(path)
            },
          })
        }
      },
    },
  },
}
</script>

<style>
.empty-screen {
  height: 100%;
  width: 100%;
}
</style>
