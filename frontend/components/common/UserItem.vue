<template>
  <div
    v-if="user"
    class="UserItem"
  >
    <span class="Name">
      {{ user.name }}
    </span>
    <span
      v-if="showOrganisation"
      class="Organisation"
    >
      <organisation-item :id="user.organisation" />
    </span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import OrganisationItem from '../common/OrganisationItem';

export default {
  components: {
    OrganisationItem
  },
  props: {
    id: {
      type: Number,
      default: null
    },
    showOrganisation: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      getUserDetails: 'system/getUserProfileDetails'
    }),
    user () {
      if (this.id) {
        return this.getUserDetails(this.id);
      }
      return null;
    }
  }
};
</script>

<style lang="less">

.UserItem {
  .Organisation {
    font-size: 12px;
  }
}

</style>
