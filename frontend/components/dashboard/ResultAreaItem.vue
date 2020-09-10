<template>
  <div :class="`ResultAreaItem ${selected === 'N/A' && 'muted'}`">
    {{ selected }}
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    value: {
      type: Number,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      items: "projects/getResultAreas"
    }),
    selected() {
      const found = this.items.find(i => i.id === this.value);
      return found ? found.name : "N/A";
    }
  }
};
</script>

<style lang="less" scoped>
.ResultAreaItem {
  width: 100%;
}
.muted {
  color: #a8a8a9;
}
</style>
