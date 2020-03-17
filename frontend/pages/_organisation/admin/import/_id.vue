<template>
  <div>
    <import-dialog
      ref="dialog"
      :custom-fields-lib="customFieldsLib"
      :imported="rows"
      :sub-levels="subLevels"
      :country="rawImport.country"
      @update="updateValue"
    />
    <el-card class="box-card">
      <import-details :item="rawImport" />
      <import-validation
        :headers="rawImport.header_mapping"
        :publish="!rawImport.draft"
      >
        <template
          v-slot:default="{globalErrors, rules, nameMapping}"
        >
          <div class="SavedSwitch">
            <el-switch
              v-model="showSaved"
              active-text="Show saved projects"
              inactive-text="Hide saved projects"
            />
          </div>
          <div class="ExportDataTable">
            <div class="Container">
              <import-headers
                :id="rawImport.id"
                :headers.sync="rawImport.header_mapping"
                :custom-fields-lib="customFieldsLib"
                :name-mapping="nameMapping"
              >
                <el-button
                  type="primary"
                  size="small"
                  @click="saveAll"
                >
                  <translate>
                    Save All
                  </translate>
                </el-button>
              </import-headers>
              <div class="Rows">
                <template v-if="showSaved">
                  <import-row
                    v-for="(row) in saved"
                    :key="row.id"
                    :row="row"
                    class="Row"
                  >
                    <template v-slot:default="{data}">
                      <div
                        class="Column Thin"
                      >
                        <el-button-group>
                          <a
                            v-if="row.project"
                            :href="localePath({name: 'organisation-projects-id-edit', params: {id: row.project, organisation: $route.params.organisation}})"
                            target="_blank"
                            class="el-button el-button--info el-button--mini"
                          >
                            <fa icon="share-square" />
                          </a>
                        </el-button-group>
                      </div>
                      <template
                        v-for="header in rawImport.header_mapping"
                      >
                        <SmartCell
                          :key="row.id + header.title"
                          :value="data[header.title]"
                          :type="header.selected"
                          :rules="rules[header.selected]"
                          class="Column"
                          :sub-levels="subLevels"
                          :custom-fields-lib="customFieldsLib"
                          :name-mapping="nameMapping"
                          disabled
                        />
                      </template>
                    </template>
                  </import-row>
                </template>
                <import-row
                  v-for="(row, index) in rows"
                  :key="row.id"
                  ref="row"
                  :row="row"
                  :custom-fields-lib="customFieldsLib"
                  class="Row"
                >
                  <template v-slot:default="{errors, valid, handleValidation, data, original, rowSave, scrollToError}">
                    <div
                      class="Column Thin"
                    >
                      <div class="ButtonList">
                        <el-button
                          :type="globalErrors.length > 0 || !valid ? 'warning' : 'success'"
                          size="mini"
                          class="SaveButton"
                          @click="singleRowSave(rowSave, valid, scrollToError)"
                        >
                          <fa icon="save" />
                        </el-button>
                        <el-button
                          size="mini"
                          class="DeleteButton"
                          type="danger"
                          @click="deleteRow(row, index)"
                        >
                          <fa icon="times" />
                        </el-button>
                      </div>
                    </div>
                    <template
                      v-for="header in rawImport.header_mapping"
                    >
                      <SmartCell
                        :key="row.id + header.title"
                        :value="data[header.title]"
                        :original="original[header.title]"
                        :type="header.selected"
                        :rules="rules[header.selected]"
                        class="Column"
                        :errors="errors"
                        :handle-validation="handleValidation"
                        :sub-levels="subLevels"
                        :custom-fields-lib="customFieldsLib"
                        :name-mapping="nameMapping"
                        @change="updateValue({row: index, key:header.title, value:$event})"
                        @openDialog="$refs.dialog.openDialog(index, header.title, $event)"
                      />
                    </template>
                    <div class="Column" />
                  </template>
                </import-row>
              </div>
            </div>
          </div>
        </template>
      </import-validation>
    </el-card>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';
import { mapGetters, mapActions } from 'vuex';
import ImportHeaders from '@/components/admin/import/ImportHeaders';
import ImportValidation from '@/components/admin/import/ImportValidation';
import ImportRow from '@/components/admin/import/ImportRow';
import SmartCell from '@/components/admin/import/SmartCell';
import ImportDialog from '@/components/admin/import/ImportDialog';
import ImportDetails from '@/components/admin/import/ImportDetails';

export default {
  name: 'ImportDetail',
  components: {
    ImportValidation,
    ImportHeaders,
    ImportRow,
    SmartCell,
    ImportDialog,
    ImportDetails
  },
  data () {
    return {
      showSaved: false
    };
  },
  computed: {
    ...mapGetters({
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails'
    }),
    selectedCountry () {
      if (this.rawImport) {
        return this.getCountryDetails(this.rawImport.country);
      }
      return {};
    },
    selectedDonor () {
      if (this.rawImport) {
        return this.getDonorDetails(this.rawImport.donor);
      }
      return {};
    },
    countryFieldsLib () {
      if (this.selectedCountry) {
        return this.selectedCountry.country_questions.reduce((a, c) => {
          a[`MOH Q.: ${c.question}`] = c;
          return a;
        }, {});
      }
      return {};
    },
    donorFieldsLib () {
      if (this.selectedDonor) {
        return this.selectedDonor.donor_questions.reduce((a, c) => {
          a[`INV Q.: ${c.question}`] = c;
          return a;
        }, {});
      }
      return {};
    },
    customFieldsLib () {
      return { ...this.donorFieldsLib, ...this.countryFieldsLib };
    },
    subLevels () {
      const nationalLevel = { id: 'National Level', name: 'National Level' };
      if (this.selectedCountry) {
        return [nationalLevel, ...this.selectedCountry.districts];
      }
      return [nationalLevel];
    },
    saved () {
      return this.rawImport.rows.filter(r => r.project);
    },
    rows () {
      return this.rawImport.rows.filter(r => !r.project);
    }
  },
  async asyncData ({ params, app: { $axios }, store }) {
    const { data } = await $axios.get(`/api/projects/import/${params.id}/`);
    await store.dispatch('countries/loadCountryDetails', data.country);
    await store.dispatch('system/loadDonorDetails', data.donor);
    return {
      rawImport: data
    };
  },
  async fetch ({ store }) {
    await Promise.all([
      store.dispatch('system/loadUserProfiles'),
      store.dispatch('system/loadDonors'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('system/loadStaticData'),
      store.dispatch('system/loadOrganisations'),
      store.dispatch('countries/loadMapData')
    ]);
  },
  methods: {
    ...mapActions({
      refreshProfile: 'user/refreshProfile'
    }),
    updateValue ({ row, key, value }) {
      const originalRow = this.rows[row];
      this.$set(originalRow.data, key, value);
      this.saveUpdatedValue(originalRow);
    },
    saveUpdatedValue: debounce(function (row) {
      this.patchRow(row);
    }, 1000),
    async patchRow (row) {
      return this.$axios.patch(`/api/projects/import-row/${row.id}/`, { ...row, id: undefined });
    },
    async deleteRow (row, index) {
      try {
        await this.$confirm(
          this.$gettext('Note that once this column is deleted, you cannot recover the data.'),
          this.$gettext('Row Delete'),
          {
            confirmButtonText: this.$gettext('OK'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning'
          });
        await this.$axios.delete(`/api/projects/import-row/${row.id}/`);
        this.rawImport.rows.splice(index, 1);
      } catch (e) {
        this.$message({
          type: 'info',
          message: this.$gettext('Delete canceled')
        });
      }
    },
    async singleRowSave (doSave, valid, scrollToError) {
      let newRow = null;
      if (valid) {
        try {
          await this.$confirm(
            this.$gettext('Note that once you have saved this project, it will be uploaded to the DHA. You can access all of your saved Projects from your My Projects page.'),
            this.$gettext('Save Project'),
            {
              confirmButtonText: this.$gettext('OK'),
              cancelButtonText: this.$gettext('Cancel'),
              type: 'warning'
            });
          this.$nuxt.$loading.start('save');
          newRow = await this.doSingleRowSave(doSave, true);
          await this.refreshProfile();
          this.$nuxt.$loading.finish('save');
        } catch (e) {
          this.$nuxt.$loading.finish('save');
          this.$message({
            type: 'info',
            message: this.$gettext('Saving Cancelled')
          });
          return;
        }
        try {
          await this.$confirm(
            this.$gettext('Your project has been successfully saved as a draft, you can go to your project page or keep working on the import interface'),
            this.$gettext('Success!'),
            {
              confirmButtonText: this.$gettext('Project page'),
              cancelButtonText: this.$gettext('Keep working'),
              type: 'info'
            });
          const id = newRow.project;
          this.$router.push(this.localePath({ name: 'organisation-projects-id-edit', params: { id, organisation: this.$route.params.organisation } }));
        } catch (e) {
          console.log('stay');
        }
      } else {
        scrollToError();
      }
    },
    async doSingleRowSave (doSave, nested) {
      try {
        const { country, country_office, donor, draft } = this.rawImport
        const newRow = await doSave(country, donor, !draft, country_office);
        await this.patchRow(newRow);
        return newRow;
      } catch (e) {
        console.error(e);
        if (e.response && e.response.data) {
          this.$alert(JSON.stringify(e.response.data), 'Error', {
            confirmButtonText: 'OK'
          });
        }
        if (nested) {
          throw e;
        }
      }
    },
    async saveAll () {
      try {
        await this.$confirm(
          this.$gettext('Note that once you have saved these projects, they will be uploaded to the DHA. You can access all saved projects from your My Projects page.'),
          this.$gettext('Save all projects'),
          {
            confirmButtonText: this.$gettext('OK'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning'
          });
        this.doSaveAll();
      } catch (e) {
        this.$message({
          type: 'info',
          message: this.$gettext('Saving all projects has been cancelled')
        });
      }
    },
    async doSaveAll () {
      this.$nuxt.$loading.start('saveAll');
      const toSave = this.$refs.row.filter(r => r.valid && r.row && !r.row.project);
      try {
        for (const p of toSave) {
          await this.doSingleRowSave(p.save, true);
        }
        await this.refreshProfile();
      } catch (e) {
        console.log(e);
      }
      this.$nuxt.$loading.finish('saveAll');
      try {
        await this.$confirm(
          this.$gettext('Your projects have been successfully saved as a draft, you can go to your project inbox or keep working on the import interface'),
          this.$gettext('Success!'),
          {
            confirmButtonText: this.$gettext('Project inbox'),
            cancelButtonText: this.$gettext('Keep working'),
            type: 'info'
          });
        this.$router.push(this.localePath({ name: 'organisation-projects', params: this.$route.params }));
      } catch (e) {
        console.log('stay');
      }
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.AdminImportPage {
  min-width: @appWidthMinLimit;
  min-height: calc(100vh - @topBarHeightSubpage - @actionBarHeight - @appFooterHeight);
  padding: 40px 40px;
  box-sizing: border-box;
  overflow: auto;

  // Fake data table

  .GlobalErrors {
    padding: 40px 0 20px;

    .el-tag {
      margin-right: 10px;

      .svg-inline--fa {
        margin-right: 3px;
      }
    }
  }

  .SavedSwitch {
    margin: 12px 0;
  }

  .ExportDataTable {
    width: 100%;
    margin: 0;
    background-color: #F5F5F5;
    font-size: @fontSizeSmall;
    line-height: 16px;
    box-shadow: inset 0 0 5px 1px rgba(0,0,0,.12);

    .Container {
      overflow: auto;
      position: relative;
      display: flex;
      flex-flow: column wrap;

      .Rows {
        height: 50vh;
        flex-shrink: 0;

        .Row {
          flex: 1 100%;
          display: flex;
          flex-direction: row;

          &:last-child {
              border-right: 0;

            .Column {
              border-bottom: 0;
            }
          }
        }
      }

      .Row {
        flex: 1 100%;
        display: flex;
        flex-direction: row;
      }

      .Column {
        box-sizing: border-box;
        flex: 0 0 200px;
        max-height: 200px;
        padding: 10px;
        border: solid @colorGrayLight;
        border-width: 0 1px 1px 0;
        overflow-y: auto;

        &:first-child {
          border-width: 0 1px 1px 1px;
        }

        &.Thin {
          flex: 0 0 100px;
        }

        &.Fluid {
          flex: 1;
        }

        &.Error {
          background-color: @colorDanger;
          color: @colorWhite;
          font-weight: 700;
        }

        .Title {
          margin-bottom: 10px;
          font-weight: 700;
        }
      }
      .ButtonList {
        display: inline-flex;
        width: 100%;

        .SaveButton, .DeleteButton {
          margin-left: 0px;
          color: white;
        }
      }
    }
  }
}

</style>
