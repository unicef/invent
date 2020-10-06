<template>
  <el-dialog
    v-if="visible"
    :visible.sync="visible"
    :title="$gettext('Initiative Approval') | translate"
    :modal="mini"
    :top="top"
    :width="width"
    custom-class="ProjectApprovalDialog"
    @open="loadCurrent"
  >
    <el-tabs
      v-model="activeTab"
    >
      <el-tab-pane
        :label="$gettext('Update') | translate"
        name="form"
      >
        <el-form
          ref="approvalForm"
          :model="form"
          :rules="rules"
          label-position="left"
          label-width="160px"
          @submit.native.prevent
        >
          <el-form-item
            :label="$gettext('Approved') | translate"
            prop="approved"
          >
            <el-select
              v-model="form.approved"
              placeholder="Select"
            >
              <el-option
                :value="true"
                label="Yes"
              />
              <el-option
                :value="false"
                label="No"
              />
              <el-option
                :value="null"
                label="Pending"
              />
            </el-select>
          </el-form-item>
          <el-form-item
            :label="$gettext('Reason') "
            prop="reason"
          >
            <el-input
              v-model="form.reason"
              :rows="3"
              type="textarea"
            />
          </el-form-item>

          <el-form-item
            :label="$gettext('User') | translate"
          >
            <user-item
              :id="approvedBy"
              show-organisation
            />
            <span class="Hint">
              <translate>Administrator that approved the project </translate>
            </span>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane
        :label="$gettext('History') | translate"
        name="history"
      >
        <el-table
          :data="history"
          border
          style="width: 100%"
        >
          <el-table-column
            :label="$gettext('Date/Time') | translate"
            :formatter="dateFormat"
            prop="modified"
          />
          <el-table-column
            :label="$gettext('User') | translate"
            prop="history_user__userprofile"
          >
            <template slot-scope="scope">
              <user-item
                :id="scope.row.history_user__userprofile"
                show-organisation
              />
            </template>
          </el-table-column>
          <el-table-column
            :label="$gettext('Reason') | translate"
            prop="reason"
          />
          <el-table-column
            :label="$gettext('Approved') | translate"
            align="center"
            width="150px"
            prop="approved"
          >
            <template slot-scope="scope">
              <approval-tag :value="scope.row.approved" />
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <span slot="footer">
      <el-row
        type="flex"
        align="center"
      >
        <el-col class="SecondaryButtons">
          <el-button
            type="text"
            class="CancelButton"
            @click="cancel"
          >
            <translate>Cancel</translate>
          </el-button>
          <el-button
            v-show="!mini"
            type="text"
            @click="goToProject"
          >
            <translate>See Initiative</translate>
          </el-button>
          <el-button
            v-show="mini"
            type="text"
            @click="goToCountryAdmin"
          >
            <translate>Back to admin</translate>
          </el-button>
        </el-col>
        <el-col class="PrimaryButtons">
          <el-button
            v-show="activeTab === 'form'"
            type="primary"
            @click="apply"
          >
            <translate>Save</translate>
          </el-button>
        </el-col>
      </el-row>
    </span>
  </el-dialog>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { format } from "date-fns";

import ApprovalTag from "../admin/ApprovalTag";
import UserItem from "../common/UserItem";

export default {
  components: {
    ApprovalTag,
    UserItem,
  },
  data() {
    return {
      mini: false,
      form: {
        approved: null,
        reason: null,
      },
      activeTab: "form",
      rules: {
        reason: [
          {
            required: true,
            message: this.$gettext("This is required"),
            trigger: "blur",
          },
        ],
      },
    };
  },
  computed: {
    ...mapGetters({
      currentProject: "admin/approval/getCurrentElement",
      currentElementDetails: "admin/approval/getCurrentElementDetails",
    }),
    visible: {
      get() {
        return this.currentProject !== null;
      },
      set() {
        this.setCurrentElement(null);
      },
    },
    top() {
      return this.mini ? "12px" : "10vh";
    },
    width() {
      return this.mini ? "60vw" : "80vw";
    },
    history() {
      if (this.currentElementDetails) {
        return this.currentElementDetails.history;
      }
      return [];
    },
    approvedBy() {
      if (this.currentElementDetails) {
        return this.history &&
          this.history[0] &&
          this.history[0].history_user__userprofile
          ? this.history[0].history_user__userprofile
          : this.currentElementDetails.legacy_approved_by;
      }
      return null;
    },
  },
  methods: {
    ...mapActions({
      setCurrentElement: "admin/approval/setCurrentElement",
      updateProjectApproval: "admin/approval/updateProjectApproval",
    }),
    loadCurrent() {
      this.form = {
        approved: this.currentElementDetails
          ? this.currentElementDetails.approved
          : null,
        reason: this.currentElementDetails
          ? this.currentElementDetails.reason
          : "",
      };
    },
    dateFormat(row, column, value) {
      return format(value, "YYYY-MM-DD HH:mm");
    },
    cancel() {
      this.visible = null;
      if (this.mini) {
        this.goToCountryAdmin();
      }
    },
    goToProject() {
      this.mini = true;
      const id = this.currentElementDetails.project;
      const path = this.localePath({
        name: "organisation-initiatives-id-published",
        params: { ...this.$route.params, id },
      });
      this.$router.push(path);
    },
    goToCountryAdmin() {
      this.mini = false;
      const path = this.localePath({
        name: "organisation-admin-country",
        params: this.$route.params,
      });
      this.$router.push(path);
    },
    apply() {
      this.$refs.approvalForm.validate(async (valid) => {
        if (valid) {
          try {
            await this.updateProjectApproval(this.form);
            this.visible = null;
            if (this.mini) {
              this.goToCountryAdmin();
            }
          } catch (e) {
            console.log(e);
            this.$alert(
              this.$gettext("An error occured while saving the data"),
              this.$gettext("Warning"),
              {
                confirmButtonText: this.$gettext("Ok"),
              }
            );
          }
        } else {
          this.$message.error(
            this.$gettext("Please fill all the required fields")
          );
        }
      });
    },
  },
};
</script>

<style lang="less">
@import "../../assets/style/variables.less";
@import "../../assets/style/mixins.less";

.ProjectApprovalDialog {
  .el-form,
  .el-form-item {
    margin: 20px 0;
  }
}
</style>
