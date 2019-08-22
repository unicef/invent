<template>
  <div
    :class="['SmartCell', {'Disabled': isDisabled, 'ValidationError': errorMessage, 'ParsingError': parsingFailed}]"
    @click="clickHandler"
  >
    <div class="Content">
      <template v-if="column">
        <div
          v-if="active"
          class="active"
        >
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

        <template v-else-if="isDate || isTextArea">
          {{ internalValue }}
        </template>

        <template v-else-if="parsedValue && parsedValue.names">
          <ul class="ParsedList">
            <li
              v-for="(name, index) in parsedValue.names"
              :key="index"
            >
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
    <div
      v-if="errorMessage || parsingFailed"
      class="ErrorOverlay"
    >
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
import DateField from '@/components/admin/import/DateField';
import { Validator } from 'vee-validate';
import { mapState } from 'vuex';
import { format } from 'date-fns';

export default {
  components: {
    DateField
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: null,
      default: null
    },
    type: {
      type: String,
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    },
    rules: {
      type: Object,
      default: null
    },
    errors: {
      type: Array,
      default: () => []
    },
    handleValidation: {
      type: Function,
      default: () => {}
    },
    subLevels: {
      type: Array,
      default: () => []
    },
    customFieldsLib: {
      type: Object,
      default: () => ({})
    },
    original: {
      type: null,
      default: null
    },
    nameMapping: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      active: false
    };
  },
  computed: {
    ...mapState('system', {
      systemDicts: state => state
    }),
    ...mapState('projects', {
      projectDicts: state => state.projectStructure
    }),
    validator () {
      return new Validator();
    },
    internalValue: {
      get () {
        if (this.isDate) {
          return new Date(this.value);
        }
        return this.value;
      },
      set (value) {
        this.$emit('change', value);
      }
    },
    column () {
      if (this.type === null || (!this.type.startsWith('MOH') && !this.type.startsWith('INV'))) {
        return this.type;
      } else {
        return 'custom_field';
      }
    },
    isDate () {
      return ['start_date', 'end_date', 'implementation_dates'].includes(this.column);
    },
    isTextArea () {
      return ['geographic_scope', 'implementation_overview', 'name',
        'contact_name', 'contact_email', 'mobile_application',
        'wiki', 'repository', 'health_workers', 'clients', 'facilities'].includes(this.column);
    },
    isForced () {
      return ['country', 'donors'].includes(this.column);
    },
    isDisabled () {
      return this.isForced || this.disabled;
    },
    parsedValue () {
      const result = { names: Array.isArray(this.value) ? this.value : [this.value], ids: Array.isArray(this.value) ? this.value : [this.value] };
      if (!this.column) {
        return result;
      } else {
        const resolver = {
          organisation: () => this.findSystemValue('organisations'),
          platforms: () => this.findProjectCollectionValue('technology_platforms', false),
          dhis: () => this.findProjectCollectionValue('strategies', true, 'subGroups', 'strategies'),
          health_focus_areas: () => this.findProjectCollectionValue('health_focus_areas', true, 'health_focus_areas'),
          hsc_challenges: () => this.findProjectCollectionValue('hsc_challenges', true, 'challenges'),
          start_date: () => this.parseDate(),
          end_date: () => this.parseDate(),
          field_office: () => this.findProjectCollectionValue('field_offices'),
          goal_area: () => this.findProjectCollectionValue('goal_areas'),
          result_area: () => this.findProjectCollectionValue('result_areas'),
          capability_levels: () => this.findProjectCollectionValue('capability_levels', true),
          capability_categories: () => this.findProjectCollectionValue('capability_categories', true),
          capability_subcategories: () => this.findProjectCollectionValue('capability_subcategories', true),

          custom_field: () => {
            const q = this.customFieldsLib[this.type];
            if (!q) {
              return { ids: [], names: [] };
            }
            if (q.type < 4) {
              return result;
            } else if (q.type >= 4) {
              const options = this.stringToArray(this.value);
              const filtered = options.filter(o => q.options.includes(o));
              return { ids: [...filtered], names: [...filtered] };
            }
          }
        };
        const res = resolver[this.column];
        return res ? res() : result;
      }
    },
    parsingFailed () {
      return this.value && this.column && this.parsedValue.ids.length === 0;
    },
    errorMessage () {
      const e = this.errors.find(e => e.field === this.column);
      return e ? e.msg : null;
    }
  },
  watch: {
    column: {
      immediate: true,
      handler (column) {
        this.validate();
      }
    },
    value: {
      immediate: true,
      handler (value) {
        this.validate();
      }
    }
  },
  methods: {
    async validate () {
      const name = this.nameMapping[this.column] || this.column;
      const { valid, errors } = await this.validator.verify(this.apiValue(), this.rules, { name });
      this.handleValidation(valid, errors[0], this.column);
    },
    clickHandler () {
      if (this.isDate || this.isDisabled || this.isTextArea || this.isCoverage) {
        this.active = true;
        return;
      }
      if (this.column) {
        this.$emit('openDialog', { value: this.parsedValue.ids, column: this.column, type: this.type });
      }
    },
    parseDate () {
      const result = this.value ? format(this.valie, 'dd/MM/yyyy', new Date(null)) : null;
      return {
        ids: [result],
        names: [result]
      };
    },
    stringToArray (value) {
      if (Array.isArray(value)) {
        return value;
      }
      if (typeof value === 'string') {
        let splitted = [];
        if (value.includes('|')) {
          splitted = value.split('|');
        } else {
          splitted = value.split(';');
        }
        return splitted.map(v => v.trim());
      }
      return [value];
    },
    toInternalRepresentation (filtered) {
      return filtered.reduce((a, c) => {
        a.ids.push(c.id);
        a.names.push(c.challenge || c.name);
        return a;
      }, { names: [], ids: [] });
    },
    stringArray () {
      const filtered = this.stringToArray(this.value)
        .map(st => ({ id: st, name: st }));
      return this.toInternalRepresentation(filtered);
    },
    valueParser (isMultiple) {
      if (!Array.isArray(this.value)) {
        return isMultiple ? this.stringToArray(this.value) : [this.value];
      } else {
        return this.value;
      }
    },
    findSystemValue (collection, isMultiple) {
      const value = this.valueParser(isMultiple);
      const filtered = this.systemDicts[collection].filter(c => value.some(d => d === c.id || d === c.name));
      return this.toInternalRepresentation(filtered);
    },
    findProjectCollectionValue (collection, isMultiple, ...subValues) {
      const value = this.valueParser(isMultiple);
      let projectData = this.projectDicts[collection];
      if (subValues && Array.isArray(subValues)) {
        subValues.forEach(subKey => {
          projectData = projectData.reduce((a, c) => {
            a.push(...c[subKey]);
            return a;
          }, []);
        });
      }
      const filtered = projectData.filter(c => value.some(d => d === c.id || d === c.name || d === c.challenge));
      return this.toInternalRepresentation(filtered);
    },
    apiValue () {
      const isMultiple = ['platforms', 'health_focus_areas', 'hsc_challenges', 'dhis', 'capability_levels', 'capability_categories', 'capability_subcategories', 'custom_field'];
      const isIds = [...isMultiple, 'donors', 'country', 'organisation', 'field_office', 'goal_area', 'result_area'];
      const idsOrNames = isIds.includes(this.column) ? this.parsedValue.ids : this.parsedValue.names;
      return isMultiple.includes(this.column) ? idsOrNames : idsOrNames[0];
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

  .SmartCell {
    position: relative;

    .Content {
      width: 100%;
      height: 100%;

      .ParsedList{
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
      background-color: #F5F5F5;
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
