/// <reference types="Cypress" />

class HomePage{

    getWelcomeSection(){
        return cy.get('[class="WelcomeSection"]')
    }
    
    getInitiativesSection(){
        return cy.get('[class="InitiativesSection"]')
    }

}
export default HomePage