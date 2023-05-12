<template>
  <el-select
    v-model="innerValue"
    filterable
    reserve-keyword
    autocomplete
    remote
    clearable
    multiple
    :remote-method="filterMethod"
    :placeholder="$gettext('Type and select a user') | translate"
    class="FocalPointSelector"
  >
    <el-option v-for="item in filteredOptions" :key="item.email" :label="item.label" :value="item.email"> </el-option>
  </el-select>
</template>

<script>
import { mapGetters } from 'vuex'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin.js'

export default {
  mixins: [VeeValidationMixin],
  filters: {
    truncate(str) {
      if (str.length > 50) return `${str.substr(0, 47)}...`
      return str
    },
  },
  $_veeValidate: {
    value() {
      return this.value
    },
    events: 'change|blur',
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      filteredOptions: [],
    }
  },
  computed: {
    ...mapGetters({
      userProfiles: 'system/getUserProfilesWithLabel',
    }),

    innerValue: {
      get() {
        if (this.value !== null) {
          return [this.value.toString()]
        } else {
          return []
        }
      },
      set(value) {
        if (value[0]) {
          this.$emit('change', value[value.length - 1].toString())
        } else {
          this.$emit('change', null)
        }
      },
    },
  },
  methods: {
    filterMethod(query) {
      if (query) {
        this.filteredOptions = this.userProfiles.filter(
          (p) => this.filter(p.name ? p.name : p.email, query) || (p.email ? this.filter(p.email, query) : false)
        )
      } else {
        this.filteredOptions = []
      }
    },
    filter(val, query) {
      return val.toLowerCase().startsWith(query.toLowerCase())
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.FocalPointSelector {
  width: 100%;
  word-wrap: normal;

  .el-select-dropdown__item.selected {
    // display: none;
  }

  .el-tag {
    height: fit-content;
    word-wrap: normal;
    white-space: normal;
  }

  &.el-select {
    .el-tag {
      &:hover {
        background-color: white;
        border-color: #777779;
      }
    }
  }
}

.NoDisplay {
  display: none;
}
</style>
