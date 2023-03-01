/// <reference types="Cypress" />

class InnovationPortfoliosPage{

    getInnovationPortfoliosSection(){
        return cy.get('class="portfolios"')
    }
}
export default InnovationPortfoliosPage