<template>
  <el-select
    v-model="innerValue"
    filterable
    reserve-keyword
    autocomplete
    remote
    clearable
    :remote-method="filterMethod"
    :placeholder="$gettext('Type and select a user') | translate"
    class="UserProfileSelector"
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
      userProfiles: 'system/getUserProfilesNoFilter',
      getOrganisationDetails: 'system/getOrganisationDetails',
    }),

    innerValue: {
      get() {
        if (this.value !== null) {
          return this.value
        } else {
          return ''
        }
      },
      set(value) {
        this.$emit('change', value)
      },
    },
    concatUserData() {
      return this.userProfiles.map((user) => ({
        ...user,
        label: `${user.name} , ${user.email}`,
      }))
    },
  },
  methods: {
    filterMethod(query) {
      if (query) {
        this.filteredOptions = this.concatUserData.filter(
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

.UserProfileSelector {
  width: 100%;
  .el-select-dropdown__item.selected {
    // display: none;
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
    height: 50px;
    .email {
      float: left;
      width: 100%;
      margin-top: -18px;
    }
  }
}
</style>
