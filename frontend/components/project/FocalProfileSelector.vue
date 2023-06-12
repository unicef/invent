<template>
  <el-select
    v-model="innerValue"
    multiple
    filterable
    default-first-option
    autocomplete
    clearable
    remote
    value-key="email"
    :remote-method="filterMethod"
    :placeholder="$gettext('Type and select a user') | translate"
    :popper-class="optionsWithValues.length > innerValue.length ? 'TeamSelectorDropdown' : 'NoDisplay'"
    class="FocalPointSelector"
  >
    <el-option v-for="item in optionsWithValues" :key="item.email" :label="item.label" :value="item.email"
      ><span style="float: left">{{ item.label }}</span>
      <br />
      <span class="email"
        ><small>{{ item.info }}</small></span
      >
    </el-option>
  </el-select>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
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
          return [this.value]
        } else {
          return []
        }
      },
      set(value) {
        if (value[0]) {
          this.$emit('change', value[value.length - 1])
        } else {
          this.$emit('change', null)
        }
      },
    },
    optionsWithValues() {
      return [
        ...this.filteredOptions.filter((profile) => profile.email !== this.value),
        ...this.userProfiles.filter((profile) => profile.email === this.value),
      ]
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

.TeamSelectorDropdown {
  .OrganisationItem {
    display: inline-block;
    margin-left: 6px;
    font-weight: 400;
    color: @colorGray;
    &::before {
      content: '(';
    }
    &::after {
      content: ')';
    }
  }
  li {
    height: fit-content;
    padding-bottom: 4px;
    .email {
      float: left;
      width: 100%;
      margin-top: -8px;
      line-height: 1.2;
    }
  }
}

.el-select-dropdown__item {
  max-width: 64vw;
  min-width: 740px;
  height: fit-content;
  word-wrap: normal;
  white-space: normal;
}
</style>
