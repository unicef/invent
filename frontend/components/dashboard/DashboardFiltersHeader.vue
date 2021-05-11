<template>
  <div class="DashboardFiltersHeader">
    <span class="ProjectToShow">
      <translate :parameters="{ total }">
        {total} initiative(s) to show
      </translate>
    </span>
    <span v-if="canCopy" class="CopyUrl">
      <div v-if="!urlCopied" class="Label Button" @click="copyUrlToClipboard">
        <fa class="left" :icon="['far', 'copy']" size="lg" />
        <translate>Copy URL</translate>
      </div>
      <div v-else class="Label">
        <fa class="left" :icon="['fas', 'check-circle']" size="lg" />
        <span>Copied</span>
      </div>
    </span>
    <!-- <el-button class="ToggleFiltersButton">
      <fa icon="chevron-right" />
    </el-button> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data() {
    return {
      canCopy: false,
      urlCopied: false,
    }
  },
  computed: {
    ...mapGetters({
      total: 'dashboard/getTotal',
    }),
  },
  mounted() {
    this.canCopy = navigator.clipboard
  },
  methods: {
    async copyUrlToClipboard() {
      this.urlCopied = true
      await navigator.clipboard.writeText(window.location.href)
      setTimeout(() => {
        this.urlCopied = false
      }, 5000)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.DashboardFiltersHeader {
  background-color: @colorBrandPrimaryDark;
  transform: translateX(40px);
  position: relative;

  .ProjectToShow {
    display: inline-block;
    box-sizing: border-box;
    padding-left: 20px;
    max-width: @advancedSearchWidth - @actionBarHeight;
    color: @colorWhite;
    font-size: @fontSizeBase;
    font-weight: 700;
    line-height: @actionBarHeight;

    .svg-inline--fa {
      margin-right: 4px;
    }
  }

  .CopyUrl {
    position: absolute;
    right: 20px;
    top: 0;
    bottom: 0;
    display: inline-flex;
    align-items: center;

    .Label {
      color: @colorWhite;
      font-size: @fontSizeBase;
    }

    .Button {
      cursor: pointer;
      opacity: 0.9;
    }

    .Button:hover {
      opacity: 1;
    }

    .left {
      margin-right: 4px;
    }
  }

  .ToggleFiltersButton {
    width: @actionBarHeight;
    height: @actionBarHeight;
    padding: 0;
    border: 0;
    background-color: @colorBrandPrimaryDark;

    &:hover {
      background-color: lighten(@colorBrandPrimaryDark, 10%);
    }
  }
}
</style>
