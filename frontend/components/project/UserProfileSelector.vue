<template>
  <el-select
    v-model="innerValue"
    :multiple="multiple"
    filterable
    autocomplete
    remote
    :remote-method="filterMethod"
    :placeholder="$gettext('Type and select a user') | translate"
    :class="omit ? 'UserProfileSelector focalFirst' : 'UserProfileSelector'"
    :popper-class="popperClass ? 'TeamSelectorDropdown' : 'NoDisplay'"
  >
    <el-option
      v-for="item in optionsWithValues"
      :key="item.id"
      :label="item.label"
      :value="item.id"
      :disabled="item.disabled ? item.disabled : false"
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
      type: Array,
      default: null,
    },
    multiple: {
      type: Boolean,
      default: true,
    },
    omit: {
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
        /**Get user ids [numArray] and translate to email array from user list, if omit email string exist we find if user id and remove it */
        if (this.omit) {
          const omitId = this.userProfiles.find((user) => user.email === this.omit).id
          const restId = this.value.filter((userId) => userId !== omitId)
          return [omitId, ...restId]
        } else {
          return this.value
        }
      },
      set(value) {
        /**Get email array as input and translate to userIds number array, If omit user exist we add it back */
        this.$emit('change', [...new Set(value)])
      },
    },
    concatUserData() {
      if (this.omit) {
        return this.userProfiles.map((user) =>
          user.email !== this.omit ? { ...user, disabled: false } : { ...user, disabled: true }
        )
      } else {
        return this.userProfiles
      }
    },
    optionsWithValues() {
      const options = [
        ...this.filteredOptions,
        ...this.value
          .map((userId) => this.concatUserData.find((profile) => profile.id === userId))
          .sort((a, b) => (a.disabled ? 1 : -1)),
      ]
      return [...new Set(options)]
    },
    popperClass() {
      return this.optionsWithValues.length > this.innerValue.length + (this.omit !== null ? 1 : 0)
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
  word-wrap: normal;
  .el-select-dropdown__item.selected {
    // display: none;
  }

  el-select__tags {
    max-width: 200px;
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

.focalFirst {
  &.el-select {
    .el-tag:nth-child(1) {
      background-color: #858585;
      border-color: #807f7f;
      .el-select__tags-text {
        color: #f1f1f1;
        &:hover {
          color: black;
        }
      }
      .el-icon-close {
        display: none;
      }
      &:hover {
        background-color: white;
        border-color: #777779;
      }
    }
  }
}
</style>
