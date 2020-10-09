<template>
  <el-dialog
    v-if="visible"
    :visible.sync="visible"
    :title="$gettext('Save filters') | translate"
    modal
    top="30vh"
    width="30vw"
    custom-class="SaveFiltersDialog"
  >
    <el-form
      :model="form"
      :rules="rules"
      label-position="left"
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
          <el-button type="text" class="CancelButton" @click="cancel">
            <translate>Cancel</translate>
          </el-button>
        </el-col>
        <el-col class="PrimaryButtons">
          <el-button type="primary" @click="apply">
            <translate>Save</translate>
          </el-button>
        </el-col>
      </el-row>
    </span>
  </el-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  components: {},
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
          { validator: this.noDuplicate, trigger: 'change' },
        ],
      },
    }
  },
  computed: {
    ...mapGetters({
      filterCategory: 'layout/getSaveFiltersDialogState',
      savedFilters: 'dashboard/getSavedFilters',
    }),
    visible: {
      get() {
        return this.filterCategory !== null
      },
      set() {
        this.setSaveFiltersDialogState(null)
      },
    },
  },
  methods: {
    ...mapActions({
      setSaveFiltersDialogState: 'layout/setSaveFiltersDialogState',
      setSavedFilters: 'dashboard/setSavedFilters',
    }),
    noDuplicate(rule, value, callback) {
      const exist = this.savedFilters.find((s) => s.name === value)
      if (exist) {
        callback(
          new Error(
            this.$gettext(
              'A saved configuration with this name is already present'
            )
          )
        )
      } else {
        callback()
      }
    },
    cancel() {
      this.setSaveFiltersDialogState(null)
    },
    apply() {
      const filters = [
        ...this.savedFilters,
        {
          category: this.filterCategory,
          name: this.form.name,
          query: this.$route.query,
        },
      ]
      this.setSavedFilters(filters)
      this.setSaveFiltersDialogState(null)
      this.form.name = ''
    },
  },
}
</script>

<style lang="less">
@import '../../assets/style/variables.less';
@import '../../assets/style/mixins.less';

.SaveFiltersDialog {
  .el-form,
  .el-form-item {
    margin: 20px 0;
  }
}
</style>
