<template>
  <lazy-el-select
    v-model="innerValue"
    :multiple="multiple"
    slot="reference"
    filterable
    autocomplete
    remote
    clearable
    :remote-method="filterMethod"
    :placeholder="$gettext('Type and select a name') | translate"
    :popper-class="optionsWithValues.length > innerValue.length ? 'TeamSelectorDropdown' : 'NoDisplay'"
    class="TeamSelector"
  >
    <el-option v-for="person in optionsWithValues" :key="person.id" :label="person.label" :value="person.id">
      <span style="float: left">{{ person.label }}</span>
      <br />
      <span class="email"
        ><small>{{ person.info }}</small></span
      >
    </el-option>
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'

import OrganisationItem from '../common/OrganisationItem'

export default {
  components: {
    OrganisationItem,
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
      type: Array,
      default: null,
    },
    multiple: {
      type: Boolean,
      default: true,
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
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    optionsWithValues() {
      const options = [
        ...this.filteredOptions,
        ...this.value.map((userId) => this.userProfiles.find((profile) => profile.id === userId)),
      ]
      return [...new Set(options)]
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

.TeamSelector {
  width: 100%;
  word-wrap: normal;
  .el-select-dropdown__item.selected {
    display: none;
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
