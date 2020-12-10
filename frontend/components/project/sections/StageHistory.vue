<template>
  <div id="stages" class="graph">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('4. Completion of initiative stages') | translate"
    >
      <c-stages v-if="stages" />
      <div v-else class="NoData">
        <div class="SimpleField">
          <div class="Header">
            <translate> No Data available </translate>
          </div>
        </div>
      </div>
    </collapsible-card>
  </div>
</template>

<script>
import cStages from '@/components/common/chart/cStages'
import CollapsibleCard from '@/components/project/CollapsibleCard'

export default {
  components: {
    CollapsibleCard,
    cStages,
  },
  computed: {
    stages() {
      return this.$store.getters['project/getStages']
    },
  },
}
</script>

<style lang="less">
.graph {
  // outside modifiers
  .CollapsibleCard .ContentContainer {
    padding: 0;
  }
}
.NoData {
  padding: 22px 74px 0px 40px;
}
</style>
