<template>
  <div class="FilterItem">
    <el-row type="flex" class="FilterItemHeader">
      <el-col class="Label">
        {{ label }}
      </el-col>
      <el-col class="Setup">
        <el-button
          type="text"
          size="small"
          class="IconLeft"
          @click="openDialog"
        >
          <span v-show="!isSelected">
            <fa icon="plus" />
            <translate>Add</translate>
          </span>
          <span v-show="isSelected">
            <fa icon="pencil-alt" />
            <translate>Edit</translate>
          </span>
        </el-button>
      </el-col>
    </el-row>

    <div class="FilterItemSelected">
      <slot />
    </div>

    <div v-show="showLimit" class="ShowMore">
      <el-button type="text" size="small" @click="openDialog">
        <translate>Show all selected...</translate>
      </el-button>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  props: {
    label: {
      type: String,
      required: true,
    },
    selected: {
      type: Array,
      default: () => [],
    },
    item: {
      type: String,
      required: true,
    },
    limit: {
      type: Number,
      default: null,
    },
  },
  computed: {
    isSelected() {
      return this.selected.length > 0
    },
    showLimit() {
      return this.limit ? this.selected.length > this.limit : false
    },
  },
  methods: {
    ...mapActions({
      setDashboardFiltersDialogState: 'layout/setDashboardFiltersDialogState',
    }),
    openDialog() {
      this.setDashboardFiltersDialogState(this.item)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.FilterItem {
  .FilterItemHeader {
    padding: 0 0 5px;

    .Label {
      width: 100%;
      font-size: @fontSizeBase;
      color: @colorTextPrimary;
    }

    .Setup {
      width: auto;
      padding-left: 10px;

      .el-button {
        padding: 0;

        .svg-inline--fa {
          position: relative;
          top: -1px;
          font-size: 10px;
        }
      }
    }
  }

  .FilterItemSelected {
    ul {
      list-style-type: none;
      margin: 2px 0 15px;
      padding: 0;
      font-size: @fontSizeSmall;

      li {
        position: relative;
        max-width: 80%;
        margin: 0 0 2px;
        padding: 0 10px 0 28px;
        line-height: 20px;
        .textTruncate();

        &:hover {
          .ListActionButton {
            + span,
            .svg-inline--fa.fa-check {
              color: @colorTextPrimary;
            }
          }
        }

        .ListActionButton {
          position: absolute;
          top: 2px;
          left: 8px;
          padding: 0;
          width: 16px;
          height: 16px;

          .svg-inline--fa {
            width: 10px;
            transition: @transitionAll;

            &.fa-check {
              color: @colorGray;
            }

            &.fa-times {
              color: @colorDanger;
            }
          }

          + span {
            color: @colorTextSecondary;
            transition: @transitionAll;
          }
        }
      }
    }
  }

  .ShowMore {
    .el-button {
      position: relative;
      top: -15px;
      margin: 0 0 0 28px;
      padding: 0;
      font-weight: 400;
    }
  }
}
</style>
