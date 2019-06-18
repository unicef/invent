<template>
  <div>
    <l-marker
      v-if="icon"
      :options="pin.options"
      :lat-lng="pin.latlng"
      :icon="icon"
      class="MapMarker"
      @click="emitMarkerClick"
    />
  </div>
</template>

<script>

export default {
  components: {
  },
  props: {
    pin: {
      type: Object,
      required: true
    },
    icon: {
      type: Object,
      required: false,
      default: null
    }
  },
  data () {
    return {};
  },
  methods: {
    emitMarkerClick () {
      this.$emit('marker-click', this.pin.id);
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

    .CountryViewBtn {}
    .MouseEventSpy {}
</style>
