<template>
  <div
    :value="innerValue"
    v-bind="{ ...$props, ...$attrs }"
    class="icon-select"
    v-on="{ ...$listeners }"
  >
    <div v-if="!$attrs.value" class="dropdown" @click="open = true">
      <span><translate>Choose icon</translate></span>
      <fa icon="sort-down" />
    </div>
    <div v-else class="selected">
      <div class="close" @click="handleRemoveIcon">
        <fa icon="times" />
      </div>
      <div class="icon">
        <span :class="`icon-tiip-${$attrs.value.icon}`">
          <template v-if="path($attrs.value.icon)">
            <span class="path1" /><span class="path2" />
          </template>
        </span>
      </div>
    </div>
    <div v-if="open" class="select">
      <div class="icons">
        <div
          v-for="item in items"
          :key="item.id"
          class="icon"
          @click="handleDropdownClick(item)"
        >
          <span :class="`icon-tiip-${item.icon}`">
            <template v-if="path(item.icon)">
              <span class="path1" /><span class="path2" />
            </template>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'change',
  },
  data() {
    return {
      open: false,
    }
  },
  computed: {
    ...mapState({
      items: (state) => state.portfolio.icons,
    }),
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
  },
  mounted() {},
  methods: {
    handleDropdownClick(val) {
      this.innerValue = val
      this.open = false
    },
    handleRemoveIcon() {
      this.innerValue = null
    },
    path(icon) {
      // check if the typography needs path drawing
      return icon === 'breast_feeding' || icon === 'mother_and_baby'
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.icon-select {
  position: relative;
  .dropdown {
    display: flex;
    align-items: baseline;
    cursor: pointer;
    color: @colorBrandPrimary;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;
    margin-top: 10px;
    svg {
      margin-left: 6px;
    }
  }
  .icon {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .selected {
    position: relative;
    height: 62px;
    width: 62px;
    .close {
      position: absolute;
      top: -10px;
      right: -10px;
      height: 24px;
      width: 24px;
      background-color: @colorWhite;
      color: @colorDanger;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.18);
      -webkit-border-radius: 20px;
      -moz-border-radius: 20px;
      border-radius: 20px;
      cursor: pointer;
      svg {
        margin: 5px 7px;
      }
    }
    .icon {
      box-sizing: border-box;
      height: 62px;
      width: 62px;
      border: 1px solid #eae6e1;
      background-color: #f5f3ef;
      color: @colorBrandPrimary;
      span {
        font-size: 40px;
      }
    }
  }
  .select {
    position: absolute;
    top: 0;
    z-index: 100;
    height: 301px;
    width: 274px;
    background-color: @colorWhite;
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.18);
    overflow: hidden;
    overflow-y: scroll;
  }
  .icons {
    display: flex;
    flex-wrap: wrap;
    padding: 10px;
    .icon {
      height: 78px;
      width: 82px;
      background-color: @colorWhite;
      cursor: pointer;
      span {
        font-size: 50px;
      }
      &:hover {
        background-color: #e8f6fd;
      }
    }
  }
}
</style>
