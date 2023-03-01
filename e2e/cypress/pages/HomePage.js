/// <reference types="Cypress" />

class HomePage{

    getWelcomeSection(){
        return cy.get('[class="WelcomeSection"]')
    }
}
export default HomePage