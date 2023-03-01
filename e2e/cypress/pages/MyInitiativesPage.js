/// <reference types="Cypress" />

class MyInitiativesPage{

    getMyInitiativesSection(){
        return cy.title().should('eq', "Invent: UNICEF's T4D and Innovation Inventory")
    }
}
export default MyInitiativesPage