const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    baseUrl: "https://invent-tst.unitst.org/en/-/",
    chromeWebSecurity: false,
    defaultCommandTimeout: 60000,
    experimentalModifyObstructiveThirdPartyCode: true,
    experimentalSessionAndOrigin:true,
    viewportHeight:1000,
    viewportWidth:1400

  },
});
