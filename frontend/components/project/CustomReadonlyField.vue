<template>
  <simple-field v-show="value" :header="question">
    <template v-if="type < 5">
      <span>
        {{ value }}
      </span>
    </template>
    <template v-if="type === 5">
      <ul>
        <li v-for="v in value" :key="v">
          <span v-show="v">
            {{ v }}
          </span>
          <span v-show="!v">
            <!-- N/A -->
          </span>
        </li>
      </ul>
    </template>
  </simple-field>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleField from './SimpleField'

export default {
  components: {
    SimpleField,
  },
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
    donorId: {
      type: Number,
      default: null,
    },
    isDraft: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      getPublishedCountryAnswerDetails:
        'project/getPublishedCountryAnswerDetails',
      getCountryAnswerDetails: 'project/getCountryAnswerDetails',
      getDonorsAnswerDetails: 'project/getDonorsAnswerDetails',
      getPublishedDonorsAnswerDetails:
        'project/getPublishedDonorsAnswerDetails',
    }),
    answer() {
      let detailsFunction = () => null
      if (!this.donorId) {
        detailsFunction = this.isDraft
          ? this.getCountryAnswerDetails
          : this.getPublishedCountryAnswerDetails
      } else {
        detailsFunction = this.isDraft
          ? this.getPublishedDonorsAnswerDetails
          : this.getPublishedDonorsAnswerDetails
      }
      const saved = detailsFunction(this.id)
      return (
        saved || {
          question_id: this.id,
          answer: [],
        }
      )
    },
    value() {
      const answer =
        this.type === 5 ? this.answer.answer : this.answer.answer[0]
      return !answer || !answer.match
        ? answer
        : answer.match(/.{1,102}/g).join('\n')
    },
  },
}
</script>

<style lang="less">
.CustomField {
  width: 100%;

  .CustomFieldSelector {
    width: 100%;
  }
}
</style>
