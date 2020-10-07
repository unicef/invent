<template>
  <div class="StandardsList">
    <ul>
      <li v-for="link in selected" :key="link.id">
        <div class="Label">
          {{ link.label }}
        </div>
        <simple-field :content="link.link" link />
      </li>
      <li v-show="selected.length === 0">
        <translate>N/A</translate>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleField from './SimpleField'

export default {
  components: {
    SimpleField,
  },
  props: {
    value: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    ...mapGetters({
      interoperabilityLinks: 'projects/getInteroperabilityLinks',
    }),
    selected() {
      const result = []
      this.interoperabilityLinks.forEach((il) => {
        const selected = { ...this.value[il.id] }
        if (selected && selected.link) {
          selected.id = il.id
          selected.label = `${il.pre} ${il.name}`
          result.push(selected)
        }
      })
      return result
    },
  },
}
</script>

<style lang="less">
.StandardsList {
  width: 100%;
}
</style>
