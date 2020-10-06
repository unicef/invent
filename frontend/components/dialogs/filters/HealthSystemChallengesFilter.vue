<template>
  <div class="HealthSystemChallengesFilter">
    <selector-dialog-column
      :header-selectable="true"
      :selected="catSelected"
      :header="$gettext('Select from list') | translate"
      @headerSelected="toggleAll"
    >
      <selector-dialog-category
        v-for="hsc in healthSystemChallenges"
        :key="hsc.id"
        :values="selected"
        :category="hsc"
        child-name="challenges"
        name-prop="challenge"
        always-expand-category
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
  },
  computed: {
    ...mapGetters({
      healthSystemChallenges: 'projects/getHscChallenges',
    }),
    allIds() {
      return this.healthSystemChallenges.reduce((a, c) => {
        return [...a, ...c.challenges.map((h) => h.id)]
      }, [])
    },
    catSelected(category) {
      return difference(this.allIds, this.selected).length === 0
    },
  },
  methods: {
    filterChange(value) {
      this.$emit('update:selected', [...value])
    },
    toggleAll(value) {
      if (value) {
        this.$emit('update:selected', [...this.allIds])
      } else {
        this.$emit('update:selected', [])
      }
    },
  },
}
</script>

<style></style>
