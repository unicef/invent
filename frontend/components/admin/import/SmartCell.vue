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
          <el-radio-group
            v-if="isGovInvestor"
            v-model="internalValue"
          >
            <el-radio :label="0">
              <translate>
                No, they have not yet contributed
              </translate>
            </el-radio>
            <el-radio :label="1">
              <translate>
                Yes, they are contributing in-kind people or time
              </translate>
            </el-radio>
            <el-radio :label="2">
              <translate>
                Yes, there is a financial contribution through MOH budget
              </translate>
            </el-radio>
          </el-radio-group>
        </div>

        <template v-else-if="isDate || isTextArea || isGovInvestor">
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
    isGovInvestor () {
      return this.column === 'government_investor';
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
          digitalHealthInterventions: () => this.findProjectCollectionValue('strategies', true, 'subGroups', 'strategies'),
          health_focus_areas: () => this.findProjectCollectionValue('health_focus_areas', true, 'health_focus_areas'),
          hsc_challenges: () => this.findProjectCollectionValue('hsc_challenges', true, 'challenges'),
          his_bucket: () => this.findProjectCollectionValue('his_bucket', true),
          implementing_partners: this.stringArray,
          government_investor: () => {
            const labelLib = {
              'no they have not yet contributed': 0,
              'yes they are contributing inkind people or time': 1,
              'yes there is a financial contribution through moh budget': 2
            };
            const cleaned = ('' + this.value).replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '').toLowerCase();
            const value = Number.isInteger(this.value) ? this.value : labelLib[cleaned];
            const label = !Number.isInteger(this.value) ? this.value : Object.keys(labelLib).find(k => labelLib[k] === cleaned);
            return {
              ids: [value],
              names: [label]
            };
          },
          licenses: () => this.findProjectCollectionValue('licenses', true),
          interoperability_links: () => this.findProjectCollectionValue('interoperability_links'),
          interoperability_standards: () => this.findProjectCollectionValue('interoperability_standards', true),
          sub_level: () => {
            const value = Array.isArray(this.value) ? this.value[0] : this.value;
            const level = this.subLevels.find(cf => cf.id === value || cf.name === value);
            if (level) {
              return { names: [level.name], ids: [level.id] };
            }
            return { names: [], ids: [] };
          },
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
      if (this.isDate || this.isDisabled || this.isTextArea || this.isCoverage || this.isGovInvestor) {
        this.active = true;
        return;
      }
      if (this.column) {
        this.$emit('openDialog', { value: this.parsedValue.ids, column: this.column, type: this.type });
      }
    },
    stringToArray (value) {
      if (Array.isArray(value)) {
        return value;
      }
      if (typeof value === 'string') {
        let splitted = [];
        if (value.includes(',')) {
          splitted = value.split(',');
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
      const isMultiple = ['platforms', 'implementing_partners', 'health_focus_areas', 'hsc_challenges', 'his_bucket', 'licenses', 'interoperability_standards', 'custom_field', 'digitalHealthInterventions'];
      const isIds = [...isMultiple, 'donors', 'country', 'organisation', 'government_investor', 'sub_level'];
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
    }

    &.ValidationError {
      border: 2px solid red !important;

      .ErrorOverlay {
        background-color: red;
      }
    }

    &.ParsingError {
      border: 2px solid orange !important;

      .ErrorOverlay {
        background-color: orange;
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
