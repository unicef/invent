<template>
  <el-dialog
    :visible="visible"
    :title="$gettext('Save filters') | translate"
    modal
    top="30vh"
    width="30vw"
    custom-class="SaveFiltersDialog"
    @close="handleCancel"
  >
    <el-form
      :model="form"
      :rules="rules"
      label-position="top"
      label-width="160px"
      @submit.native.prevent
    >
      <el-form-item
        :label="$gettext('Filter preset name') | translate"
        prop="name"
      >
        <el-input v-model="form.name" />
      </el-form-item>
    </el-form>

    <span slot="footer">
      <el-row type="flex" align="center">
        <el-col class="SecondaryButtons">
          <el-button type="text" class="CancelButton" @click="handleCancel">
            <translate>Cancel</translate>
          </el-button>
        </el-col>
        <el-col class="PrimaryButtons">
          <el-button
            type="primary"
            :disabled="disabled"
            :loading="loading"
            @click="handleSave"
          >
            <translate>Save</translate>
          </el-button>
        </el-col>
      </el-row>
    </span>
  </el-dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      form: {
        name: '',
      },
      rules: {
        name: [
          {
            required: true,
            message: this.$gettext('This is required'),
            trigger: 'blur',
          },
        ],
      },
    }
  },
  computed: {
    ...mapState({
      visible: (state) => state.layout.saveFiltersDialogState,
      loading: (state) => state.filters.loading,
    }),
    disabled() {
      return !(this.form.name.length >= 3)
    },
  },
  methods: {
    ...mapActions({
      setDialog: 'layout/setSaveFiltersDialogState',
      newFilter: 'filters/newFilter',
    }),
    handleCancel() {
      this.setDialog(false)
    },
    handleSave() {
      this.newFilter(this.form.name)
      this.setDialog(false)
      this.form.name = ''
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.SaveFiltersDialog {
  .el-form,
  .el-form-item {
    margin: 20px 0;
  }
}
</style>
