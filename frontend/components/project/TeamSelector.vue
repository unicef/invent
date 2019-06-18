<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Type and select a name') | translate"
    :remote-method="filterList"
    multiple
    filterable
    remote
    class="TeamSelector"
    popper-class="TeamSelectorDropdown"
    @change="changeHandler"
  >
    <el-option
      v-for="person in optionsAndValues"
      :key="person.id"
      :label="person.name"
      :value="person.id"
    >
      <span>{{ person.name }}</span>
      <template v-if="person.organisation">
        <organisation-item :id="person.organisation" />
      </template>
    </el-option>
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex';
import LightSelectMixin from '../mixins/LightSelectMixin.js';

import OrganisationItem from '../common/OrganisationItem';

export default {
  components: {
    OrganisationItem
  },
  mixins: [LightSelectMixin],
  $_veeValidate: {
    value () {
      return this.value;
    },
    events: 'change|blur'
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: Array,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      items: 'system/getUserProfiles'
    })
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .TeamSelector {
    width: 100%;
  }

  .TeamSelectorDropdown {
     .OrganisationItem {
      display: inline-block;
      margin-left: 6px;
      font-weight: 400;
      color: @colorGray;

      &::before {
        content: "(";
      }

      &::after {
        content: ")";
      }
    }
  }
</style>
