<template>
  <div
    class="OrganisationItem"
  >
    <span v-if="organisation">
      {{ organisation.name }}
    </span>
    <span v-else>
      <translate>N/A</translate>
    </span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  components: {},
  props: {
    id: {
      type: [String, Number],
      default: null
    }
  },
  computed: {
    ...mapGetters({
      getOrganisationDetails: 'system/getOrganisationDetails'
    }),
    organisation () {
      if (this.id) {
        const id = parseInt(this.id, 10);
        return this.getOrganisationDetails(id);
      }
      return null;
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

</style>
