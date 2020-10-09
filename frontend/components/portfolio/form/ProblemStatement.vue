<template>
  <div id="general" class="ProblemStatement">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Problem Statements') | translate"
    >
      <statements />
    </collapsible-card>
  </div>
</template>

<script>
import CollapsibleCard from '@/components/portfolio/CollapsibleCard'
import Statements from '@/components/portfolio/form/inputs/Statements'

export default {
  components: {
    CollapsibleCard,
    Statements,
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      console.log('General settings published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('statements'),
      ])
      console.log('General settings draft validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
