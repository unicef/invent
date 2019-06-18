<template>
  <div class="FormHint">
    <div class="Trigger">
      <slot /> <fa
        class="HintToggle"
        icon="question-circle"
        @click="show = !show"
      />
    </div>
    <transition name="el-zoom-in-top">
      <div
        v-if="show"
        class="Hint"
      >
        <slot name="hint" />
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data () {
    return {
      show: false
    };
  }
};
</script>

<style lang="less" scoped>
.FormHint {
  display: inline-flex;
  flex-flow: row wrap;

  .HintToggle {
    cursor: pointer;
   }

  .Hint {
    margin-top: -10px;
  }

}

</style>
