<template>
  <div>
    <div v-if="errors" class="GlobalErrors">
      <el-tag v-for="error in errors" :key="error" type="danger">
        <fa icon="exclamation" />
        {{ error }}
      </el-tag>
    </div>
    <slot
      :rules="validationRules"
      :globalErrors="errors"
      :nameMapping="nameMapping"
    />
  </div>
</template>

<script>
import { draftRules, publishRules } from '@/utilities/projects'
import { nameMapping } from '@/utilities/import'
export default {
  props: {
    headers: {
      type: Array,
      default: () => [],
    },
    publish: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    internalDraftRules() {
      return { ...draftRules() }
    },
    internalPublishRules() {
      const standardRules = publishRules()
      return {
        ...standardRules,
        strategies: undefined,
        digitalHealthInterventions: standardRules.strategies,
        ...standardRules.national_level_deployment,
      }
    },
    validationRules() {
      const rules = this.publish
        ? this.internalPublishRules
        : this.internalDraftRules
      return {
        ...rules,
        team: undefined,
        viewers: undefined,
        country: undefined,
        country_office: undefined,
        donors: undefined,
      }
    },
    nameMapping() {
      return {
        ...nameMapping,
      }
    },
    errors() {
      const result = []
      const draftRequireds = []
      for (const key in this.validationRules) {
        const rule = this.validationRules[key]
        if (
          rule &&
          rule.required &&
          key.substr(0, 8) !== 'partner_' &&
          key.substr(0, 5) !== 'link_'
        ) {
          draftRequireds.push(key)
        }
      }
      draftRequireds.forEach((dr) => {
        if (!this.headers.some((h) => h.selected === dr)) {
          const name = this.nameMapping[dr] || dr
          result.push(`Please select ${name} column`)
        }
      })
      return result
    },
  },
}
</script>

<style></style>
