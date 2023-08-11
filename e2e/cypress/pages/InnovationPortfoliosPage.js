/// <reference types="Cypress" />

class InnovationPortfoliosPage{

    getInnovationPortfoliosSection(){
        return cy.contains("UNICEF’s Global Innovation Portfolios")
    }

    getPortfolios(){
        return cy.get('[class="portfolio-title"]')
    }

    getSeeAllSolutions(){
        return cy.get('.SolutionsButton > a').contains("See all solutions")
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
        cy.get('[class="active"]').contains("Summary")
    }

    openAllSolution(){
        this.getSeeAllSolutions().click()
        //return cy.get('.SolutionsButton > a').click()
    }


}
export default InnovationPortfoliosPage