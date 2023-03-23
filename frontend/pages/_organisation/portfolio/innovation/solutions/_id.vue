<template>
  <div class="Project">
    <nuxt-child />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
    }),
  },
  watch: {
    currentProject: {
      immediate: true,
      handler() {
        const allowed =
          this.profile.is_superuser ||
          this.profile.global_portfolio_owner ||
          this.profile.manager.length > 0 ||
          this.$route.name.split('__')[0] === 'organisation-portfolio-innovation-solutions-id'
        // this.profile.member.includes(parseInt(this.$route.params.id, 10))
        if (!allowed) {
          this.$alert(this.$gettext('You are not authorized to access this view'), this.$gettext('Warning'), {
            confirmButtonText: 'OK',
            callback: () => {
              const path = this.localePath({
                name: 'organisation-portfolio-innovation-solutions-id',
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

<style></style>
