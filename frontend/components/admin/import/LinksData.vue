<template>
  <div>
    <div v-for="(linkType, index) in getLinkTypes" :key="linkType.name">
      <div slot="label">{{ linkType.name }} URL</div>
      <character-count-input
        :value="getLinkWebsite(index)"
        @input="setLinkWebsite($event, index)"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import findIndex from 'lodash/findIndex'
import find from 'lodash/find'

export default {
  name: 'LinksData',
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      getLinkTypes: 'system/getLinkTypes',
    }),
    links: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('update:value', val)
      },
    },
  },
  methods: {
    setLinkWebsite(url, index) {
      const links = [...this.links]
      const linkIndex = findIndex(links, (l) => l.link_type === index)
      const data = {
        link_url: url,
        link_type: index,
      }
      if (linkIndex !== -1) {
        links[linkIndex] = data
      } else {
        links.push(data)
      }
      this.links = links
    },
    getLinkWebsite(index) {
      const link = find(this.links, (l) => l.link_type === index)
      return link ? link.link_url : ''
    },
  },
}
</script>

<style scoped></style>
