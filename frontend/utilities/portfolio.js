export const portfolioFields = () => ({
  name: '',
  description: '',
  status: '',
  icon: null,
  managers: [],
  statements: [],
})

export const draftRules = () => {
  return {
    name: {
      required: true,
      min: 1,
      max: 80,
    },
    description: {
      required: true,
      max: 1000,
    },
    status: {
      required: false,
    },
    icon: {
      required: true,
    },
    managers: {
      required: false,
    },
    statements: {
      required: false,
    },
    statementName: {
      required: false,
      min: 1,
      max: 100,
    },
    statementDescription: {
      required: false,
      max: 1000,
    },
    funding: {
      required: true,
      min_value: 0,
      max_value: 999999999,
      integer: true,
      numeric: true,
    },
    landscapeReview: {
      required: true,
    },
    innovationHub: {
      required: true,
    },
  }
}

export const publishRules = () => {
  return {
    name: {
      required: true,
      min: 1,
      max: 80,
    },
    description: {
      required: true,
      max: 1000,
    },
    status: {
      required: false,
    },
    icon: {
      required: true,
    },
    managers: {
      required: false,
    },
    statements: {
      required: false,
    },
    statementName: {
      required: false,
      min: 1,
      max: 100,
    },
    statementDescription: {
      required: false,
      max: 1000,
    },
    funding: {
      required: true,
      min_value: 0,
      max_value: 999999999,
      integer: true,
      numeric: true,
    },
    landscapeReview: {
      required: true,
    },
    innovationHub: {
      required: true,
    },
  }
}
