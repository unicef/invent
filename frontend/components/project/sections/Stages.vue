<template>
  <div
    id="general"
    class="GeneralOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Stages') | translate"
      show-legend
    >
      <el-row
        :gutter="20"
        type="flex"
      >
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('phase')"
            :draft-rule="draftRules.phase"
            :publish-rule="publishRules.phase"
          >
            <template slot="label">
              <translate key="phase-label">
                Please select which phase the inititiave has reached to date.
              </translate>
            </template>

            <single-select
              v-model="phase"
              v-validate="rules.phase"
              data-vv-name="phase"
              data-vv-as="Phase of Initiative"
              source="projects/getPhases"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js';
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js';
import CollapsibleCard from '../CollapsibleCard';
import SingleSelect from '@/components/common/SingleSelect';
import { mapGettersActions } from '../../../utilities/form';
import { mapGetters } from 'vuex';

export default {
  components: {
    CollapsibleCard,
    SingleSelect
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified'
    }),
    ...mapGettersActions({
      phase: ['project', 'getPhase', 'setPhase', 0]
    })
  },
  methods: {
    async validate () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate()
      ]);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft () {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate('phase')
      ]);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";
</style>
