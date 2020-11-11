<template>
  <div>
    <el-row
      v-for="(partner, index) in partners"
      :key="index"
      class="partnerRow"
    >
      <el-col :span="16">
        <translate key="partners">
          Please select all partner types involved with the initiative.
        </translate>
        <single-select
          :value="partner ? partner.partner_type : null"
          source="system/getPartnerTypes"
          @change="setPartnerItem(index, 'partner_type', $event)"
        />
      </el-col>
      <el-col :span="8" class="btContainer">
        <add-rm-buttons
          :show-add="isLastAndExist(partners, index)"
          :show-rm="partners.length > 1"
          @add="addPartner"
          @rm="rmPartner(index)"
        />
      </el-col>
      <el-col v-if="partners[index]" :span="24">
        <translate key="partner_name">
          Please provide the name(s) of your partner(s).
        </translate>

        <character-count-input
          :value="partner.partner_name"
          @input="setPartnerItem(index, 'partner_name', $event)"
        />
        <translate key="partner_contact">
          Please provide the name and title of the person in charge of the
          initiative at the respective partner(s).
        </translate>

        <character-count-input
          :value="partner.partner_contact"
          @input="setPartnerItem(index, 'partner_contact', $event)"
        />
        <translate key="partner_email"> Contact Email </translate>

        <character-count-input
          :value="partner.partner_email"
          @input="setPartnerItem(index, 'partner_email', $event)"
        />
        <translate key="partner_website"> Partner Website </translate>

        <character-count-input
          :value="partner.partner_website"
          @input="setPartnerItem(index, 'partner_website', $event)"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import SingleSelect from '@/components/common/SingleSelect'
import AddRmButtons from '@/components/project/AddRmButtons'

export default {
  name: 'PartnerData',
  components: {
    SingleSelect,
    AddRmButtons,
  },
  props: {
    value: {
      required: true,
      type: Array,
    },
  },
  computed: {
    partners: {
      get() {
        return this.value && this.value.length ? this.value : [null]
      },
      set(val) {
        this.$emit('update:value', val)
      },
    },
  },
  methods: {
    addPartner() {
      this.partners = [...this.partners, null]
    },
    rmPartner(index) {
      this.partners = this.partners.filter((p, i) => i !== index)
    },
    isLastAndExist(collection, index) {
      return !!(collection.length - 1 === index && collection[index])
    },
    setPartnerItem(index, key, value) {
      const partners = [...this.partners]
      partners[index] = partners[index] ? { ...partners[index] } : {}
      partners[index][key] = value
      this.partners = partners
    },
  },
}
</script>

<style scoped>
.btContainer {
  margin-top: 20px;
}
.partnerRow {
  border-bottom: 1px dotted black;
  padding-top: 15px;
  padding-bottom: 15px;
}
</style>
