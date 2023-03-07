export const draftRules = () => {
  return {
    name: {
      min: 3,
      max: 128,
    },
    phase: {},
    tech: {},
    learning: {},
    override_reach: {},
  }
}
export const publishRules = () => {
  return {
    name: {
      required: true,
      min: 3,
      max: 128,
    },
    phase: {
      required: true,
    },
    tech: {},
    learning: {},
    override_reach: {},
  }
}
