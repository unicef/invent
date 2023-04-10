<template>
  <el-select
    v-model="innerValue"
    :multiple="multiple"
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
      type: Array,
      default: null,
    },
    multiple: {
      type: Boolean,
      default: true,
    },
    ommit: {
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
        /**Get user ids [numArray] and translate to email array from user list, if ommit email string exist we find if user id and remove it */
        const stringEmailsArr = this.value.map(
          (userId) => this.userProfiles.find((profile) => profile.id === userId).email
        )

        if (this.ommit) {
          return stringEmailsArr.filter((user) => user !== this.ommit)
        } else {
          return stringEmailsArr
        }
      },
      set(value) {
        /**Get email array as input and translate to userIds number array, If ommit user exist we add it back */

        if (this.ommit) {
          const emailSet = new Set([...value, this.ommit])
          const withOmmited = [...emailSet]
          const userIds = withOmmited.map(
            (userEmail) => this.userProfiles.find((profile) => profile.email === userEmail).id
          )
          this.$emit('change', userIds)
        } else {
          const userIds = value.map((userEmail) => this.userProfiles.find((profile) => profile.email === userEmail).id)
          this.$emit('change', userIds)
        }
      },
    },
    concatUserData() {
      if (this.ommit) {
        return this.userProfiles.filter((user) => user.email !== this.ommit)
      } else {
        return this.userProfiles
      }
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
