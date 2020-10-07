<template>
  <lazy-el-select
    :disabled="filtered.length === 0"
    :value="value"
    :placeholder="$gettext('Select from list') | translate"
    filterable
    clearable
    popper-class="FieldOfficeDropdown"
    class="FieldOffice"
    @change="changeHandler"
  >
    <el-option
      v-for="item in filtered"
      :key="item.id"
      :label="item.name"
      :value="item.id"
    />
  </lazy-el-select>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [Number, String],
      default: null,
    },
    office: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      open: false,
    }
  },
  computed: {
    ...mapGetters({
      items: 'projects/getFieldOffices',
    }),
    filtered() {
      return this.items.filter((i) => i.country_office_id === this.office)
    },
  },
  methods: {
    changeHandler(value) {
      this.$emit('change', value)
    },
    toggleHandler(value) {
      if (value) {
        this.open = value
      }
    },
  },
}
</script>

<style lang="less">
.FieldOffice {
  width: 100%;
}
</style>
