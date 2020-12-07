<template>
  <lazy-el-select
    :value="selected"
    :placeholder="$gettext('Select from list') | translate"
    popper-class="PlatformSelectorDropdown"
    class="PlatformSelector"
    value-key="id"
    :filter-method="filter"
    v-bind="{ ...$attrs, ...$props }"
    @change="changeHandler"
    @blur="$emit('blur')"
  >
    <el-option
      v-if="newItem"
      :key="newItem.id"
      :label="newItem.name"
      :value="newItem.id"
      class="new"
    >
      <span class="left">
        <b>{{ newItem.name }}</b>
      </span>
      <span class="left">
        <small>{{ newInfoTitle }}</small>
      </span>
      <span class="right">
        <b>
          <fa icon="plus-circle" />
          <translate>Add as new</translate>
        </b>
      </span>
    </el-option>
    <el-option
      v-for="item in availableItems"
      :key="item.id"
      :label="item.name"
      :value="item.id"
      :class="`${item.state === 2 ? 'requested' : ''}`"
    >
      <template v-if="item.state === 1">
        {{ item.name }}
      </template>
      <template v-if="item.state === 2">
        <span class="left">
          <b>{{ item.name }}</b>
        </span>
        <span class="right">
          <small>
            <fa icon="exclamation-triangle" />
            <translate>Requested, please wait for approval</translate>
          </small>
        </span>
      </template>
    </el-option>
  </lazy-el-select>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  model: {
    prop: 'items',
    event: 'change',
  },
  props: {
    items: {
      type: [Array, Number],
      required: true,
    },
    options: {
      type: Array,
      required: true,
    },
    source: {
      type: String,
      required: true,
    },
    newInfoTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      newItem: null,
      availableItems: [],
    }
  },
  computed: {
    selected() {
      return 'multiple' in this.$attrs ? [...this.items] : this.items[0]
    },
  },
  mounted() {
    const options = this.options
    this.availableItems = options.sort((a, b) => a.name.localeCompare(b.name))
  },
  methods: {
    ...mapActions({
      setNewItem: 'projects/setNewItem',
    }),
    async changeHandler(value) {
      // get a new item
      let newItem = Array.isArray(value) ? value[value.length - 1] : value
      if (typeof newItem === 'string') {
        // try to add new item
        const result = await this.setNewItem({
          type: this.source,
          name: newItem,
        })
        newItem = typeof result === 'number' ? [result] : []
        'multiple' in this.$attrs
          ? this.$emit('change', [...value.slice(0, -1), ...newItem])
          : this.$emit('change', [...newItem])
      } else {
        // handle regular change
        'multiple' in this.$attrs
          ? this.$emit('change', [...value])
          : this.$emit('change', [value])
      }
    },
    filter(value) {
      this.availableItems = this.options.filter((item) =>
        item.name.toLowerCase().includes(value.toLowerCase())
      )
      if (value) {
        this.newItem = { id: value, name: value }
      } else {
        this.newItem = null
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.PlatformSelector {
  width: 100%;
}

.el-select-dropdown__item {
  &.requested {
    background-color: #fffbdd !important;
    .left {
      float: left;
      width: 60%;
      overflow: hidden;
    }
    .right {
      float: right;
      overflow: hidden;
      color: @colorTextMuted;
      font-size: 10px;
      margin-top: 0px;
      margin-right: 20px;
      svg {
        color: #f8a72a;
        margin-right: 6px;
      }
    }
  }
  &.new {
    background-color: #fff8c4;
    padding-top: 5px;
    height: 58px;
    .left {
      float: left;
      width: 70%;
      height: 16px;
    }
    .right {
      float: right;
      // width: 25%;
      color: @colorBrandPrimary;
      font-size: 13px;
      margin-top: -7px;
      svg {
        margin-right: 10px;
      }
    }
  }
}
</style>
