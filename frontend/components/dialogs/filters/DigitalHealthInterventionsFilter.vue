<template>
  <div class="DigitalHealthInterventionsFilter">
    <el-row type="flex">
      <el-col
        v-for="category in digitalHealthInterventions"
        :key="category.name"
        :span="6"
      >
        <selector-dialog-column
          :header-selectable="true"
          :header="category.name"
          :selected="catSelected(category)"
          @headerSelected="toggleAll($event, category)"
        >
          <template v-if="!childSelection">
            <selector-dialog-category
              :values="selected"
              :category-selectable="true"
              :category="category.subGroups"
              hide-header
              @change="filterChange"
            />
          </template>

          <template v-if="childSelection">
            <selector-dialog-category
              v-for="cat in category.subGroups"
              :key="cat.id"
              :values="selected"
              :category-selectable="true"
              :category="cat"
              child-name="strategies"
              @change="filterChange"
            />
          </template>
        </selector-dialog-column>
      </el-col>
    </el-row>
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
    childSelection: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      digitalHealthInterventions: 'projects/getDigitalHealthInterventions',
    }),
  },
  methods: {
    catSelected(category) {
      const ids = this.categoryIds(category)
      return difference(ids, this.selected).length === 0
    },
    categoryIds(category) {
      return category.subGroups.map((s) => s.id)
    },
    filterChange(value) {
      this.$emit('update:selected', [...value])
    },
    toggleAll(value, category) {
      const categoryIds = this.categoryIds(category)
      const filtered = this.selected.filter((s) => !categoryIds.includes(s))
      if (value) {
        this.$emit('update:selected', [...filtered, ...categoryIds])
      } else {
        this.$emit('update:selected', filtered)
      }
    },
  },
}
</script>

<style></style>
