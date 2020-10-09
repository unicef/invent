<template>
  <div id="general" class="GeneralOverview">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Focal point overview') | translate"
      show-legend
    >
      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('contact_name')"
            :draft-rule="draftRules.contact_name"
            :publish-rule="publishRules.contact_name"
          >
            <template slot="label">
              <translate key="contact-name">
                Programme Focal Point Name
              </translate>
              <form-hint>
                <translate key="contact-name-hint">
                  This is the individual who will be the lead point of contact
                  for any queries through the DHA.
                </translate>
              </form-hint>
            </template>

            <character-count-input
              v-model="contact_name"
              v-validate="rules.contact_name"
              :rules="rules.contact_name"
              data-vv-name="contact_name"
              data-vv-as="Contact name"
            />
          </custom-required-form-item>
        </el-col>
        <el-col :span="12">
          <custom-required-form-item
            :error="errors.first('contact_email')"
            :draft-rule="draftRules.contact_email"
            :publish-rule="publishRules.contact_email"
          >
            <template slot="label">
              <translate key="contact-email">
                Programme Focal Point Email
              </translate>
            </template>

            <character-count-input
              v-model="contact_email"
              v-validate="rules.contact_email"
              :rules="rules.contact_email"
              data-vv-name="contact_email"
              data-vv-as="Contact email"
            />
          </custom-required-form-item>
        </el-col>
      </el-row>
    </collapsible-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import VeeValidationMixin from '../../mixins/VeeValidationMixin.js'
import ProjectFieldsetMixin from '../../mixins/ProjectFieldsetMixin.js'
import CollapsibleCard from '../CollapsibleCard'
import FormHint from '../FormHint'
import { mapGettersActions } from '../../../utilities/form'

export default {
  components: {
    CollapsibleCard,
    FormHint,
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified',
    }),
    ...mapGettersActions({
      contact_name: ['project', 'getContactName', 'setContactName', 0],
      contact_email: ['project', 'getContactEmail', 'setContactEmail', 0],
    }),
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([this.$validator.validate()])
      return validations.reduce((a, c) => a && c, true)
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard()
      const validations = await Promise.all([
        this.$validator.validate('contact_email'),
      ])
      return validations.reduce((a, c) => a && c, true)
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
