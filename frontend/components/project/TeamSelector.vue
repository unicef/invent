<template>
  <lazy-el-select
    slot="reference"
    :value="value"
    :placeholder="$gettext('Type and select a name') | translate"
    :remote-method="filterList"
    multiple
    filterable
    remote
    class="TeamSelector"
    :popper-class="optionsAndValues.length > value.length ? 'TeamSelectorDropdown' : 'NoDisplay'"
    @change="changeHandler"
    v-outside="{
      exclude: [],
      handler: 'onOutside'
    }"
    @keyup.enter.native="onEnter"
    v-paste="{
      exclude: [],
      handler: 'onPaste'
    }"
  >
    <el-option
      v-for="person in optionsAndValues"
      :key="person.id"
      :label="`${person.name ? person.name + ', ': ''}${person.organisation ?  getOrganisationDetails(person.organisation).name : ''} ${person.name ? '(' + person.email + ')' : person.email }` | truncate"
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
  data() {
    return {
      invalidEmails: []
    }
  },
  computed: {
    ...mapGetters({
      items: 'system/getUserProfilesNoFilter',
      getOrganisationDetails: 'system/getOrganisationDetails'
    })
  },
  filters: {
    truncate (str) {
      if (str.length > 50 ) return `${str.substr(0, 47)}...`
      return str
    }
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    },
    onOutside () {
      this.emitEmails(this.validEmails(this.emailList(this.query)));
      this.query = '';
      this.errorMessage();
    },
    onPaste (str, e) {
      // good paste
      // pepe@unicef.org, trending@unicef.org

      // bad paste
      // pepe@pepito.com, doni@asd
      const emails = this.emailList(str);
      const validEmails = this.validEmails(emails);
      this.errorMessage();

      if (emails.length === validEmails.length) {
        this.emitEmails(validEmails);
        e.target.blur();
      }
    },
    onEnter(e) {
      this.emitEmails(this.validEmails(this.emailList(e.target.value)));
      this.errorMessage();
    },
    emailList (str) {
      return str.trim().replace(/ /g,'').split(',');
    },
    emitEmails (mails) {
      mails.map(email => this.$emit('change', email));
    },
    validEmails (mails) {
      return mails.filter(email => this.validateEmail(email) && !this.arrIncludes(email))
    },
    arrIncludes (val) {
      return this.value.includes(val);
    },
    validateEmail (email) {
      const valid = validator.isEmail(email) && (email.endsWith('unicef.org') || email.endsWith('pulilab.com'));
      if (!valid) {
        this.invalidEmails = [...this.invalidEmails, email]
      }
      return valid;
    },
    errorMessage () {
      if (this.invalidEmails.length > 0 && this.invalidEmails[0] !== "") {
        this.$message({
          dangerouslyUseHTMLString: true,
          message: `<b>${this.invalidEmails.join(', ')}</b> ${this.$gettext(`cant't be added. Make sure email is part of unicef.org`)}`,
          type: 'error'
        });
      }
      this.invalidEmails = [];
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
