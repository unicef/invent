<template>
  <div class="CreateProject">
    <div class="PageTitle">
      <h2><translate>Register your Digital Health Initiative</translate></h2>
      <p>
        <translate
          >Please complete the questions below to include your initiative
          information in the Digital Health Atlas. These questions document your
          initiative's health focus area(s), software features and national
          scale.</translate
        >
      </p>
    </div>
    <project-form />
  </div>
</template>

<script>
import ProjectForm from '../../../components/project/ProjectForm'

export default {
  components: {
    ProjectForm,
  },
  async fetch({ store }) {
    await Promise.all([
      store.dispatch('projects/loadProjectStructure'),
      store.dispatch('system/loadDonors'),
      store.dispatch('system/loadOrganisations'),
    ])
    await store.dispatch('project/resetProjectState')
    store.dispatch('landing/resetSearch')
  },
}
</script>

<style lang="less">
@import '../../../assets/style/variables.less';
@import '../../../assets/style/mixins.less';

.CreateProject {
}
</style>
