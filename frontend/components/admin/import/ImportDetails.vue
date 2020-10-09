<template>
  <div v-if="item" class="ImportDetails">
    <el-row type="flex">
      <el-col :span="8">
        <div class="Label">
          <translate>Country</translate>
        </div>
        <country-item :id="countryId" />
      </el-col>

      <el-col :span="8">
        <div class="Label">
          <translate>Office</translate>
        </div>
        {{ countryOffice }}
      </el-col>

      <el-col :span="8">
        <div class="Label">
          <translate> Investor </translate>
        </div>
        <donor-item :id="item.donor" />
      </el-col>

      <el-col :span="8">
        <div class="Label">
          <translate> Draft or Published </translate>
        </div>
        <span v-if="item.draft">Draft</span>
        <span v-else>Publish</span>
      </el-col>
      <el-col :span="8">
        <div class="Label">
          <translate> Sheet Name </translate>
        </div>
        {{ item.sheet_name }}
      </el-col>
      <el-col :span="10">
        <div class="Label">
          <translate> File Name </translate>
        </div>
        {{ item.filename }}
      </el-col>

      <el-col :span="4">
        <slot />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CountryItem from '@/components/common/CountryItem'
import DonorItem from '@/components/common/DonorItem'
import { mapState, mapActions } from 'vuex'

export default {
  components: {
    CountryItem,
    DonorItem,
  },
  props: {
    item: {
      type: Object,
      default: null,
    },
  },
  computed: {
    ...mapState({
      offices: (state) => state.offices.offices,
    }),
    countryOffice() {
      const office = this.offices.find(
        (obj) => obj.id === this.item.country_office
      )
      return office ? office.name : 'N/A'
    },
    countryId() {
      const office = this.offices.find(
        (obj) => obj.id === this.item.country_office
      )
      return office ? office.country : undefined
    },
  },
  mounted() {
    if (this.offices.length === 0) {
      this.loadOffices()
    }
  },
  methods: {
    ...mapActions({
      loadOffices: 'offices/loadOffices',
    }),
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.Label {
  display: block;
  margin: 0 0 15px;
  color: @colorTextPrimary;
  font-size: @fontSizeBase;
  font-weight: 700;
}

.ImportDetails {
  margin-bottom: 15px;
}
</style>
