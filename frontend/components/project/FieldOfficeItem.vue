<template>
  <div class="FieldOfficeItem">
    <span v-if="selected">{{ selected.name }}</span>
    <span v-else>
      <translate>
        N/A
      </translate>
    </span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: {
      type: Number,
      default: null
    },
    country: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      open: false
    };
  },
  computed: {
    ...mapGetters({
      items: 'projects/getFieldOffices'
    }),
    filtered () {
      return this.items.filter(i => i.country_id === this.country);
    },
    selected () {
      return this.filtered.find(f => this.value === f.id);
    }
  }
};
</script>

<style lang="less">
.FieldOfficeItem {
  width: 100%;
}

</style>
