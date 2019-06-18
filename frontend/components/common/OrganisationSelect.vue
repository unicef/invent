<template>
  <lazy-el-select
    v-model="innerValue"
    :allow-create="true"
    :placeholder="$gettext('Type and select a name') | translate"
    :remote-method="filterList"
    :default-first-option="true"
    filterable
    remote
    class="OrganisationSelector"
    popper-class="OrganisationSelectorDropdown"
  >
    <el-option
      v-for="organisation in optionsAndValues"
      :key="organisation.id"
      :label="organisation.name"
      :value="organisation.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import LightSelectMixin from '../mixins/LightSelectMixin.js';

export default {
  components: {
  },
  mixins: [LightSelectMixin],
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: [String, Number],
      default: null
    },
    autoSave: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      items: 'system/getOrganisations'
    }),
    innerValue: {
      get () {
        if (isNaN(this.value)) {
          return this.value;
        }
        return this.value ? +this.value : null;
      },
      set (value) {
        this.$emit('change', value);
        this.save(value);
      }
    }
  },
  methods: {
    ...mapActions({
      addOrganisation: 'system/addOrganisation'
    }),
    async save (value) {
      if (this.autoSave && !Number.isInteger(value)) {
        this.$nuxt.$loading.start('organisation');
        await this.addOrganisation(value);
        this.$nuxt.$loading.finish('organisation');
      }
    }
  }
};
</script>

<style lang="less">
.OrganisationSelector {
  width: 100%;
}
.OrganisationSelectorDropdown {
}
</style>
