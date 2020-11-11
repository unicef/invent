<template>
  <el-form-item
    :error="errors.first('answer', 'custom_question_' + id)"
    :label="question"
    class="CustomField"
  >
    <div v-show="isPrivate" class="PrivateBadge">
      <el-tooltip
        effect="dark"
        placement="right"
        content="This field is hidden from public"
      >
        <el-tag :key="1" size="mini" type="danger"> Private field </el-tag>
      </el-tooltip>
    </div>

    <el-input
      v-if="type < 3"
      v-model="innerValue"
      v-validate="localRules"
      :data-vv-as="question"
      :data-vv-scope="'custom_question_' + id"
      data-vv-name="answer"
    />

    <el-radio-group
      v-if="type === 3"
      v-model="innerValue"
      v-validate="localRules"
      :data-vv-as="question"
      :data-vv-scope="'custom_question_' + id"
      data-vv-name="answer"
    >
      <el-radio label="Yes">
        <translate>Yes</translate>
      </el-radio>
      <el-radio label="No">
        <translate>No</translate>
      </el-radio>
    </el-radio-group>

    <template v-if="type > 3 && options">
      <el-select
        v-model="innerValue"
        v-validate="localRules"
        :placeholder="$gettext('Select from list') | translate"
        :multiple="type === 5"
        :data-vv-as="question"
        :data-vv-scope="'custom_question_' + id"
        filterable
        data-vv-name="answer"
        popper-class="CustomFieldSelectorDropdown"
        class="CustomFieldSelector"
      >
        <el-option v-for="opt in options" :key="opt" :value="opt" />
      </el-select>
    </template>
  </el-form-item>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import VeeValidationMixin from '../mixins/VeeValidationMixin.js'

export default {
  mixins: [VeeValidationMixin],
  props: {
    type: {
      type: Number,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
    question: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      default: () => [],
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    isPrivate: {
      type: Boolean,
      default: false,
    },
    doValidation: {
      type: Boolean,
      default: false,
    },
    donorId: {
      type: Number,
      default: null,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      getCountryAnswerDetails: 'project/getCountryAnswerDetails',
      getDonorsAnswerDetails: 'project/getDonorsAnswerDetails',
    }),
    answer() {
      const saved = !this.donorId
        ? this.getCountryAnswerDetails(this.id)
        : this.getDonorsAnswerDetails(this.id)
      return (
        saved || {
          question_id: this.id,
          answer: null,
        }
      )
    },
    value() {
      return this.answer.answer
    },
    innerValue: {
      get() {
        if (this.value && Array.isArray(this.value) && this.value.length > 0) {
          return this.type === 5 ? this.value : this.value[0]
        }
        return this.type === 5 ? [] : null
      },
      set(answer) {
        answer = Array.isArray(answer) ? answer : [answer]
        if (!this.donorId) {
          this.setCountryAnswer({ ...this.answer, answer })
        } else {
          this.setDonorAnswer({ ...this.answer, answer })
        }
      },
    },
    localRules() {
      return {
        required: this.isRequired && this.doValidation,
        numeric: this.type === 2 && this.doValidation,
      }
    },
  },
  watch: {
    customCountryErrors: {
      immediate: true,
      handler(errors) {
        if (!this.donorId) {
          this.findCountryError(errors)
        }
      },
    },
    customDonorsErrors: {
      immediate: true,
      handler(errors) {
        if (this.donorId) {
          this.findDonorError(errors)
        }
      },
    },
  },
  methods: {
    ...mapActions({
      setCountryAnswer: 'project/setCountryAnswer',
      setDonorAnswer: 'project/setDonorAnswer',
    }),
    addErrorToBag(error) {
      const firsElement = error[Object.keys(error)[0]]
      const msg = firsElement ? firsElement[0] : null
      if (msg) {
        this.errors.add({
          field: 'answer',
          scope: 'custom_question_' + this.id,
          msg,
        })
      }
    },
    findCountryError(errors) {
      if (errors && errors.length > this.index - 1) {
        const error = errors[this.index]
        if (error) {
          this.addErrorToBag(error)
        }
      }
    },
    findDonorError(errors) {
      const error = errors.find(
        (e) => e.index === this.index && e.donor_id === this.donorId
      )
      if (error) {
        this.addErrorToBag(error.error)
      }
    },
    validate() {
      return this.$validator.validate()
    },
  },
}
</script>

<style lang="less">
.CustomField {
  position: relative;

  .el-form-item__label {
    line-height: 20px;
    margin-bottom: 10px;
  }

  .CustomFieldSelector {
    width: 100%;
  }

  .PrivateBadge {
    position: relative;
    top: -5px;
    margin-bottom: 10px;
    width: 100%;
  }
}
</style>
