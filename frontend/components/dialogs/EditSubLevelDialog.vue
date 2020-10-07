<template>
  <el-dialog
    v-if="visible"
    :visible.sync="visible"
    :title="$gettext('Edit Sub Level') | translate"
    modal
    top="10vh"
    width="70vw"
    custom-class="EditSubLevelDialog"
  >
    <el-form label-position="left" label-width="160px" @submit.native.prevent>
      <el-form-item v-for="key in editableKeys" :key="key" :label="key">
        <el-input v-model="localValue[key]" />
      </el-form-item>
    </el-form>
    <span slot="footer">
      <el-row type="flex" align="center">
        <el-col class="SecondaryButtons">
          <el-button type="text" class="CancelButton" @click="visible = false">
            <translate>Cancel</translate>
          </el-button>
        </el-col>
        <el-col class="PrimaryButtons">
          <el-button type="primary" @click="save">
            <translate>Save</translate>
          </el-button>
        </el-col>
      </el-row>
    </span>
  </el-dialog>
</template>

<script>
import { mapGettersActions } from '@/utilities/form.js'

export default {
  data() {
    return {
      localValue: {},
    }
  },
  computed: {
    ...mapGettersActions({
      model: [
        'layout',
        'getEditSubLevelDialogState',
        'setEditSubLevelDialogState',
        0,
      ],
    }),
    visible: {
      get() {
        return !!this.model
      },
      set() {
        this.model = null
      },
    },
    editableKeys() {
      return Object.keys(this.model.item).filter((k) => k.includes('name'))
    },
  },
  watch: {
    model: {
      immediate: true,
      deep: true,
      handler(value) {
        if (value) {
          this.localValue = { ...value.item }
        }
      },
    },
  },
  methods: {
    save() {
      this.model.callback(this.localValue)
      this.visible = false
    },
  },
}
</script>

<style></style>
