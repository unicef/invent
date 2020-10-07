import uniqBy from 'lodash/uniqBy'

export default {
  data() {
    return {
      options: [],
      query: '',
    }
  },
  computed: {
    optionsAndValues() {
      // const result = [...this.options].sort((a, b) => a.email.localeCompare(b.email));
      const result = [...this.options].sort()

      if (this.value) {
        if (Array.isArray(this.value) && this.value.length > 0) {
          result.push(
            ...this.items.filter((p) => this.value.some((v) => v === p.id))
          )
        } else {
          result.push(...this.items.filter((p) => p.id === +this.value))
        }
      }
      return uniqBy(result, 'id')
    },
  },
  methods: {
    filterList(query) {
      this.query = query
      if (query) {
        this.options = this.items.filter(
          (p) =>
            this.filter(p.name ? p.name : p.email, query) ||
            (p.email ? this.filter(p.email, query) : false)
        )
      } else {
        this.options = []
      }
    },
    filter(val, query) {
      return val.toLowerCase().startsWith(query.toLowerCase())
    },
  },
}
