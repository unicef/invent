/// <reference types="Cypress" />

class HomePage{

    getWelcomeSection() {
        return cy.get('[class="WelcomeSection"]')
    }
    
    getInitiativesSection() {
        return cy.get('[class="InitiativesSection"]')
    }

    getSeeAll() {
        return cy.get('.action > .link > a')
    }

    getTable() {
        return cy.get('.initiative-wrapper > .top').find('tr')
    }

}
export default HomePage