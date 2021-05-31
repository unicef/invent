const { percyHealthCheck } = require("@percy/cypress/task");
const codeCoverageTask = require("@cypress/code-coverage/task");

module.exports = (on, config) => {
  on("task", {
    percyHealthCheck,
    async "db:seed"() {
      // seed database with test data
      const { data } = await axios.post(`${testDataApiEndpoint}/seed`);
      return data;
    },

    // fetch test data from a database (MySQL, PostgreSQL, etc...)
    "filter:database"(queryPayload) {
      return queryDatabase(queryPayload, (data, attrs) => _.filter(data.results, attrs));
    },
    "find:database"(queryPayload) {
      return queryDatabase(queryPayload, (data, attrs) => _.find(data.results, attrs));
    },
  });
  codeCoverageTask(on, config);
  return config;
};
