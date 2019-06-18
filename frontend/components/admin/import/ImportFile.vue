<template>
  <el-form
    label-width="120px"
    label-position="top"
    class="ImportFile"
  >
    <div class="Info">
      <p>
        <fa icon="info-circle" />
        <translate>
          The Import Interface allows you to import your Projects from an Excel file into the Digital Health Atlas.
        </translate>
      </p>
      <p>
        <translate>
          When importing your projects
        </translate>
        <xlsx-workbook>
          <xlsx-sheet
            v-for="sheet in templateSheets"
            :key="sheet.name"
            :collection="sheet.data"
            :sheet-name="sheet.name"
          />
          <xlsx-download filename="DHA_Import_template.xlsx">
            <a class="XLSXTemplate">
              <translate> you can use this file as a reference for the format of the data </translate>
              <fa icon="file-excel" />
            </a>
          </xlsx-download>
        </xlsx-workbook>
      </p>
      <p>
        <translate>
          Note that your data should be organized to have data from only one country included in a spreadsheet.
        </translate>
      </p>
      <p>
        <translate>
          In addition, you can also only select one Investor for all of the data from within your spreadsheet.
        </translate>
      </p>
      <p>
        <translate>
          If you have more than one investor, we recommend that you go back to your projects once uploaded and add the correct investors.
        </translate>
      </p>
      <p>
        <translate>
          Note that for now the imported project are loaded in draft and need to be manually published
        </translate>
      </p>
    </div>
    <el-form-item>
      <template #label>
        <translate>
          Select File
        </translate>
      </template>
      <input
        type="file"
        @change="onChange"
      >
    </el-form-item>
    <el-form-item>
      <template #label>
        <translate>
          Select Sheet
        </translate>
      </template>
      <xlsx-read
        :file="inputFile"
        :options="{ type: 'binary', cellDates: true }"
      >
        <template #default="{loading}">
          <xlsx-sheets>
            <template #default="{sheets}">
              <div v-loading="loading">
                <el-select
                  v-model="selectedSheet"
                  class="SheetSelector"
                  :disabled="!sheets || sheets.length === 0"
                >
                  <el-option
                    v-for="sheet in sheets"
                    :key="sheet"
                    :value="sheet"
                  >
                    {{ sheet }}
                  </el-option>
                </el-select>
              </div>
            </template>
          </xlsx-sheets>
          <xlsx-json
            :sheet="selectedSheet"
            :options="{defval: ''}"
            @parsed="parsed = $event"
          />
        </template>
      </xlsx-read>
    </el-form-item>
    <el-form-item>
      <template #label>
        <form-hint>
          <translate>
            Select Country
          </translate>
          <template #hint>
            <translate>Data can only be added one country at a time. If your data is from more than one country, you can make a separate sheet for each country.</translate>
          </template>
        </form-hint>
      </template>
      <country-select
        v-model="country"
      />
    </el-form-item>
    <el-form-item>
      <template #label>
        <form-hint>
          <translate>
            Select Investor
          </translate>
          <template #hint>
            <translate>
              Data can only be uploaded for one investor at a time. You can update each project once they are saved in your My Projects page before publication.
            </translate>
          </template>
        </form-hint>
      </template>
      <donor-select
        v-model="donor"
      />
    </el-form-item>
    <el-form-item
      v-if="false"
      class="DraftOrPublished"
    >
      <template #label>
        <translate>
          Draft or Publish
        </translate>
      </template>
      <el-radio-group v-model="isDraftOrPublish">
        <el-radio label="draft">
          <translate>
            Draft
          </translate>
        </el-radio>
        <el-radio label="publish">
          <translate>
            Publish
          </translate>
        </el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item
      class="ConfirmSettings"
    >
      <el-button @click="save">
        <translate>
          Import
        </translate>
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import DonorSelect from '@/components/common/DonorSelect';
import CountrySelect from '@/components/common/CountrySelect';
import FormHint from '@/components/common/FormHint';
import { XlsxRead, XlsxSheets, XlsxJson, XlsxWorkbook, XlsxSheet, XlsxDownload } from 'vue-xlsx';
import { importTemplate, nameMapping } from '@/utilities/import';
import { draftRules } from '@/utilities/projects';

export default {
  components: {
    DonorSelect,
    CountrySelect,
    XlsxRead,
    XlsxSheets,
    XlsxJson,
    FormHint,
    XlsxWorkbook,
    XlsxSheet,
    XlsxDownload
  },
  data () {
    return {
      country: null,
      donor: null,
      isDraftOrPublish: 'draft',
      inputFile: null,
      selectedSheet: null,
      parsed: null
    };
  },
  computed: {
    ...mapState('system', {
      systemDicts: state => state
    }),
    ...mapState('projects', {
      projectDicts: state => state.projectStructure
    }),
    fieldsData () {
      const flatHFA = this.projectDicts.health_focus_areas.reduce((a, c) => {
        const innerNames = c.health_focus_areas.map(i => i.name);
        return a.concat(innerNames);
      }, []);
      const flatHSC = this.projectDicts.hsc_challenges.reduce((a, c) => {
        const innerNames = c.challenges.map(i => i.challenge);
        return a.concat(innerNames);
      }, []);
      const flatsHIS = this.projectDicts.his_bucket.reduce((a, c) => {
        a.push(c.name);
        return a;
      }, []);
      const flatLicenses = this.projectDicts.licenses.map(l => l.name);
      const flatPlatforms = this.projectDicts.technology_platforms.map(p => p.name);
      const flathDHI = this.projectDicts.strategies.reduce((a, c) => {
        const innerValue = c.subGroups.reduce((innerA, innerC) => {
          return innerA.concat(innerC.strategies.map(s => s.name));
        }, []);
        return a.concat(innerValue);
      }, []);
      const flatOrganisations = this.systemDicts.organisations.map(o => o.name);
      return [
        [nameMapping.health_focus_areas, ...flatHFA],
        [nameMapping.hsc_challenges, ...flatHSC],
        [nameMapping.his_bucket, ...flatsHIS],
        [nameMapping.licenses, ...flatLicenses],
        [nameMapping.platforms, ...flatPlatforms],
        [nameMapping.digitalHealthInterventions, ...flathDHI],
        [nameMapping.organisation, ...flatOrganisations]
      ];
    },
    draftRequiredFields () {
      const rules = draftRules();
      const requireds = [];
      for (const rule in rules) {
        if (rules[rule].required) {
          requireds.push([nameMapping[rule]]);
        }
      }
      return requireds;
    },
    templateSheets () {
      return [
        { name: 'Import Example', data: importTemplate },
        { name: 'Fields', data: this.fieldsData },
        { name: 'Draft required fields', data: this.draftRequiredFields }
      ];
    }
  },
  methods: {
    ...mapActions({
      addDataToQueue: 'admin/import/addDataToQueue'
    }),
    onChange (event) {
      this.inputFile = event.target.files ? event.target.files[0] : null;
    },
    async save () {
      this.$nuxt.$loading.start('importXLSX');
      const importData = {
        filename: this.inputFile.name,
        country: this.country,
        donor: this.donor,
        sheet_name: this.selectedSheet,
        header_mapping: Object.keys(this.parsed[0]).map(title => ({ selected: null, title })),
        'draft': this.isDraftOrPublish === 'draft',
        'rows': [
          {
            'data': this.parsed
          }
        ]
      };
      try {
        const importItem = await this.addDataToQueue(importData);
        this.$nuxt.$loading.finish('importXLSX');
        this.$router.push(this.localePath({ name: 'organisation-admin-import-id', params: { ...this.$route.params, id: importItem.id }, query: undefined }));
      } catch {
        this.$nuxt.$loading.finish('importXLSX');
        await this.$alert(
          this.$gettext('Note that all import files need to have a unique name. Please re-name the file and upload it again.'),
          this.$gettext('Error'),
          {
            confirmButtonText: 'OK',
            type: 'warning'
          });
      }
    }
  }
};
</script>

<style lang="less">
.ImportFile {
  .SheetSelector, .DonorSelector, .CountrySelector{
    width: 100%;
  }

  .XLSXTemplate{
    color: blue;
    text-decoration: underline;
  }

  .Info {

  }
}
</style>
