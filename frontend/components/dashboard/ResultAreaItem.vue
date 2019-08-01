<template>
  <div class="ResultAreaItem">
    {{ selected }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: {
    value: {
      type: Number,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      items: 'projects/getResultAreas'
    }),
    selected () {
      const found = this.items.find(i => i.id === this.value);
      return found ? found.name : 'N/A';
    }
  }
};
</script>

<style lang="less">
.ResultAreaItem {
  width: 100%;
}
</style>
