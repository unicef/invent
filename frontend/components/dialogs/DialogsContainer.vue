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
import DigitalHealthInterventionsDialog from './DigitalHealthInterventionsDialog';
import DashboardFiltersDialog from './DashboardFiltersDialog';
import SaveFilterDialog from './SaveFilterDialog';
import SendEmailDialog from './SendEmailDialog';
import ProjectApprovalDialog from './ProjectApprovalDialog';
import EditSubLevelDialog from './EditSubLevelDialog';
import { mapGettersActions } from '../..//utilities/form';

export default {
  components: {
    DigitalHealthInterventionsDialog,
    DashboardFiltersDialog,
    SaveFilterDialog,
    SendEmailDialog,
    ProjectApprovalDialog,
    EditSubLevelDialog
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
                this.$router.replace(this.localePath({ name: 'organisation-edit-profile', params: { organisation: '-' }, query: undefined }));
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
