export const rules = () => {
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
