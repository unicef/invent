<template>
  <div
    id="partners"
    class="GeneralOverview"
  >
    <collapsible-card
      ref="collapsible"
      :title="$gettext('Partners') | translate"
      show-legend
    >
      <el-row
        v-for="(partner, index) in partners"
        :key="index"
      >
        <el-col :span="16">
          <custom-required-form-item>
            <template slot="label">
              <translate key="partners">
                Please select all partner types involved with the initiative.
              </translate>
            </template>
            <single-select
              :value="partner ? partner.partner_type : null"
              :reject="selectedType(partner ? partner.partner_type : null)"
              data-vv-name="partnerType"
              data-vv-as="Partner Type"
              source="system/getPartnerTypes"
              @change="setPartnerItem(index, 'partner_type', $event)"
            />
          </custom-required-form-item>
        </el-col>
        <el-col
          :span="8"
          class="btContainer"
        >
          <add-rm-buttons
            :show-add="isLastAndExist(partners, index)"
            :show-rm="partners.length > 1"
            @add="addPartner"
            @rm="rmPartner(index)"
          />
        </el-col>
        <el-col
          v-if="partners[index]"
          :span="24"
        >
          <custom-required-form-item
            :error="errors.first('partner_name')"
            :draft-rule="draftRules.partner_name"
            :publish-rule="publishRules.partner_name"
          >
            <template slot="label">
              <translate key="partner_name">
                Please provide the name(s) of your partner(s).
              </translate>
            </template>

            <character-count-input
              v-validate="rules.partner_name"
              :value="partner.partner_name"
              :rules="rules.partner_name"
              data-vv-name="partner_name"
              data-vv-as="Partner Name"
              @input="setPartnerItem(index, 'partner_name' ,$event)"
            />
          </custom-required-form-item>
          <custom-required-form-item
            :error="errors.first('partner_email')"
            :draft-rule="draftRules.partner_email"
            :publish-rule="publishRules.partner_email"
          >
            <template slot="label">
              <translate key="partner_email">
                Contact Email
              </translate>
            </template>

            <character-count-input
              v-validate="rules.partner_email"
              :value="partner.partner_email"
              :rules="rules.partner_email"
              data-vv-name="partner_email"
              data-vv-as="Partner Email"
              @input="setPartnerItem(index, 'partner_email' ,$event)"
            />
          </custom-required-form-item>
          <custom-required-form-item
            :error="errors.first('partner_website')"
            :draft-rule="draftRules.partner_website"
            :publish-rule="publishRules.partner_website"
          >
            <template slot="label">
              <translate key="partner_website">
                Partner Website
              </translate>
            </template>

            <character-count-input
              v-validate="rules.partner_website"
              :value="partner.partner_website"
              :rules="rules.partner_website"
              data-vv-name="partner_website"
              data-vv-as="Partner Website"
              @input="setPartnerItem(index, 'partner_website' ,$event)"
            />

            <span class="Hint">
              <fa icon="info-circle" />
              <p>
                <translate>URL format: https://invent.unicef.org</translate>
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
import AddRmButtons from '@/components/project/AddRmButtons';
import SingleSelect from '@/components/common/SingleSelect';
import { mapGettersActions } from '../../../utilities/form';
import { mapGetters } from 'vuex';

export default {
  components: {
    CollapsibleCard,
    AddRmButtons,
    SingleSelect
  },
  mixins: [VeeValidationMixin, ProjectFieldsetMixin],
  computed: {
    ...mapGetters({
      modified: 'project/getModified'
    }),
    ...mapGettersActions({
      partners: ['project', 'getPartners', 'setPartners', 0]
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
        this.$validator.validate()
      ]);
      return validations.reduce((a, c) => a && c, true);
    },
    addPartner () {
      this.partners = [...this.partners, null];
    },
    rmPartner (index) {
      this.partners = this.partners.filter((p, i) => i !== index);
    },
    isLastAndExist (collection, index) {
      return !!(collection.length - 1 === index && collection[index]);
    },
    setPartnerItem (index, key, value) {
      const partners = [...this.partners];
      partners[index] = partners[index] ? { ...partners[index] } : {};
      partners[index][key] = value;
      this.partners = partners;
    },
    selectedType (partnerId) {
      return this.partners
        .filter((partner) => partner && partner.partner_type !== partnerId)
        .map(({ partner_type }) => partner_type);
    }
  }
};
</script>

<style lang="less">
.btContainer {
  margin-top: 50px;
}
</style>
