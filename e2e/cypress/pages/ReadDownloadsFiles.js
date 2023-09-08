/// <reference types="Cypress" />

class ReadDownloadsFiles {
    readCSV() {
        const moment = require('moment')
        const filename = 'cypress/downloads/User-'+ moment().format("YYYY-MM-DD") +'.csv'
        return cy.readFile(filename)
    }
}
export default ReadDownloadsFiles