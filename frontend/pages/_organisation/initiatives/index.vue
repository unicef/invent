<template>
  <div>
    <tabs :tabs="tabs" :tab="tab" @handleTab="setTab">
      <template slot="title">
        <h2>
          <translate>My Initiatives</translate>
        </h2>
      </template>
    </tabs>
    <user-project-list />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

import UserProjectList from '@/components/common/UserProjectsList'
import Tabs from '@/components/common/Tabs'

export default {
  components: {
    UserProjectList,
    Tabs,
  },
  computed: {
    ...mapState({
      tabs: (state) => state.projects.tabs,
      tab: (state) => state.projects.tab,
    }),
  },
  methods: {
    ...mapActions({
      setTab: 'projects/setTab',
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
</style>
