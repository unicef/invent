<template>
  <simple-field
    :header="question"
  >
    <template v-if="type < 5">
      <span v-show="value">
        {{ value }}
      </span>
      <span v-show="!value">
        <translate> N/A </translate>
      </span>
    </template>
    <template v-if="type === 5">
      <ul>
        <li
          v-for="v in value"
          :key="v"
        >
          <span v-show="v">
            {{ v }}
          </span>
          <span v-show="!v">
            <translate> N/A </translate>
          </span>
        </li>
      </ul>
    </template>
  </simple-field>
</template>

<script>
import SimpleField from './SimpleField';

import { mapGetters } from 'vuex';

export default {
  components: {
    SimpleField
  },
  props: {
    type: {
      type: Number,
      required: true
    },
    id: {
      type: Number,
      required: true
    },
    question: {
      type: String,
      required: true
    },
    donorId: {
      type: Number,
      default: null
    },
    isDraft: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      getPublishedCountryAnswerDetails: 'project/getPublishedCountryAnswerDetails',
      getCountryAnswerDetails: 'project/getCountryAnswerDetails',
      getDonorsAnswerDetails: 'project/getDonorsAnswerDetails',
      getPublishedDonorsAnswerDetails: 'project/getPublishedDonorsAnswerDetails'
    }),
    answer () {
      let detailsFunction = () => null;
      if (!this.donorId) {
        detailsFunction = this.isDraft ? this.getCountryAnswerDetails : this.getPublishedCountryAnswerDetails;
      } else {
        detailsFunction = this.isDraft ? this.getPublishedDonorsAnswerDetails : this.getPublishedDonorsAnswerDetails;
      }
      const saved = detailsFunction(this.id);
      return saved || {
        question_id: this.id,
        answer: []
      };
    },
    value () {
      return this.type === 5 ? this.answer.answer : this.answer.answer[0];
    }
  }
};
</script>

<style lang="less">
.CustomField {
  width: 100%;

  .CustomFieldSelector {
    width: 100%;
  }
}

</style>
