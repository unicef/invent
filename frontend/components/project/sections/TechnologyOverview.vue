<template>
  <div id="technology" class="TechnologyOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Technology overview') | translate"
      show-legend
    >
      <custom-required-form-item
        :error="errors.first('implementation_dates')"
        :draft-rule="draftRules.implementation_dates"
        :publish-rule="publishRules.implementation_dates"
      >
        <template slot="label">
          <translate key="implementation_dates">
            When will the technology be first deployed?
          </translate>
        </template>

        <SafeDatePicker
          v-model="implementation_dates"
          v-validate="rules.implementation_dates"
          :placeholder="$gettext('Pick a day') | translate"
          data-vv-name="implementation_dates"
          data-vv-as="Implementation dates"
          class="Date"
          align="left"
        />
      </custom-required-form-item>
      <custom-required-form-item
        :error="errors.first('licenses')"
        :draft-rule="draftRules.licenses"
        :publish-rule="publishRules.licenses"
      >
        <template slot="label">
          <translate key="licenses">
            Under what license is the project governed?
          </translate>
        </template>
        <license-selector
          v-model="licenses"
          v-validate="rules.licenses"
          data-vv-name="licenses"
          data-vv-as="License"
        />
      </custom-required-form-item>
      <custom-required-form-item
        :error="errors.first('repository')"
        :draft-rule="draftRules.repository"
        :publish-rule="publishRules.repository"
      >
        <template slot="label">
          <translate key="repository">
            Can you provide a link to code documentation?
          </translate>
        </template>

        <character-count-input
          v-model="repository"
          v-validate="rules.repository"
          class="LinkField"
          :rules="rules.repository"
          type="text"
          placeholder="http://"
          data-vv-name="repository"
          data-vv-as="Repository"
        />
      </custom-required-form-item>
      <custom-required-form-item
        :error="errors.first('mobile_application')"
        :draft-rule="draftRules.mobile_application"
        :publish-rule="publishRules.mobile_application"
      >
        <template slot="label">
          <translate key="mobile_application">
            Can you provide a link to a demo of the application?
          </translate>
        </template>

        <character-count-input
          v-model="mobile_application"
          v-validate="rules.mobile_application"
          class="LinkField"
          :rules="rules.mobile_application"
          type="text"
          placeholder="http://"
          data-vv-name="mobile_application"
          data-vv-as="Mobile application"
        />
      </custom-required-form-item>
      <custom-required-form-item
        :error="errors.first('wiki')"
        :label="$gettext('Link to the wiki page') | translate"
        :draft-rule="draftRules.wiki"
        :publish-rule="publishRules.wiki"
      >
        <template slot="label">
          <translate key="wiki">
            Can you provide a link to the software wikipage?
          </translate>
        </template>

        <character-count-input
          v-model="wiki"
          v-validate="rules.wiki"
          class="LinkField"
          :rules="rules.wiki"
          type="text"
          placeholder="http://"
          data-vv-name="wiki"
          data-vv-as="Wiki"
        />
      </custom-required-form-item>
    </collapsible-card>
  </div>
</template>

<script>
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'

import { mapGettersActions } from '../../../utilities/form'
import CollapsibleCard from '../CollapsibleCard'
import LicenseSelector from '../LicenseSelector'

export default {
  components: {
    CollapsibleCard,
    LicenseSelector,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGettersActions({
      implementation_dates: [
        'project',
        'getImplementationDates',
        'setImplementationDates',
        0,
      ],
      licenses: ['project', 'getLicenses', 'setLicenses', 0],
      repository: ['project', 'getRepository', 'setRepository', 0],
      mobile_application: [
        'project',
        'getMobileApplication',
        'setMobileApplication',
        0,
      ],
      wiki: ['project', 'getWiki', 'setWiki', 0],
    }),
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.TechnologyOverview {
  .Date {
    width: 50% !important;
  }
}
</style>
