<template>
  <lazy-el-select
    :value="value"
    :placeholder="$gettext('Select from list') | translate"
    multiple
    filterable
    popper-class="HealthSystemChallengesSelectorDropdown"
    class="HealthSystemChallengesSelector"
    @change="changeHandler"
  >
    <el-option-group
      v-for="group in healthSystemChallenges"
      :key="group.id"
      :label="group.name"
    >
      <el-option
        v-for="hsc in group.challenges"
        :key="hsc.id"
        :label="hsc.challenge"
        :value="hsc.id"
      />
    </el-option-group>
  </lazy-el-select>
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
      type: Array,
      default: null
    }
  },
  computed: {
    ...mapGetters({
      healthSystemChallenges: 'projects/getHscChallenges'
    })
  },
  methods: {
    changeHandler (value) {
      this.$emit('change', value);
    }
  }
};
</script>

<style lang="less">
.HealthSystemChallengesSelector {
  width: 100%;
}
.HealthSystemChallengesSelectorDropdown {

}
</style>
