<template>
  <div class="HealthInformationSystem">
    <selector-dialog-column
      :header-selectable="true"
      :selected="catSelected"
      :header="$gettext('Select from list') | translate"
      @headerSelected="toggleAll"
    >
      <selector-dialog-category
        :values="selected"
        :category="healthInformationSystems"
        hide-header
        @change="filterChange"
      />
    </selector-dialog-column>
  </div>
</template>

<script>
import difference from 'lodash/difference';
import SelectorDialogColumn from '../SelectorDialogColumn';
import SelectorDialogCategory from '../SelectorDialogCategory';
import { mapGetters } from 'vuex';

export default {
  components: {
    SelectorDialogColumn,
    SelectorDialogCategory
  },
  props: {
    selected: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    ...mapGetters({
      healthInformationSystems: 'projects/getHisBucket'
    }),
    catSelected () {
      const ids = this.healthInformationSystems.map(s => s.id);
      return difference(ids, this.selected).length === 0;
    }
  },
  methods: {
    filterChange (value) {
      this.$emit('update:selected', [...value]);
    },
    toggleAll (value) {
      if (value) {
        this.$emit('update:selected', [...this.healthInformationSystems.map(s => s.id)]);
      } else {
        this.$emit('update:selected', []);
      }
    }
  }
};
</script>

<style>

</style>
