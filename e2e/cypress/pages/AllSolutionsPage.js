/// <reference types="Cypress" />

class AllSolutionsPage{

    getTitle() {
        return cy.get('h1')
    }

    getInnovationPortfoliosSection() {
        return cy.contains("UNICEF’s Global Innovation Portfolios")
    }

    getAllPortfolios() {
        return cy.get('[class="portfolio-title"]')
    }

    getCreateNewSolution() {
        return cy.get('.SolutionsButton').contains("Create new Solution")
    }

    pressCreateNewSolution() {
        this.getCreateNewSolution().click()
    }

    noCreateNewSolution() {
        this.getCreateNewSolution().should('not.exist');
    }
}
export default AllSolutionsPage