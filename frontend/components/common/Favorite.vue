<template>
  <p class="heart">
    <template v-if="favorite">
      <el-tooltip
        :content="$gettext('Remove from Favorites') | translate"
        placement="bottom"
      >
        <fa
          class="heart-full"
          :icon="['fas', 'heart']"
          @click="removeFavorite({ id, type })"
        />
      </el-tooltip>
    </template>
    <template v-else>
      <el-tooltip
        :content="$gettext('Add to favorites') | translate"
        placement="bottom"
      >
        <fa
          class="heart-empty"
          :icon="['far', 'heart']"
          @click="addFavorite({ id, type })"
        />
      </el-tooltip>
    </template>
  </p>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
    favorite: {
      type: Boolean,
      required: true,
    },
    type: {
      type: String,
      default: 'detail',
    },
  },
  methods: {
    ...mapActions({
      addFavorite: 'projects/addFavorite',
      removeFavorite: 'projects/removeFavorite',
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';

.heart {
  margin: 10px 2px 0 0;
  float: right;
  .heart-full {
    cursor: pointer;
    color: #c4225f;
  }
  .heart-empty {
    cursor: pointer;
    color: @colorBrandGrayLight;
  }
}
</style>
