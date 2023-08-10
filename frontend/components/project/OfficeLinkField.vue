<template>
  <div class="SimpleField">
    <div class="Header">
      <template v-if="header">
        {{ header }}
      </template>
    </div>
    <div class="Content">
      <span>{{ office }}</span>
      <nuxt-link
        data-test="published-country-homepage-link"
        :to="
          localePath({
            name: 'organisation',
            params: { organisation: `${country.code}` },
            query: { ...this.$route.query },
          })
        "
      >
        {{ country.name }}
      </nuxt-link>
      <span>{{ `,  ${region}` }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    header: {
      type: String,
      default: null,
    },
    office: {
      type: String,
      default: null,
    },
    country: {
      type: Object,
      default: null,
    },
    region: {
      type: String,
      default: null,
    },
  },
}
</script>

<style></style>
