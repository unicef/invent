<template>
  <div :class="['SelectorDialogCategory', {'NoParent': !hideHeader && !alwaysExpandCategory}]">
    <div
      v-show="!hideHeader"
      :class="['CategoryName', {'Opened': categoryToggled}]"
    >
      <el-button
        type="text"
        @click="toggleCategory"
      >
        <fa
          v-show="!categoryToggled && !alwaysExpandCategory"
          icon="angle-down"
        />
        <fa
          v-show="categoryToggled && !alwaysExpandCategory"
          icon="angle-up"
        />
        <el-checkbox
          v-show="categorySelectable"
          :value="headerChecked"
          @change="selectAllCategory"
        />
        <span>{{ category.name }}</span>
      </el-button>
    </div>

    <transition name="slide-fade">
      <div
        v-show="categoryShown"
        role="group"
        class="el-checkbox-group Items OnePerRow"
      >
        <el-checkbox
          v-for="item in items"
          :key="item.id"
          :value="values.includes(item.id)"
          class="Item"
          @change="filterChange(item.id)"
        >
          {{ getItemName(item) }}
        </el-checkbox>
      </div>
    </transition>
  </div>
</template>

<script>

export default {
  model: {
    prop: 'values',
    event: 'change'
  },
  props: {
    categorySelectable: {
      type: Boolean,
      required: false,
      default: false
    },
    category: {
      type: [Object, Array],
      required: true
    },
    childName: {
      type: String,
      default: null
    },
    values: {
      type: Array,
      required: true
    },
    nameProp: {
      type: String,
      default: 'name'
    },
    hideHeader: {
      type: Boolean,
      default: false
    },
    alwaysExpandCategory: {
      type: Boolean,
      default: false
    },
    expandCollapse: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      categoryToggled: false
    };
  },
  computed: {
    categoryShown () {
      return this.hideHeader || this.categoryToggled || this.alwaysExpandCategory;
    },
    items () {
      if (this.childName) {
        return this.category[this.childName];
      }
      return this.category;
    },
    headerChecked () {
      return this.items.reduce((c, n) => {
        return c && this.values.includes(n.id);
      }, true);
    }
  },
  methods: {
    filterChange (item) {
      if (this.values.includes(item)) {
        this.$emit('change', this.values.filter(v => v !== item));
      } else {
        this.$emit('change', [...this.values, item]);
      }
    },
    toggleCategory () {
      this.categoryToggled = !this.categoryToggled;
    },
    selectAll () {
      this.$emit('change', [...this.values, ...this.items.map(i => i.id)]);
    },
    deSelectAll () {
      this.$emit('change', this.values.filter(v => !this.items.map(i => i.id).includes(v)));
    },
    selectAllCategory () {
      this.categoryToggled = true;
      if (!this.headerChecked) {
        this.selectAll();
      } else {
        this.deSelectAll();
      }
    },
    getItemName (item) {
      return item[this.nameProp];
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

.SelectorDialogCategory {
  .CategoryName {

    &.Opened {
      .el-button {
        color: @colorTextPrimary;
      }
    }

    .el-button {
      line-height: 19px;
      text-align: left;
      color: @colorTextSecondary;

      > span {
        display: inline-flex;
      }

      &:hover {
        color: @colorTextPrimary;
      }

      .svg-inline--fa {
        width: 12px;
        margin-top: 2px;
      }

      .el-checkbox {
        margin: 0 10px 0 15px;

        &.is-checked {
          + span {
            color: @colorBrandPrimary;
          }
        }

        + span {
          white-space: normal;
        }
      }
    }
  }

  .Items {
    margin-bottom: 10px;
    padding: 0 20px 0 50px;

    .Item {
      display: block;
      margin: 0;
    }
  }

  .slide-fade-enter-active {
    transition: all .1s ease;
  }

  .slide-fade-leave-active {
    transition: all .1s cubic-bezier(1.0, 0.5, 0.8, 1.0);
  }

  .slide-fade-enter, .slide-fade-leave-to
  /* .slide-fade-leave-active below version 2.1.8 */ {
    transform: translateY(-10px);
    opacity: 0;
  }
}

</style>
