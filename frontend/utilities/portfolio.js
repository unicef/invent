export const portfolioFields = () => ({
  name: "",
  description: "",
  status: [],
  icon: null,
  managers: [],
  statements: []
});

export const draftRules = () => {
  return {
    name: {
      required: false,
      min: 1,
      max: 128
    },
    description: {
      required: false,
      max: 128
    },
    status: {
      required: false
    },
    icon: {
      required: false
    },
    managers: {
      required: false
    },
    statements: {
      required: false
    },
    statementName: {
      required: false
    },
    statementDescription: {
      required: false
    }
  };
};

export const publishRules = () => {
  return {
    name: {
      required: false,
      min: 1,
      max: 128
    },
    description: {
      required: false,
      max: 128
    },
    status: {
      required: false
    },
    icon: {
      required: false
    },
    managers: {
      required: false
    },
    statements: {
      required: false
    },
    statementName: {
      required: false
    },
    statementDescription: {
      required: false
    }
  };
};
