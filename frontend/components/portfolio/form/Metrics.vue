<template>
  <div id="metrics" class="metrics-settings">
    <collapsible-card ref="collapsible" :title="$gettext('Portfolio metrics') | translate">
      <custom-required-form-item
        :error="errors.first('funding')"
        :draft-rule="draftRules.funding"
        :publish-rule="publishRules.funding"
        row
      >
        <template slot="label">
          <translate key="portfolio-name"> Funding to date (USD) </translate>
        </template>
        <el-input-number
          v-model.number="funding"
          v-validate="rules.funding"
          :rules="rules.funding"
          data-as-name="Funding"
          data-vv-name="funding"
          class="number-input"
          :min="0"
          :controls="false"
          controls-position="left"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('landscapeReview')"
        :draft-rule="draftRules.landscapeReview"
        :publish-rule="publishRules.landscapeReview"
        row
      >
        <template slot="label">
          <translate key="status"> Completed landscape review? </translate>
        </template>
        <el-radio-group
          v-model="landscapeReview"
          v-validate="rules.landscapeReview"
          data-vv-name="landscapeReview"
          data-vv-as="landscapeReview"
          class="radio-group"
        >
          <el-radio :label="true"><translate>Yes</translate></el-radio>
          <el-radio :label="false"><translate>No</translate></el-radio>
        </el-radio-group>
      </custom-required-form-item>
      <custom-required-form-item
        :error="errors.first('innovationHub')"
        :draft-rule="draftRules.innovationHub"
        :publish-rule="publishRules.innovationHub"
        row
      >
        <template slot="label">
          <translate key="status"> Innovation Hub? </translate>
        </template>
        <el-radio-group
          v-model="innovationHub"
          v-validate="rules.innovationHub"
          data-vv-name="innovationHub"
          data-vv-as="innovationHub"
          class="radio-group"
        >
          <el-radio :label="true"><translate>Yes</translate></el-radio>
          <el-radio :label="false"><translate>No</translate></el-radio>
        </el-radio-group>
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import { mapGettersActions } from '@/utilities/form'
import VeeValidationMixin from '@/components/mixins/VeeValidationMixin'
import PortfolioFieldsetMixin from '@/components/mixins/PortfolioFieldsetMixin'
import CollapsibleCard from '@/components/portfolio/CollapsibleCard'
import PortfolioSelect from '@/components/portfolio/form/inputs/PortfolioSelect'
import IconSelect from '@/components/portfolio/form/inputs/IconSelect'

export default {
  components: {
    CollapsibleCard,
    IconSelect,
    PortfolioSelect,
  },
  mixins: [VeeValidationMixin, PortfolioFieldsetMixin],
  computed: {
    ...mapGettersActions({
      funding: ['portfolio', 'getFunding', 'setFunding', 0],
      landscapeReview: ['portfolio', 'getLandscapeReview', 'setLandscapeReview', 0],
      innovationHub: ['portfolio', 'getInnovationHub', 'setInnovationHub', 0],
    }),
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      console.log('Metrics published validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('funding'),
        this.$validator.validate('landscapeReview'),
        this.$validator.validate('innovationHub'),
      ])
      console.log('Metrics draft validation', validations)
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.metrics-settings {
  .el-card {
    overflow: inherit;
  }
  .portfolio-select {
    width: 50%;
  }
  .disclaimer {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    color: @colorBrandGrayDark;
    svg {
      color: #a8a8a9;
      margin: 0 8px;
    }
    p {
      margin: 0;
      font-size: 12px;
      letter-spacing: 0;
      line-height: 18px;
    }
  }
  .radio-group {
    display: flex;
    justify-content: space-between;

    width: 250px;
    //margin: auto;
    padding-top: 8px;
  }
  .number-input {
    width: 70%;
    &.el-input-number .el-input__inner {
      text-align: left;
    }
  }
}
</style>
