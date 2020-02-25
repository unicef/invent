<template>
  <lazy-el-select
    slot="reference"
    v-outside="{
      exclude: [],
      handler: 'onOutside'
    }"
    v-paste="{
      exclude: [],
      handler: 'onPaste'
    }"
    :value="value"
    :placeholder="$gettext('Type and select a name') | translate"
    :remote-method="filterList"
    multiple
    filterable
    remote
    class="TeamSelector"
    :popper-class="optionsAndValues.length > value.length ? 'TeamSelectorDropdown' : 'NoDisplay'"
    @change="changeHandler"
    @keyup.enter.native="onEnter"
  >
    <el-option
      v-for="person in optionsAndValues"
      :key="person.id"
      :label="`${person.name ? person.name + ', ': ''}${person.organisation ? getOrganisationDetails(person.organisation).name : ''} ${person.name ? '(' + person.email + ')' : person.email }` | truncate"
      :value="person.id"
    >
      <span style="float: left;">{{ person.name ? person.name : 'N/A' }}</span>
      <template v-if="person.organisation">
        <organisation-item :id="person.organisation" />
      </template>
      <span class="email"><small>{{ person.email }}</small></span>
    </el-option>
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex';
import LightSelectMixin from '../mixins/LightSelectMixin.js';
import OrganisationItem from '../common/OrganisationItem';
import validator from 'validator';

export default {
  components: {
    OrganisationItem
  },
  filters: {
    truncate (str) {
      if (str.length > 50) return `${str.substr(0, 47)}...`;
      return str;
    }
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
      items: 'system/getUserProfilesNoFilter',
      getOrganisationDetails: 'system/getOrganisationDetails'
    })
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    },
    onOutside () {
      this.emitEmails(this.validEmails(this.emailList(this.query)));
    },
    onPaste (str, e) {
      // good paste
      // pepe@pepe.com, trending@tren.com

      // bad paste
      // pepe@pepito.com, doni@asd
      const emails = this.emailList(str);
      const validEmails = this.validEmails(emails);

      if (emails.length === validEmails.length) {
        this.emitEmails(validEmails);
        e.target.blur();
      }
    },
    onEnter (e) {
      this.emitEmails(this.validEmails(this.emailList(e.target.value)));
    },
    emailList (str) {
      return str.trim().replace(/ /g, '').split(',');
    },
    emitEmails (mails) {
      mails.map(email => this.$emit('change', email));
    },
    validEmails (mails) {
      return mails.filter(email => this.validateEmail(email) && !this.arrIncludes(email));
    },
    arrIncludes (val) {
      return this.value.includes(val);
    },
    validateEmail (email) {
      return validator.isEmail(email) && (email.endsWith('unicef.org') || email.endsWith('pulilab.com'));
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .TeamSelector {
    width: 100%;
    .el-select-dropdown__item.selected {
      display: none;
    }

    &.el-select {
      .el-tag{
        &:hover {
          background-color: white;
          border-color: #B9B9B9;
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
        content: "(";
      }

      &::after {
        content: ")";
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
