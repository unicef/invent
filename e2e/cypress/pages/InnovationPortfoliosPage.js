/// <reference types="Cypress" />

class InnovationPortfoliosPage{

    getInnovationPortfoliosSection(){
        return cy.contains("UNICEF’s Global Innovation Portfolios")
    }

    getPortfolios(){
        return cy.get('[class="portfolio-title"]')
    }

    getEditPortfolioButton(){
        return cy.get('.SolutionsButton > a').contains("Edit Portfolio")
    }

    getViewPortfolios(){
        return cy.get('.AccordionTitle').each(($ele) => {
            cy.wrap($ele).contains('View Portfolio').should('be.visible')
        })

    }
    openSolution(){
        return cy.get('[class="ProjectName"]').eq(1).click()
    }

    openPortfolio(name){
        this.getPortfolios().contains(name).click()
        cy.get('[class="el-collapse-item is-active"]').contains('View Portfolio').click()
        cy.get('.portfolio-summary > span').contains("Summary")
    }
}
export default InnovationPortfoliosPage