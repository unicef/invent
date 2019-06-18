<template>
  <div class="licensesList">
    <ul>
      <li
        v-for="license in selected"
        :key="license.id"
      >
        {{ license.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  props: {
    value: {
      type: Array,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      licenses: 'projects/getLicenses'
    }),
    selected () {
      return this.licenses.filter(hfa => this.value.includes(hfa.id));
    }
  }
};
</script>

<style lang="less">
.licensesList {
  width: 100%;
}
</style>
