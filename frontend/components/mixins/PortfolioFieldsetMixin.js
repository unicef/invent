export default {
  props: {
    usePublishRules: {
      type: Boolean,
      default: false
    },
    draftRules: {
      type: Object,
      required: true
    },
    publishRules: {
      type: Object,
      required: true
    }
  }
};
