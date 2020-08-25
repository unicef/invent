<template>
  <div id="general" class="general-settings">
    <collapsible-card
      ref="collapsible"
      :title="$gettext('General settings') | translate"
    >
      <custom-required-form-item
        :error="errors.first('name')"
        :draft-rule="draftRules.name"
        :publish-rule="publishRules.name"
        row
      >
        <template slot="label">
          <translate key="portfolio-name">
            Portfolio name
          </translate>
        </template>
        <character-count-input
          v-model="name"
          v-validate="rules.name"
          :rules="rules.name"
          data-as-name="Name"
          data-vv-name="name"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('description')"
        :draft-rule="draftRules.description"
        :publish-rule="publishRules.description"
        row
      >
        <template slot="label">
          <translate key="portfolio-description">
            Description
          </translate>
        </template>

        <character-count-input
          v-model="description"
          v-validate="rules.description"
          :rules="rules.description"
          data-vv-name="description"
          data-vv-as="Description"
          type="textarea"
        />
      </custom-required-form-item>
      <custom-required-form-item
        :error="
          errors.first('status')
            ? errors.first('status').replace('_', ' ')
            : undefined
        "
        :draft-rule="draftRules.status"
        :publish-rule="publishRules.status"
        row
      >
        <template slot="label">
          <translate key="status">
            Status
          </translate>
        </template>
        <country-office-select
          v-model="status"
          v-validate="rules.status"
          data-vv-name="status"
          data-vv-as="status"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="
          errors.first('icon')
            ? errors.first('icon').replace('_', ' ')
            : undefined
        "
        :draft-rule="draftRules.icon"
        :publish-rule="publishRules.icon"
        row
      >
        <template slot="label">
          <translate key="icon">
            Icon
          </translate>
        </template>
        <icon-select
          v-model="icon"
          icons=""
          v-validate="rules.icon"
          data-vv-name="icon"
          data-vv-as="icon"
        />
      </custom-required-form-item>

      <div class="disclaimer">
        <fa icon="info-circle" size="md" />
        <p>
          <translate>
            This is a bottom note section if it’s needed: lorem ispumd olor sit
            amet. Prima luce, cum quibus mons aliud consensu ab eo. Cum sociis
            natoque penatibus et magnis dis parturient. Ambitioni dedisse
            scripsisse iudicaretur. Quis aute iure reprehenderit in voluptate
            velit esse.
          </translate>
        </p>
      </div>
    </collapsible-card>
  </div>
</template>

<script>
import { mapGettersActions } from "@/utilities/form";
import { mapGetters, mapState } from "vuex";
import VeeValidationMixin from "@/components/mixins/VeeValidationMixin";
import PortfolioFieldsetMixin from "@/components/mixins/PortfolioFieldsetMixin";
import CollapsibleCard from "@/components/portfolio/CollapsibleCard";
import CountryOfficeSelect from "@/components/common/CountryOfficeSelect";
import IconSelect from "@/components/portfolio/form/inputs/IconSelect";

export default {
  components: {
    CollapsibleCard,
    CountryOfficeSelect,
    IconSelect
  },
  mixins: [VeeValidationMixin, PortfolioFieldsetMixin],
  computed: {
    ...mapState({
      // todo: setIcons
      offices: state => state.offices.offices
    }),
    ...mapGetters({
      // todo: getIcons
    }),
    ...mapGettersActions({
      name: ["portfolio", "getName", "setName", 0],
      description: ["portfolio", "getDescription", "setDescription", 0],
      status: ["portfolio", "getStatus", "setStatus", 0],
      icon: ["portfolio", "getIcon", "setIcon", 0]
    })
  },
  methods: {
    async validate() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([this.$validator.validate()]);
      console.log("General settings published validation", validations);
      return validations.reduce((a, c) => a && c, true);
    },
    async validateDraft() {
      this.$refs.collapsible.expandCard();
      const validations = await Promise.all([
        this.$validator.validate("name"),
        this.$validator.validate("description"),
        this.$validator.validate("status"),
        this.$validator.validate("icon")
      ]);
      console.log("General settings draft validation", validations);
      return validations.reduce((a, c) => a && c, true);
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.general-settings {
  .el-card {
    overflow: inherit;
  }
  .select-office {
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
}
</style>
