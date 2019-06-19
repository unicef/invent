<template>
  <div class="DigitalHealthInterventionsSelector">
    <el-button
      v-show="dhi.length === 0"
      class="IconLeft"
      @click="openDialog"
    >
      <fa icon="plus" />
      <translate>Add Digital Health Interventions</translate>
    </el-button>
    <div
      v-show="dhi.length > 0"
      class="HasSelectedItems"
    >
      <ul class="SelectedDigitalHealthInterventions">
        <li
          v-for="item in dhi"
          :key="item.id"
        >
          <fa
            icon="check"
            size="xs"
          />
          <digital-health-intervention-item :id="item" />
        </li>
      </ul>
      <el-button
        class="IconLeft"
        @click="openDialog"
      >
        <fa icon="edit" />
        <translate>Edit selection</translate>
      </el-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import DigitalHealthInterventionItem from '../common/DigitalHealthInterventionItem';

export default {
  components: {
    DigitalHealthInterventionItem
  },
  $_veeValidate: {
    value () {
      return this.dhi;
    },
    events: 'change'
  },
  computed: {
    ...mapGetters({
      dhi: 'project/getDigitalHealthInterventions'
    })
  },
  watch: {
    dhi: {
      immediate: true,
      deep: true,
      handler () {
        this.$emit('change');
      }
    }
  },
  methods: {
    ...mapActions({
      setDigitalHealthInterventionsDialogState: 'layout/setDigitalHealthInterventionsDialogState'
    }),
    openDialog () {
      this.setDigitalHealthInterventionsDialogState(true);
    }
  }
};
</script>

<style lang="less">
  @import "../../assets/style/variables.less";
  @import "../../assets/style/mixins.less";

  .DigitalHealthInterventionsSelector {
    .el-button {
      margin-bottom: 10px;
    }

    ul.SelectedDigitalHealthInterventions {
      list-style-type: none;
      display: block;
      margin: 0 0 30px;
      padding: 0;

      li {
        position: relative;
        margin-bottom: 20px;
        padding-left: 22px;
        line-height: 19px;
        color: @colorBrandPrimary;

        .svg-inline--fa {
          position: absolute;
          top: 4px;
          left: 0;
        }
      }
    }
  }
</style>
