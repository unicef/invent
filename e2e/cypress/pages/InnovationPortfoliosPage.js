/// <reference types="Cypress" />

class InnovationPortfoliosPage{

    getInnovationPortfoliosSection(){
        return cy.contains("UNICEF’s Global Innovation Portfolios")
    }

    getPortfolios(){
        return cy.get('[class="portfolio-title"]')
    }//<span data-v-59673754="" class="portfolio-title">Climate Change</span>

    openPortfolio(name){
        this.getPortfolios().contains(name).click()

    }


}
export default InnovationPortfoliosPage