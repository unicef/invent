const { defineConfig } = require("cypress")
const {downloadFile} = require("cypress-downloadfile/lib/addPlugin")

module.exports = defineConfig({
  reporter: 'cypress-mochawesome-reporter',
  e2e: {
    setupNodeEvents(on, config) {
      require('cypress-mochawesome-reporter/plugin')(on),
      on ('task', {downloadFile})
    },
    baseUrl: "https://invent-tst.unitst.org",
    chromeWebSecurity: false,
    defaultCommandTimeout: 60000,
    experimentalModifyObstructiveThirdPartyCode: true,
    experimentalSessionAndOrigin:true,
    viewportHeight:1000,
    viewportWidth:1400,
    watchForFileChanges: false,
    video: true
  },
})
