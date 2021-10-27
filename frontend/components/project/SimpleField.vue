<template>
  <div class="SimpleField">
    <div class="Header">
      <template v-if="header">
        {{ header }}
      </template>
      <template v-if="!header">
        <slot name="header" />
      </template>
    </div>
    <div v-show="!missingContent" class="Content">
      <template v-if="showContent">
        <span v-if="!link">
          {{ processedContent }}
        </span>
        <a v-if="link" :href="content" target="_blank" class="TextLink">
          {{ evenLines }}
        </a>
      </template>
      <template v-if="!showContent">
        <slot />
      </template>
    </div>
    <div v-show="missingContent" class="Empty">
      <!-- N/A -->
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns'
import { isNumber } from 'lodash'

export default {
  props: {
    header: {
      type: String,
      default: null,
    },
    content: {
      type: [String, Number, Date],
      default: null,
    },
    date: {
      type: Boolean,
      default: false,
    },
    link: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    showContent() {
      return this.content !== null && this.content !== undefined
    },
    missingContent() {
      return !this.$slots.default && !this.content
    },
    processedContent() {
      if (this.date) {
        return format(this.content, 'DD/MM/YYYY')
      }
      var resultContent = this.content
      if (isNumber(this.content)){
        resultContent = this.$options.filters.formatNumber(this.content)
      }
      return resultContent
    },
    evenLines() {
      return this.content.match(/.{1,102}/g).join('\n')
    },
  },
}
</script>

<style></style>
