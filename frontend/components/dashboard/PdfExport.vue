<template>
  <div />
</template>

<script>
import { format } from 'date-fns'
import get from 'lodash/get'
import { mapGetters, mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
    }),
    ...mapGetters({
      projects: 'dashboard/getProjectsBucket',
      selectedRows: 'dashboard/getSelectedRows',
      selectAll: 'dashboard/getSelectAll',
      getCountryDetails: 'countries/getCountryDetails',
      getDonorDetails: 'system/getDonorDetails',
      getOrganisationDetails: 'system/getOrganisationDetails',
      getHealthFocusAreas: 'projects/getHealthFocusAreas',
      dashboardType: 'dashboard/getDashboardType',
      countryColumns: 'dashboard/getCountryColumns',
      donorColumns: 'dashboard/getDonorColumns',
      goalAreas: 'projects/getGoalAreas',
      resultAreas: 'projects/getResultAreas',
      capabilityLevels: 'projects/getCapabilityLevels',
      capabilityCategories: 'projects/getCapabilityCategories',
      capabilitySubcategories: 'projects/getCapabilitySubcategories',
      fieldOffices: 'projects/getFieldOffices',
      regions: 'system/getUnicefRegions',
      hscChallenges: 'projects/getHscChallenges',
    }),
    exportDate() {
      return format(Date.now(), 'Do MMM, YYYY')
    },
    tableHeader() {
      return {
        table: {
          widths: ['50%', '50%'],
          headerRows: 2,
          body: [
            [
              {
                text: this.$gettext('TIIP'),
                fillColor: '#1CABE2',
                color: '#FFFFFF',
                colSpan: 2,
                style: 'mainHeader',
                margin: [5, 0, 0, 0],
              },
              '',
            ],
            [
              {
                text: this.$gettext('All Countries'),
                fillColor: '#EEEEEE',
                color: '#000000',
                style: 'headerSecondRow',
                margin: [5, 0, 0, 0],
              },
              {
                text: this.$gettext('List exported on ') + this.exportDate,
                fillColor: '#EEEEEE',
                color: '#000000',
                style: 'headerSecondRowRight',
                margin: [0, 0, 5, 0],
              },
            ],
          ],
        },
        layout: 'noBorders',
        margin: [0, 10],
      }
    },
    docDefinition() {
      return {
        content: [],
        defaultStyle: {
          font: 'Roboto',
          fontSize: 10,
        },
        pageSize: 'A4',
        margin: [40, 40, 40, 40],
        pageOrientation: 'landscape',
        styles: {
          mainHeader: {
            bold: true,
            fontSize: 16,
          },
          headerSecondRow: {
            alignment: 'left',
            fontSize: 12,
            bold: true,
          },
          headerSecondRowRight: {
            alignment: 'right',
            fontSize: 12,
          },
          tableHeader: {
            bold: true,
            fontSize: 14,
          },
          subHeader: {
            bold: true,
            fontSize: 10,
            color: '#8A8A8A',
          },
        },
        images: this.base64Images,
      }
    },
    selected() {
      return this.selectAll
        ? this.projects
        : this.projects.filter((p) =>
            this.selectedRows.some((sr) => sr === p.id)
          )
    },
    parsed() {
      return this.selected.map((s) => {
        let custom = []
        if (this.dashboardType === 'donor') {
          try {
            custom = this.donorColumns.map((dc) => {
              const value =
                s.donor_answers && s.donor_answers[dc.donorId]
                  ? s.donor_answers[dc.donorId][dc.originalId]
                  : ''
              return {
                text: dc.label,
                value,
                donor: dc.donorId,
              }
            })
          } catch (e) {
            console.error('failed to print custom donor answers', e)
          }
        }
        if (this.dashboardType === 'country') {
          try {
            custom = this.countryColumns.map((cc) => {
              const value = s.country_answers
                ? s.country_answers[cc.originalId]
                : ''
              return {
                text: cc.label,
                value,
              }
            })
          } catch (e) {
            console.error('failed to print custom country answers', e)
          }
        }
        return {
          ...s,
          custom,
        }
      })
    },
  },
  methods: {
    printDate(dateString) {
      return format(dateString, 'Do MMM, YYYY')
    },
    printBoolean(value) {
      return value ? this.$gettext('Yes') : this.$gettext('No')
    },
    printCustomAnswer(value) {
      if (value && value[0] && value.length === 1) {
        return value[0]
      } else if (value && value.length > 0) {
        return value.join(', ')
      }
      return 'N/A'
    },
    printProjectLink(project) {
      if (window) {
        let path = '/404'
        if (project && project.id) {
          path = this.localePath({
            name: 'organisation-initiatives-id-published',
            params: { organisation: '-', id: project.id },
          })
        }
        return window.location.origin + path
      }
      return ''
    },
    parseFlatList(flatList, type) {
      try {
        const all = typeof this[type] === 'function' ? this[type]() : this[type]
        return all
          .filter((cb) => flatList.includes(cb.id))
          .map((cb) => cb.name)
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseHscChallenges(values) {
      try {
        return this.hscChallenges
          .reduce((a, c) => {
            c.challenges.forEach((cc) => {
              if (values.includes(cc.id)) {
                a.push(cc.challenge)
              }
            })
            return a
          }, [])
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    parseHealthFocusAreas(health_focus_areas) {
      try {
        return this.getHealthFocusAreas
          .filter((hfa) =>
            hfa.health_focus_areas.some((h) =>
              health_focus_areas.includes(h.id)
            )
          )
          .map((hf) => hf.name)
          .join(',')
      } catch (e) {
        console.warn(e)
        return ''
      }
    },
    capabilityData({
      capabilityLevels,
      capabilityCategories,
      capabilitySubcategories,
    }) {
      return [
        [
          { text: this.$gettext('Capability Levels:'), style: 'subHeader' },
          capabilityLevels,
        ],
        [
          { text: this.$gettext('Capability Categories:'), style: 'subHeader' },
          capabilityCategories,
        ],
        {
          stack: [
            {
              text: this.$gettext('Capability Subcategories:'),
              style: 'subHeader',
            },
            capabilitySubcategories,
          ],
          colSpan: 2,
        },
        '',
      ]
    },
    dhaFields({ health_focus_areas, hsc_challenges }) {
      return [
        {
          stack: [
            { text: this.$gettext('Health Focus Area:'), style: 'subHeader' },
            health_focus_areas,
          ],
          colSpan: 2,
        },
        '',
        {
          stack: [
            {
              text: this.$gettext('Health System Challenges'),
              style: 'subHeader',
            },
            hsc_challenges,
          ],
          colSpan: 2,
        },
        '',
      ]
    },
    printPdf() {
      this.base64Images = require('../../utilities/exportBase64Images.js')
      this.pdfMake = require('pdfmake/build/pdfmake.js')
      const pdfFonts = require('pdfmake/build/vfs_fonts.js')

      this.pdfMake.vfs = pdfFonts.pdfMake.vfs
      const docDefinition = {
        ...this.docDefinition,
        content: [this.tableHeader],
      }

      this.parsed.forEach((project, index) => {
        const country = this.getCountryDetails(project.country)
        const country_name =
          country && country.name ? country.name.toUpperCase() : ''
        const country_office_name =
          this.offices
            .find((obj) => obj.id === project.country_office)
            .name.toUpperCase() || ''
        const donors = project.donors
          .map((d) => this.getDonorDetails(d))
          .filter((d) => d)
          .map((d) => d.name)
        const health_focus_areas = this.parseHealthFocusAreas(
          project.health_focus_areas
        )
        const goalArea = get(
          this.goalAreas.find((g) => g.id === project.goal_area),
          'name',
          ''
        )
        const resultArea = get(
          this.resultAreas.find((g) => g.id === project.result_area),
          'name',
          ''
        )
        const region = get(
          this.regions.find((r) => r.id === project.region),
          'name',
          ''
        )
        const fieldOffice = get(
          this.fieldOffices.find((r) => r.id === project.field_office),
          'name',
          ''
        )
        const capabilityLevels = this.parseFlatList(
          project.capability_levels,
          'capabilityLevels'
        )
        const capabilityCategories = this.parseFlatList(
          project.capability_categories,
          'capabilityCategories'
        )
        const capabilitySubcategories = this.parseFlatList(
          project.capability_subcategories,
          'capabilitySubcategories'
        )
        const hsc_challenges = this.parseHscChallenges(project.hsc_challenges)

        docDefinition.content.push({
          margin: [0, 10],
          table: {
            widths: [118, 118, 118, 118, 118, 118],
            headerRows: 1,
            body: [
              [
                {
                  text: `${index + 1}. ${project.name || ''}`,
                  fillColor: '#EEEEEE',
                  style: 'tableHeader',
                  colSpan: 4,
                },
                '',
                '',
                '',
                {
                  text: this.$gettext('Go to project'),
                  decoration: 'underline',
                  link: this.printProjectLink(project),
                  color: '#008DC9',
                  style: 'subHeader',
                },
                `${country_office_name}, ${country_name}`,
              ],
              [
                [
                  { text: this.$gettext('Region:'), style: 'subHeader' },
                  region,
                ],
                [
                  { text: this.$gettext('Field office:'), style: 'subHeader' },
                  fieldOffice,
                ],

                {
                  stack: [
                    { text: this.$gettext('Investors:'), style: 'subHeader' },
                    donors.join(', '),
                  ],
                  colSpan: 3,
                },
                '',
                '',

                [
                  {
                    text: this.$gettext('Programme Focal Point Name:'),
                    style: 'subHeader',
                  },
                  `${project.contact_name || ''} - ${
                    project.contact_email || ''
                  }`,
                ],
              ],
              [
                {
                  stack: [
                    {
                      text: this.$gettext('Initiative Description:'),
                      style: 'subHeader',
                    },
                    { text: project.implementation_overview || '' },
                  ],
                  colSpan: 6,
                },
                '',
                '',
                '',
                '',
                '',
              ],
              [
                [
                  { text: this.$gettext('Goal Area:'), style: 'subHeader' },
                  goalArea,
                ],
                [
                  { text: this.$gettext('Result Area:'), style: 'subHeader' },
                  resultArea,
                ],
                ...(project.goal_area !== 1
                  ? this.capabilityData({
                      capabilityLevels,
                      capabilityCategories,
                      capabilitySubcategories,
                    })
                  : this.dhaFields({ health_focus_areas, hsc_challenges })),
              ],
              ...project.custom.map((c) => [
                {
                  stack: [
                    { text: c.text, style: 'subHeader' },
                    this.printCustomAnswer(c.value),
                  ],
                  colSpan: 6,
                },
                '',
                '',
                '',
                '',
                '',
              ]),
            ],
          },
        })
      })
      this.pdfMake
        .createPdf(docDefinition)
        .download('clv-searchable-export.pdf')
    },
  },
}
</script>
