<template>
  <div class="DialogsContainer">
    <digital-health-interventions-dialog />
    <dashboard-filters-dialog />
    <save-filter-dialog />
    <send-email-dialog />
    <project-approval-dialog />
  </div>
</template>

<script>
import DigitalHealthInterventionsDialog from './DigitalHealthInterventionsDialog';
import DashboardFiltersDialog from './DashboardFiltersDialog';
import SaveFilterDialog from './SaveFilterDialog';
import SendEmailDialog from './SendEmailDialog';
import ProjectApprovalDialog from './ProjectApprovalDialog';
import { mapGettersActions } from '../..//utilities/form';

export default {
  components: {
    DigitalHealthInterventionsDialog,
    DashboardFiltersDialog,
    SaveFilterDialog,
    SendEmailDialog,
    ProjectApprovalDialog
  },
  computed: {
    ...mapGettersActions({
      showEmptyProfileWarning: ['layout', 'getShowEmptyProfileWarning', 'setShowEmptyProfileWarning']
    })
  },
  watch: {
    showEmptyProfileWarning: {
      immediate: true,
      handler (show) {
        if (show) {
          this.$alert(
            this.$gettext('Please fill your profile first'),
            this.$gettext('Warning'),
            {
              confirmButtonText: 'OK',
              callback: action => {
                this.showEmptyProfileWarning = false;
                this.$router.replace(this.localePath({ name: 'organisation-edit-profile', params: this.$route.params, query: undefined }));
              }
            });
        }
      }
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .DialogsContainer {}
</style>
