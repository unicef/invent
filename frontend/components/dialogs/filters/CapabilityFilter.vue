<template>
  <div class="CapabilityFilter">
    <selector-dialog-column
      :header-selectable="true"
      :selected="catSelected"
      :header="$gettext('Select from list') | translate"
      @headerSelected="toggleAll"
    >
      <selector-dialog-category
        :values="selected"
        :category-selectable="true"
        :category="items"
        hide-header
        @change="filterChange"
      />
    </selector-dialog-column>
  </div>
</template>

<script>
import difference from 'lodash/difference'
import { mapGetters } from 'vuex'
import SelectorDialogColumn from '../SelectorDialogColumn'
import SelectorDialogCategory from '../SelectorDialogCategory'

export default {
  components: {
    SelectorDialogColumn,
    SelectorDialogCategory,
  },
  props: {
    selected: {
      type: Array,
      default: () => [],
    },
    goalArea: {
      type: Number,
      required: true,
    },
    type: {
      type: String,
      required: true,
      validator: (value) =>
        [
          'capabilityLevels',
          'capabilityCategories',
          'capabilitySubcategories',
        ].includes(value),
    },
  },
  computed: {
    ...mapGetters({
      capabilityLevels: 'projects/getCapabilityLevels',
      capabilityCategories: 'projects/getCapabilityCategories',
      capabilitySubcategories: 'projects/getCapabilitySubcategories',
    }),
    items() {
      return this[this.type](this.goalArea)
    },
    catSelected() {
      const ids = this.items.map((s) => s.id)
      return difference(ids, this.selected).length === 0
    },
  },
  methods: {
    filterChange(value) {
      this.$emit('update:selected', [...value])
    },
    toggleAll(value) {
      if (value) {
        this.$emit('update:selected', [...this.items.map((s) => s.id)])
      } else {
        this.$emit('update:selected', [])
      }
    },
  },
}
</script>

<style></style>
