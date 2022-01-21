<template>
  <div class="DialogsContainer">
    <DigitalHealthInterventionsDialog />
    <DashboardFiltersDialog />
    <SaveFilterDialog />
    <SendEmailDialog />
    <ProjectApprovalDialog />
    <EditSubLevelDialog />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { mapGettersActions } from '../..//utilities/form'
import DigitalHealthInterventionsDialog from './DigitalHealthInterventionsDialog'
import DashboardFiltersDialog from './DashboardFiltersDialog'
import SaveFilterDialog from './SaveFilterDialog'
import SendEmailDialog from './SendEmailDialog'
import ProjectApprovalDialog from './ProjectApprovalDialog'
import EditSubLevelDialog from './EditSubLevelDialog'

export default {
  components: {
    DigitalHealthInterventionsDialog,
    DashboardFiltersDialog,
    SaveFilterDialog,
    SendEmailDialog,
    ProjectApprovalDialog,
    EditSubLevelDialog,
  },
  computed: {
    ...mapGettersActions({
      showEmptyProfileWarning: ['layout', 'getShowEmptyProfileWarning', 'setShowEmptyProfileWarning'],
      showNoUnicefOrgOrDonor: ['layout', 'getShowNoUnicefOrgOrDonor', 'setShowNoUnicefOrgOrDonor'],
    }),
  },
  watch: {
    showEmptyProfileWarning: {
      immediate: true,
      handler(show) {
        if (show) {
          this.$alert(this.$gettext('Please fill your profile first'), this.$gettext('Warning'), {
            confirmButtonText: 'OK',
            callback: (action) => {
              this.showEmptyProfileWarning = false
              this.$router.replace(
                this.localePath({
                  name: 'organisation-edit-profile',
                  params: { organisation: '-' },
                  query: undefined,
                })
              )
            },
          })
        }
      },
    },
    showNoUnicefOrgOrDonor: {
      immediate: true,
      handler(show) {
        if (show) {
          this.$alert(
            this.$gettext('UNICEF donor or organisation record not found. Make sure these records exists.'),
            this.$gettext('Warning'),
            {
              confirmButtonText: 'OK',
              callback: () => {
                this.showNoUnicefOrgOrDonor = false
              },
            }
          )
        }
      },
    },
  },
  methods: {
    ...mapActions({
      logout: 'user/doLogout',
    }),
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.DialogsContainer {
}
</style>
