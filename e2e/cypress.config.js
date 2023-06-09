const { defineConfig } = require("cypress");

module.exports = defineConfig({
  reporter: 'cypress-mochawesome-reporter',
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      require('cypress-mochawesome-reporter/plugin')(on);
    },
    baseUrl: "https://invent-dev.unitst.org",
    chromeWebSecurity: false,
    defaultCommandTimeout: 60000,
    experimentalModifyObstructiveThirdPartyCode: true,
    experimentalSessionAndOrigin:true,
    viewportHeight:1000,
    viewportWidth:1400,
    watchForFileChanges: false,
    video: false
  },
});
