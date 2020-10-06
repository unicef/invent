<template>
  <div class="ProjectCardActions">
    <el-row
      type="flex"
      justify="end"
    >
      <el-col v-if="showViewDraft">
        <nuxt-link
          :to="localePath({name: 'organisation-initiatives-id', params: {id: project.id, organisation: $route.params.organisation}})"
          class="NuxtLink IconLeft"
        >
          <fa icon="arrow-right" />
          <translate>View Draft</translate>
        </nuxt-link>
      </el-col>
      <el-col v-if="showViewPublished">
        <nuxt-link
          :to="localePath({name: 'organisation-initiatives-id-published', params: {id: project.id, organisation: $route.params.organisation}})"
          class="NuxtLink IconLeft"
        >
          <fa icon="arrow-right" />
          <translate>View Published</translate>
        </nuxt-link>
      </el-col>
      <el-col v-if="showEditDraft">
        <nuxt-link
          :to="localePath({name: 'organisation-initiatives-id-edit', params: {id: project.id, organisation: $route.params.organisation}})"
          class="NuxtLink IconLeft"
        >
          <fa icon="edit" />
          <translate>Edit Draft</translate>
        </nuxt-link>
      </el-col>
      <el-col v-if="isSuperUser">
        <nuxt-link
          :to="localePath({name: 'organisation-initiatives-id-assessment', params: {id: project.id, organisation: $route.params.organisation}})"
          class="NuxtLink IconLeft"
        >
          <fa icon="tachometer-alt" />
          <translate>Assessment</translate>
        </nuxt-link>
      </el-col>
      <el-col v-if="project.isPublished">
        <nuxt-link
          to=""
          class="NuxtLink IconLeft Danger"
          @click.native="handleClickUnPublish({ name: 'organisation-initiatives' }, project.id)"
        >
          <fa icon="times-circle" />
          <translate>Unpublish</translate>
        </nuxt-link>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import handleProjectActions from "@/components/mixins/handleProjectActions";

export default {
  mixins: [handleProjectActions],
  props: {
    project: {
      type: Object,
      required: true,
    },
    forceShow: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isSuperUser() {
      return this.user && this.user.is_superuser;
    },
    showViewDraft() {
      return this.forceShow || this.project.isViewer || this.project.isMember;
    },
    showEditDraft() {
      return this.forceShow || this.project.isMember;
    },
    showViewPublished() {
      return this.forceShow || this.project.isPublished;
    },
  },
};
</script>

<style lang="less">
@import "../../assets/style/variables.less";
@import "../../assets/style/mixins.less";

.ProjectCardActions {
  .el-row {
    .el-col {
      width: auto;
    }
  }

  .NuxtLink {
    margin-left: 40px;
    line-height: 24px;
  }

  .Danger {
    color: @colorDanger;
    &:hover {
      color: @colorDanger;
    }
  }
}
</style>
