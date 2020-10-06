const formAPIErrorsMixin = {
  data() {
    return {
      formAPIErrors: {},
    }
  },

  methods: {
    deleteFormAPIErrors() {
      this.formAPIErrors = {}
    },

    setFormAPIErrors(error) {
      if (error.response && error.response.data) {
        this.formAPIErrors = error.response.data
      } else {
        console.error('Failed to associate API error: ', error)
      }
    },

    validatorGenerator(prop) {
      return (rule, value, callback) => {
        if (this.formAPIErrors[prop] && this.formAPIErrors[prop].length) {
          const error = {
            message: this.formAPIErrors[prop][0],
            field: rule.fullField,
          }
          callback(error)
        } else {
          callback()
        }
      }
    },
    collectionValidatorGenerator(prop) {
      return (rule, value, callback) => {
        const parts = rule.field.split('.')
        prop = parts[0]
        const index = +parts[1]
        if (this.formAPIErrors[prop] && this.formAPIErrors[prop][index]) {
          const firstError = this.formAPIErrors[prop][index][
            Object.keys(this.formAPIErrors[prop][index])[0]
          ]
          if (firstError && firstError.length) {
            const error = {
              message: firstError[0],
              field: rule.fullField,
            }
            callback(error)
            return
          }
        }
        callback()
      }
    },
  },

  computed: {
    nonFieldErrors() {
      if (
        this.formAPIErrors.non_field_errors &&
        this.formAPIErrors.non_field_errors.length
      ) {
        return this.formAPIErrors.non_field_errors[0]
      } else {
        return ''
      }
    },
  },
}

export default formAPIErrorsMixin
