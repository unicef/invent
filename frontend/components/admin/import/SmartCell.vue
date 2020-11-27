<template>
  <div
    :class="[
      'SmartCell',
      {
        Disabled: isDisabled,
        ValidationError: errorMessage,
        ParsingError: parsingFailed,
      },
    ]"
    @click="clickHandler"
  >
    <div class="Content">
      <template v-if="column">
        <div v-if="active" class="active">
          <date-field
            v-if="isDate"
            v-model="internalValue"
            :disabled="disabled"
          />
          <el-input
            v-if="isTextArea"
            v-model="internalValue"
            :disabled="disabled"
            type="textarea"
            :rows="6"
          />
        </div>

        <template v-else-if="column === 'team'">
          <team-list :value="parsedValue.ids" />
        </template>
        <template v-else-if="isDate || isTextArea">
          {{ internalValue }}
        </template>
        <template v-else-if="isLinks">
          <div
            v-for="(parsed, i) in parsedValue.ids"
            :key="`${parsed.link_type}_${i}`"
          >
            <ul>
              <li>
                {{ getLinkHeader(parsed.link_type) }}
              </li>
              <li>{{ parsed.link_url }}</li>
            </ul>
            <div>-----------------------------</div>
          </div>
        </template>
        <template v-else-if="isPartner">
          <div v-for="parsed in parsedValue.ids" :key="parsed.partner_name">
            <ul>
              <li>
                <list-element
                  :value="parsed.partner_type * 1"
                  source="getPartnerTypes"
                  root="system"
                />
              </li>
              <li>{{ parsed.partner_name }}</li>
              <li>{{ parsed.partner_contact }}</li>
              <li>{{ parsed.partner_email }}</li>
              <li>{{ parsed.partner_website }}</li>
            </ul>
            <div>-----------------------------</div>
          </div>
        </template>

        <template v-else-if="parsedValue && parsedValue.names">
          <ul class="ParsedList">
            <li v-for="(name, index) in parsedValue.names" :key="index">
              {{ name }}
            </li>
          </ul>
        </template>
      </template>
      <template v-if="!column">
        {{ value }}
      </template>
      <template v-if="parsingFailed">
        <span class="OriginalValue">{{ original }}</span>
      </template>
    </div>
    <div v-if="errorMessage || parsingFailed" class="ErrorOverlay">
      <span v-if="errorMessage && !parsingFailed">
        {{ errorMessage }}
      </span>
      <span v-if="parsingFailed">
        <translate>
          Failed to parse your data, click to manually fix
        </translate>
      </span>
    </div>
  </div>
</template>

<script>
import TeamList from '@/components/project/TeamList'
import DateField from '@/components/admin/import/DateField'
import ListElement from '@/components/project/ListElement'
import { Validator } from 'vee-validate'
import { mapState } from 'vuex'
import chunk from 'lodash/chunk'
import find from 'lodash/find'
import compact from 'lodash/compact'
import pickBy from 'lodash/pickBy'

export default {
  components: {
    DateField,
    ListElement,
    TeamList,
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: null,
      default: null,
    },
    type: {
      type: String,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    rules: {
      type: Object,
      default: null,
    },
    errors: {
      type: Array,
      default: () => [],
    },
    handleValidation: {
      type: Function,
      default: () => {},
    },
    subLevels: {
      type: Array,
      default: () => [],
    },
    customFieldsLib: {
      type: Object,
      default: () => ({}),
    },
    original: {
      type: null,
      default: null,
    },
    nameMapping: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      active: false,
    }
  },
  computed: {
    ...mapState('system', {
      systemDicts: (state) => state,
    }),
    ...mapState('projects', {
      projectDicts: (state) => state.projectStructure,
    }),
    validator() {
      return new Validator()
    },
    internalValue: {
      get() {
        if (this.isDate) {
          return new Date(this.value)
        }
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    column() {
      if (
        this.type === null ||
        (!this.type.startsWith('MOH') && !this.type.startsWith('INV'))
      ) {
        return this.type
      } else {
        return 'custom_field'
      }
    },
    isPartner() {
      return this.column === 'partners'
    },
    isLinks() {
      return this.column === 'links'
    },
    isDate() {
      return ['start_date', 'end_date', 'implementation_dates'].includes(
        this.column
      )
    },
    isTextArea() {
      return [
        'geographic_scope',
        'implementation_overview',
        'name',
        'contact_name',
        'contact_email',
        'mobile_application',
        'wiki',
        'repository',
        'health_workers',
        'clients',
        'facilities',
        'overview',
        'program_targets',
        'program_targets_achieved',
        'current_achievements',
        'awp',
        'total_budget_narrative',
        'funding_needs',
        'partnership_needs',
        'total_budget',
        'target_group_reached',
      ].includes(this.column)
    },
    isForced() {
      return ['country', 'donors'].includes(this.column)
    },
    isDisabled() {
      return this.isForced || this.disabled
    },
    parsedValue() {
      const result = {
        names: Array.isArray(this.value) ? this.value : [this.value],
        ids: Array.isArray(this.value) ? this.value : [this.value],
      }
      if (!this.column) {
        return result
      } else {
        const resolver = {
          organisation: () => this.findSystemValue('organisations'),
          platforms: () =>
            this.findProjectCollectionValue('technology_platforms', true),
          dhis: () =>
            this.findProjectCollectionValue(
              'strategies',
              true,
              'subGroups',
              'strategies'
            ),
          health_focus_areas: () =>
            this.findProjectCollectionValue(
              'health_focus_areas',
              true,
              'health_focus_areas'
            ),
          hsc_challenges: () =>
            this.findProjectCollectionValue(
              'hsc_challenges',
              true,
              'challenges'
            ),
          start_date: () => this.parseDate(),
          end_date: () => this.parseDate(),
          goal_area: () => this.findProjectCollectionValue('goal_areas'),
          result_area: () => this.findProjectCollectionValue('result_areas'),
          capability_levels: () =>
            this.findProjectCollectionValue('capability_levels', true),
          capability_categories: () =>
            this.findProjectCollectionValue('capability_categories', true),
          capability_subcategories: () =>
            this.findProjectCollectionValue('capability_subcategories', true),
          // INVENT
          total_budget: () => this.parseNumber(),
          target_group_reached: () => this.parseNumber(),
          wbs: () => this.stringArray(),
          team: () => this.stringArray(),
          links: () => this.parseLinks(),
          partners: () => this.parsePartners(),
          unicef_sector: () => this.findProjectCollectionValue('sectors', true),
          functions: () => this.findProjectCollectionValue('functions', true),
          currency: () => this.findProjectCollectionValue('currencies', false),
          phase: () => this.findProjectCollectionValue('phases', false),
          hardware: () => this.findProjectCollectionValue('hardware', true),
          nontech: () => this.findProjectCollectionValue('nontech', true),
          regional_priorities: () =>
            this.findProjectCollectionValue('regional_priorities', true),
          innovation_categories: () =>
            this.findProjectCollectionValue('innovation_categories', true),
          cpd: () => this.findProjectCollectionValue('cpd', true),
          custom_field: () => {
            const q = this.customFieldsLib[this.type]
            if (!q) {
              return { ids: [], names: [] }
            }
            if (q.type < 4) {
              return result
            } else if (q.type >= 4) {
              const options = this.stringToArray(this.value)
              const filtered = options.filter((o) => q.options.includes(o))
              return { ids: [...filtered], names: [...filtered] }
            }
          },
        }
        const res = resolver[this.column]
        return res ? res() : result
      }
    },
    parsingFailed() {
      return this.value && this.column && this.parsedValue.ids.length === 0
    },
    errorMessage() {
      const e = this.errors.find((e) => e.field === this.column)
      return e ? e.msg : null
    },
  },
  watch: {
    column: {
      immediate: true,
      handler(column) {
        this.validate()
      },
    },
    value: {
      immediate: true,
      handler(value) {
        this.validate()
      },
    },
  },
  methods: {
    async validate() {
      const name = this.nameMapping[this.column] || this.column
      const { valid, errors } = await this.validator.verify(
        this.apiValue(),
        this.rules,
        { name }
      )
      this.handleValidation(valid, errors[0], this.column)
    },
    clickHandler() {
      if (
        this.isDate ||
        this.isDisabled ||
        this.isTextArea ||
        this.isCoverage
      ) {
        this.active = true
        return
      }
      if (this.column) {
        this.$emit('openDialog', {
          value: this.parsedValue.ids,
          column: this.column,
          type: this.type,
        })
      }
    },
    getLinkHeader(link_type) {
      const type = find(this.systemDicts.link_types, (t) => t.id === link_type)
      return type ? `${type.name} URL` : link_type
    },
    parseLinks() {
      const names = []
      let ids =
        typeof this.value !== 'string'
          ? this.value
          : compact(
              chunk(this.stringToArray(this.value), 2).map((list) => {
                const type = find(
                  this.systemDicts.link_types,
                  (type) => type.name.substr(0, 3) === list[0].substr(0, 3)
                )
                if (type) {
                  names.push(list[1])
                } else {
                  return
                }
                return {
                  link_type: type.id,
                  link_url: list[1],
                }
              })
            )
      ids = ids.filter((value) => {
        return value.link_url
      })
      return { ids, names }
    },
    parsePartners() {
      const names = []
      const ids =
        typeof this.value !== 'string'
          ? this.value
          : compact(
              chunk(this.stringToArray(this.value), 5).map((list) => {
                const type = find(
                  this.systemDicts.partner_types,
                  (type) => type.name.substr(0, 3) === list[0].substr(0, 3)
                )
                if (type) {
                  names.push(list[1])
                } else {
                  return
                }
                return {
                  partner_type: type.id,
                  partner_name: list[1],
                  partner_contact: list[2],
                  partner_email: list[3],
                  partner_website: list[4],
                }
              })
            )
      ids.forEach(function (value, key) {
        ids[key] = pickBy(value, (val) => val || val === 0)
      })
      return { ids, names }
    },
    parseDate() {
      const result = this.value ? new Date(this.value) : null
      return {
        ids: [result],
        names: [result],
      }
    },
    parseNumber() {
      const result = this.value ? this.value * 1 : null
      return {
        ids: [result],
        names: [result],
      }
    },
    stringToArray(value) {
      if (Array.isArray(value)) {
        return value
      }
      if (typeof value === 'string') {
        let splitted = []
        if (value.includes('|')) {
          splitted = value.split('|')
        } else {
          splitted = value.split(';')
        }
        return splitted.map((v) => v.trim())
      }
      return [value]
    },
    toInternalRepresentation(filtered) {
      return filtered.reduce(
        (a, c) => {
          a.ids.push(c.id)
          a.names.push(c.challenge || c.name)
          return a
        },
        { names: [], ids: [] }
      )
    },
    stringArray() {
      const filtered = this.stringToArray(this.value).map((st) => ({
        id: st,
        name: st,
      }))
      return this.toInternalRepresentation(filtered)
    },
    valueParser(isMultiple) {
      if (!Array.isArray(this.value)) {
        return isMultiple ? this.stringToArray(this.value) : [this.value]
      } else {
        return this.value
      }
    },
    findSystemValue(collection, isMultiple) {
      const value = this.valueParser(isMultiple)
      const filtered = this.systemDicts[collection].filter((c) =>
        value.some((d) => d === c.id || d === c.name)
      )
      return this.toInternalRepresentation(filtered)
    },
    findProjectCollectionValue(collection, isMultiple, ...subValues) {
      const value = this.valueParser(isMultiple)
      let projectData = this.projectDicts[collection]
      if (subValues && Array.isArray(subValues)) {
        subValues.forEach((subKey) => {
          projectData = projectData.reduce((a, c) => {
            a.push(...c[subKey])
            return a
          }, [])
        })
      }
      const filtered = projectData.filter((c) =>
        value.some((d) => d === c.id || d === c.name || d === c.challenge)
      )
      return this.toInternalRepresentation(filtered)
    },
    apiValue() {
      const isMultiple = [
        'team',
        'partners',
        'platforms',
        'health_focus_areas',
        'hsc_challenges',
        'dhis',
        'capability_levels',
        'capability_categories',
        'capability_subcategories',
        'custom_field',
        'functions',
        'hardware',
        'nontech',
        'regional_priorities',
        'innovation_categories',
        'unicef_sector',
        'cpd',
        'wbs',
        'links',
      ]
      const isIds = [
        ...isMultiple,
        'currency',
        'phase',
        'donors',
        'country',
        'organisation',
        'goal_area',
        'result_area',
      ]
      const idsOrNames = isIds.includes(this.column)
        ? this.parsedValue.ids
        : this.parsedValue.names
      return isMultiple.includes(this.column) ? idsOrNames : idsOrNames[0]
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SmartCell {
  position: relative;

  .Content {
    width: 100%;
    height: 100%;

    .ParsedList {
      list-style: none;
    }
  }

  .ErrorOverlay {
    padding: 2px;
    opacity: 0;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    transition: all 0.3s ease-in;
    background-color: #f5f5f5;
  }

  &:hover {
    .ErrorOverlay {
      opacity: 1;
    }
  }

  &.Disabled {
    cursor: not-allowed;
    pointer-events: none;
  }

  &.ValidationError {
    border: 2px solid @colorDanger !important;

    .ErrorOverlay {
      background-color: @colorDanger;
      color: @colorWhite;
      font-weight: 500;
    }
  }

  &.ParsingError {
    border: 2px solid @colorDraft !important;

    .ErrorOverlay {
      background-color: @colorDraft;
    }
  }

  .OriginalValue {
    font-style: italic;
  }

  .el-textarea {
    textarea {
      font-size: @fontSizeSmall;
    }
  }

  ul {
    margin: 0;
    padding-left: 20px;
  }
}
</style>
