<template>
  <el-form label-width="120px" label-position="top" class="ImportFile">
    <div class="Info">
      <p>
        <fa icon="info-circle" />
        <translate>
          The Import Interface allows you to import your Projects from an Excel
          file into the Digital Health Atlas.
        </translate>
      </p>
      <p>
        <translate> When importing your initiatives </translate>
        <xlsx-workbook>
          <xlsx-sheet
            v-for="sheet in templateSheets"
            :key="sheet.name"
            :collection="sheet.data"
            :sheet-name="sheet.name"
          />
          <xlsx-download filename="TIIP_Import_template.xlsx">
            <a class="XLSXTemplate">
              <translate>
                you can use this file as a reference for the format of the data
              </translate>
              <fa icon="file-excel" />
            </a>
          </xlsx-download>
        </xlsx-workbook>
      </p>
      <p>
        <translate>
          Note that your data should be organized to have data from only one
          office included in a spreadsheet.
        </translate>
      </p>
      <p>
        <translate>
          In addition, you can also only select one Investor for all of the data
          from within your spreadsheet.
        </translate>
      </p>
      <p>
        <translate>
          If you have more than one investor, we recommend that you go back to
          your initiatives once uploaded and add the correct investors.
        </translate>
      </p>
      <p>
        <translate>
          Note that for now the imported project are loaded in draft and need to
          be manually published
        </translate>
      </p>
    </div>
    <el-form-item>
      <template #label>
        <translate> Select File </translate>
      </template>
      <input type="file" @change="onChange" />
    </el-form-item>
    <el-form-item>
      <template #label>
        <translate> Select Sheet </translate>
      </template>
      <xlsx-read
        :file="inputFile"
        :options="{ type: 'binary', cellDates: true }"
      >
        <template #default="{ loading }">
          <xlsx-sheets>
            <template #default="{ sheets }">
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
            :options="{ defval: '' }"
            @parsed="parsed = $event"
          />
        </template>
      </xlsx-read>
    </el-form-item>
    <el-form-item>
      <template #label>
        <form-hint>
          <translate> Select Unicef Office </translate>
          <template #hint>
            <translate
              >Data can only be added one office at a time. If your data is from
              more than one office, you can make a separate sheet for each
              one.</translate
            >
          </template>
        </form-hint>
      </template>
      <country-office-select v-model="country_office" />
    </el-form-item>
    <el-form-item v-if="false" class="DraftOrPublished">
      <template #label>
        <translate> Draft or Publish </translate>
      </template>
      <el-radio-group v-model="isDraftOrPublish">
        <el-radio label="draft">
          <translate> Draft </translate>
        </el-radio>
        <el-radio label="publish">
          <translate> Publish </translate>
        </el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item class="ConfirmSettings">
      <el-button @click="save">
        <translate> Import </translate>
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import CountryOfficeSelect from '@/components/common/CountryOfficeSelect'
import FormHint from '@/components/common/FormHint'
import {
  XlsxRead,
  XlsxSheets,
  XlsxJson,
  XlsxWorkbook,
  XlsxSheet,
  XlsxDownload,
} from 'vue-xlsx'
import {
  importTemplate,
  nameMapping,
  nameInventMapping,
  apiNameInvenMapping,
} from '@/utilities/import'
import { draftRules } from '@/utilities/projects'
import get from 'lodash/get'
import reduce from 'lodash/reduce'

export default {
  components: {
    CountryOfficeSelect,
    XlsxRead,
    XlsxSheets,
    XlsxJson,
    FormHint,
    XlsxWorkbook,
    XlsxSheet,
    XlsxDownload,
  },
  data() {
    return {
      country_office: null,
      donor: 20,
      isDraftOrPublish: 'draft',
      inputFile: null,
      selectedSheet: null,
      parsed: null,
    }
  },
  computed: {
    ...mapState('system', {
      systemDicts: (state) => state,
    }),
    ...mapState('projects', {
      projectDicts: (state) => state.projectStructure,
    }),
    ...mapState({
      offices: (state) => state.offices.offices,
    }),
    ...mapGetters({
      getUnicefDonor: 'system/getUnicefDonor',
    }),
    finalImportTemplate() {
      const unicefCustomQuestions =
        get(
          this,
          `systemDicts.donorsLibrary.${this.getUnicefDonor.id}.donor_questions`
        ) || []
      const keyMapping = {
        unicef_sector: 'sectors',
        phase: 'phases',
      }
      const inventFields = reduce(
        apiNameInvenMapping,
        (res, val, key) => {
          res[nameInventMapping[key]] = this.projectDicts[
            keyMapping[key] || key
          ][0].name
          return res
        },
        {}
      )
      return importTemplate.map((i) => {
        const row = {
          ...i,
          ...inventFields,
        }
        unicefCustomQuestions.forEach((q) => {
          row[q.question] = q.options.join('|')
        })
        return row
      })
    },
    fieldsData() {
      const flatHFA = this.projectDicts.health_focus_areas.reduce((a, c) => {
        const innerNames = c.health_focus_areas.map((i) => i.name)
        return a.concat(innerNames)
      }, [])
      const flatHSC = this.projectDicts.hsc_challenges.reduce((a, c) => {
        const innerNames = c.challenges.map((i) => i.challenge)
        return a.concat(innerNames)
      }, [])
      const flatPlatforms = this.projectDicts.technology_platforms.map(
        (p) => p.name
      )
      const flathDHI = this.projectDicts.strategies.reduce((a, c) => {
        const innerValue = c.subGroups.reduce((innerA, innerC) => {
          return innerA.concat(innerC.strategies.map((s) => s.name))
        }, [])
        return a.concat(innerValue)
      }, [])
      const flatGoalAreas = this.projectDicts.goal_areas.map((p) => p.name)
      const flatFieldOffices = this.projectDicts.field_offices.map(
        (p) => p.name
      )
      const flatResultAreas = this.projectDicts.result_areas.map((p) => p.name)
      const flatCapabilityLevels = this.projectDicts.capability_levels.map(
        (p) => p.name
      )
      const flatCapabilityCategories = this.projectDicts.capability_categories.map(
        (p) => p.name
      )
      const flatCapabilitySubcategories = this.projectDicts.capability_subcategories.map(
        (p) => p.name
      )
      // INVENT
      const flatCurrency = this.projectDicts.currencies.map((p) => p.name)
      const flatPhases = this.projectDicts.phases.map((p) => p.name)
      const flatFunctions = this.projectDicts.functions.map((p) => p.name)
      const flatHardware = this.projectDicts.hardware.map((p) => p.name)
      const flatNontech = this.projectDicts.nontech.map((p) => p.name)
      const flatRegionalPriorities = this.projectDicts.regional_priorities.map(
        (p) => p.name
      )
      const flatInnovationCategories = this.projectDicts.innovation_categories.map(
        (p) => p.name
      )
      const flatCpd = this.projectDicts.cpd.map((p) => p.name)
      // const flatPhases = this.projectDicts.phases.map(p => p.name);

      return [
        [nameMapping.phase, ...flatPhases],
        [nameMapping.currency, ...flatCurrency],
        [nameMapping.functions, ...flatFunctions],
        [nameMapping.hardware, ...flatHardware],
        [nameMapping.nontech, ...flatNontech],
        [nameMapping.regional_priorities, ...flatRegionalPriorities],
        [nameMapping.innovation_categories, ...flatInnovationCategories],
        [nameMapping.cpd, ...flatCpd],
        // [nameMapping.phases, ...flatPhases],
        [nameMapping.health_focus_areas, ...flatHFA],
        [nameMapping.hsc_challenges, ...flatHSC],
        [nameMapping.platforms, ...flatPlatforms],
        [nameMapping.dhis, ...flathDHI],
        [nameMapping.field_office, ...flatFieldOffices],
        [nameMapping.goal_area, ...flatGoalAreas],
        [nameMapping.result_area, ...flatResultAreas],
        [nameMapping.capability_levels, ...flatCapabilityLevels],
        [nameMapping.capability_categories, ...flatCapabilityCategories],
        [nameMapping.capability_subcategories, ...flatCapabilitySubcategories],
      ]
    },
    draftRequiredFields() {
      const rules = draftRules()
      const requireds = []
      for (const rule in rules) {
        if (rules[rule].required) {
          requireds.push([nameMapping[rule]])
        }
      }
      return requireds
    },
    templateSheets() {
      return [
        { name: 'Import Example', data: this.finalImportTemplate },
        { name: 'Fields', data: this.fieldsData },
        { name: 'Draft required fields', data: this.draftRequiredFields },
      ]
    },
  },
  methods: {
    ...mapActions({
      addDataToQueue: 'admin/import/addDataToQueue',
    }),
    onChange(event) {
      this.inputFile = event.target.files ? event.target.files[0] : null
    },
    async save() {
      this.$nuxt.$loading.start('importXLSX')
      const importData = {
        filename: this.inputFile.name,
        country_office: this.country_office,
        country: this.offices.find((obj) => obj.id === this.country_office)
          .country,
        donor: this.donor,
        sheet_name: this.selectedSheet,
        header_mapping: Object.keys(this.parsed[0]).map((title) => ({
          selected: null,
          title,
        })),
        draft: this.isDraftOrPublish === 'draft',
        rows: [
          {
            data: this.parsed,
          },
        ],
      }
      try {
        const importItem = await this.addDataToQueue(importData)
        this.$nuxt.$loading.finish('importXLSX')
        this.$router.push(
          this.localePath({
            name: 'organisation-admin-import-id',
            params: { ...this.$route.params, id: importItem.id },
            query: undefined,
          })
        )
      } catch {
        this.$nuxt.$loading.finish('importXLSX')
        await this.$alert(
          this.$gettext(
            'Note that all import files need to have a unique name. Please re-name the file and upload it again.'
          ),
          this.$gettext('Error'),
          {
            confirmButtonText: 'OK',
            type: 'warning',
          }
        )
      }
    },
  },
}
</script>

<style lang="less">
.ImportFile {
  .SheetSelector,
  .DonorSelector,
  .CountrySelector {
    width: 100%;
  }

  .XLSXTemplate {
    color: blue;
    text-decoration: underline;
  }
}
</style>
