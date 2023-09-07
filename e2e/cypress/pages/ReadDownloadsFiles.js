/// <reference types="Cypress" />

class ReadDownloadsFiles {

    readCSV() {
        return cy.readFile('cypress/downloads/User-2023-09-05.csv')
    }
}
export default ReadDownloadsFiles