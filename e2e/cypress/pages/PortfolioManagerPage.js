/// <reference types="Cypress" />

class PortfolioManagerPage{

    getPortfolioManagerSection(){
        return cy.get('class="portfolios"')
    }
}
export default PortfolioManagerPage