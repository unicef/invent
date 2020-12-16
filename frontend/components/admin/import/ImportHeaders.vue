<template>
  <div class="Headers">
    <div v-if="internalValue.length > 0" class="Row">
      <div class="Column Thin Header">
        <slot />
      </div>

      <div
        v-for="(header, index) in internalValue"
        :key="index"
        class="Column Header"
      >
        <div class="Title">
          {{ header.title }}
        </div>
        <el-button
          class="DeleteColumnButton"
          size="mini"
          type="danger"
          @click="rmHeader(index)"
        >
          <fa icon="times" />
        </el-button>
        <el-select
          v-model="header.selected"
          class="HeaderSelect"
          size="small"
          filterable
          clearable
          @change="columnChange(header)"
        >
          <el-option
            v-for="item in availableFields(header.selected)"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>

      <div class="Column Header">
        <div class="Title">
          <fa icon="info" />
          <translate>Select an header to create a new column</translate>
        </div>
        <div>
          <el-select
            v-model="additonalHeader"
            class="HeaderSelect"
            size="small"
            filterable
            clearable
          >
            <el-option
              v-for="item in notUsedFields"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { projectFields } from '@/utilities/projects'

const blackList = [
  'modified',
  'organisation',
  'country',
  'country_office',
  'donors',
  'coverage',
  'national_level_deployment',
  'coverageData',
  'viewers',
  'coverageType',
  'coverage_second_level',
  'interoperability_links',
  // New invent fields
  'innovation_ways',
  'isc',
  'end_date_note',
  'research',
  'stages',
  'stagesDraft',
]

export default {
  props: {
    headers: {
      type: Array,
      default: () => [],
    },
    id: {
      type: [Number, String],
      default: null,
    },
    customFieldsLib: {
      type: Object,
      default: () => ({}),
    },
    nameMapping: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      internalValue: null,
      additonalHeader: null,
    }
  },
  computed: {
    fields() {
      return [
        ...Object.keys(projectFields()).filter((k) => !blackList.includes(k)),
        ...Object.keys(this.customFieldsLib),
      ]
    },
    notUsedFields() {
      const selected = this.headers.map((h) => h.selected).filter((s) => s)
      return this.fields
        .filter((f) => !selected.includes(f))
        .map((f) => {
          return {
            label: this.nameMapping[f] || f,
            value: f,
          }
        })
        .sort((a, b) => a.label.localeCompare(b.label))
    },
  },
  watch: {
    headers: {
      immediate: true,
      handler(headers) {
        this.internalValue = headers.map((h) => ({ ...h }))
      },
    },
    additonalHeader: {
      immediate: false,
      handler(column) {
        if (column) {
          const mappeName = this.nameMapping[column]
          this.internalValue.push({
            selected: column,
            title: mappeName || column,
          })
          this.additonalHeader = null
          this.columnChange()
        }
      },
    },
  },
  methods: {
    async rmHeader(index) {
      try {
        await this.$confirm(
          this.$gettext('Are you sure? this operation is not reversible'),
          this.$gettext('Column Delete'),
          {
            confirmButtonText: this.$gettext('OK'),
            cancelButtonText: this.$gettext('Cancel'),
            type: 'warning',
          }
        )
        this.$delete(this.internalValue, index)
        this.columnChange()
      } catch (e) {
        this.$message({
          type: 'info',
          message: 'Delete canceled',
        })
      }
    },
    availableFields(value) {
      if (value && !this.notUsedFields.some((f) => f.value === value)) {
        return [
          { label: this.nameMapping[value] || value, value },
          ...this.notUsedFields,
        ]
      }
      return this.notUsedFields
    },
    async columnChange() {
      const { data } = await this.$axios.patch(
        `/api/projects/import/${this.id}/`,
        {
          header_mapping: this.internalValue,
        }
      )
      this.$emit('update:headers', data.header_mapping)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.Headers {
  position: sticky;
  top: 0;
  z-index: 10;

  .Row {
    .Column {
      &.Header {
        border-width: 1px 1px 1px 0;
        position: relative;
        background-color: #f5f5f5;
        z-index: 10;
        overflow: hidden;

        &:first-child {
          border-width: 1px;
        }
      }
    }
  }

  .Title {
    margin-right: 8px;
  }
  .DeleteColumnButton {
    position: absolute;
    top: 0;
    right: 0;
    padding: 2px 4px;
  }
  .HeaderSelect {
    position: absolute;
    bottom: 4px;
    left: 3.5px;
    width: 192px;
  }
}
</style>
