import { mapActions } from 'vuex'

const handleProjectUnpublish = {
  methods: {
    ...mapActions({
      unpublishProject: 'project/unpublishProject',
      latestProject: 'project/latestProject',
      setLoading: 'project/setLoading',
    }),
    async handleClickUnPublish(destination, id) {
      try {
        await this.$confirm(
          this.$gettext('The current project will be unpublish'),
          this.$gettext('Attention'),
          {
            confirmButtonText: this.$gettext('Ok'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning',
          }
        )
        await this.unpublishProject(id)
        const localised = this.localePath(destination)
        this.$router.push(localised)
        this.$message({
          type: 'success',
          message: this.$gettext('The project has been unpublish'),
        })
      } catch (e) {
        this.setLoading(false)
        this.$message({
          type: 'info',
          message: this.$gettext('Action cancelled'),
        })
      }
    },
    async handleClickLatest(id) {
      try {
        await this.latestProject(id)
        this.$message({
          type: 'success',
          message: this.$gettext('The project has been updated to latest'),
        })
      } catch (e) {
        this.setLoading(false)
        this.$message({
          type: 'info',
          message: this.$gettext('Action cancelled'),
        })
      }
    },
  },
}

export default handleProjectUnpublish
