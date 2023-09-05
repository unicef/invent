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
    portfolio_statements_table: {
      required: false,
    },
    countrySingleSelect: {
      required: true,
      is_not: null,
    },
    countrySingleNumber: {},
    portfolioSingleSelect: { required: true, is_not: null },
    problemStatementSelect: { required: true, is_not: [] },
    setAside2021: { required: false },
    setAside2022: { required: false },
  }
}
