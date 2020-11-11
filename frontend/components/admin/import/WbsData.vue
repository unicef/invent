<template>
  <div>
    <el-row v-for="(wbsItem, index) in wbs" :key="index">
      <el-col :span="16">
        <div>
          <translate> Please add the relevant WBS number: </translate>
        </div>
        <character-count-input
          :value="wbsItem"
          @input="setWbsItem(index, $event)"
        />
      </el-col>
      <el-col :span="8" class="btContainer">
        <add-rm-buttons
          :show-add="isLastAndExist(wbs, index)"
          :show-rm="wbs.length > 1"
          @add="addDhi"
          @rm="rmDhi(index)"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import AddRmButtons from '@/components/project/AddRmButtons'
export default {
  name: 'WbsData',
  components: {
    AddRmButtons,
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  computed: {
    wbs: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('update:value', val)
      },
    },
  },
  methods: {
    isLastAndExist(collection, index) {
      return !!(collection.length - 1 === index && collection[index])
    },
    addDhi() {
      this.wbs = [...this.wbs, null]
    },
    rmDhi(index) {
      this.wbs = this.wbs.filter((p, i) => i !== index)
    },
    setWbsItem(index, value) {
      const wbs = [...this.wbs]
      wbs[index] = value
      this.wbs = wbs
    },
  },
}
</script>

<style scoped></style>
