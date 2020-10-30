<template>
  <div class="ImportList">
    <el-row type="flex">
      <el-col v-if="queue && queue.length > 0" :span="16">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <translate>Previous imports</translate>
          </div>
          <import-details
            v-for="(item, index) in queue"
            :key="index"
            :item="item"
            type="flex"
          >
            <el-button @click="select(item)">
              <translate> Select </translate>
            </el-button>
          </import-details>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <translate>New Import</translate>
          </div>
          <import-file />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ImportFile from '@/components/admin/import/ImportFile'
import ImportDetails from '@/components/admin/import/ImportDetails'

export default {
  components: {
    ImportFile,
    ImportDetails,
  },
  async fetch({ store }) {
    await Promise.all([
      store.dispatch('system/loadDonors'),
      store.dispatch('countries/loadMapData'),
      store.dispatch('admin/import/loadQueue'),
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('system/loadStaticData'),
    ]).then(function () {
      const code = store.getters['system/getUnicefDonor'].id
      return store.dispatch('system/loadDonorDetails', code)
    })
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/getProfile',
      queue: 'admin/import/getQueue',
      getCountryDetails: 'countries/getCountryDetails',
      dhi: 'projects/getDigitalHealthInterventions',
    }),
  },
  methods: {
    async select({ id }) {
      this.$nuxt.$loading.start()
      await this.$nextTick()
      this.$router.push(
        this.localePath({
          name: 'organisation-admin-import-id',
          params: { ...this.$route.params, id },
          query: undefined,
        })
      )
    },
  },
}
</script>

<style lang="less">
.ImportList {
  .box-card {
    margin: 12px;
  }
}
</style>
