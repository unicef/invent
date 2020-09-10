<template>
  <div
    id="categorization"
    class="GeneralOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Categorization') | translate"
      show-legend
    >
      <el-row
        :gutter="20"
        type="flex"
      >
        <el-col :span="24">
          <custom-required-form-item
            :error="errors.first('unicef_sector')"
            :draft-rule="draftRules.unicef_sector"
            :publish-rule="publishRules.unicef_sector"
          >
            <template slot="label">
              <translate key="sector-label">
                UNICEF Sector
              </translate>
<!--              <form-hint>-->
<!--                <translate key="implementation-overview-hint">-->
<!--                  Describe your overall digital health project design.-->
<!--                </translate>-->
<!--              </form-hint>-->
            </template>

            <multi-selector
              v-model="unicef_sector"
              v-validate="rules.unicef_sector"
              data-vv-name="unicef_sector"
              data-vv-as="UNICEF Sector"
              source="getSectors"
            />
            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>
                  Please select the sector(s) the initiative serves.
                </translate>
              </p>
            </span>
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
import MultiSelector from '@/components/project/MultiSelector';
// import FormHint from '../FormHint';
import { mapGettersActions } from '../../../utilities/form';
import { mapGetters } from 'vuex';

export default {
  components: {
    CollapsibleCard,
    MultiSelector
    // FormHint
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified'
    }),
    ...mapGettersActions({
      unicef_sector: ['project', 'getSectors', 'setSectors', 0]
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
        this.$validator.validate('unicef_sector')
      ]);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
</style>
