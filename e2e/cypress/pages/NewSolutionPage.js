/// <reference types="Cypress" />

class NewSolutionPage {

    getTitle() {
        return cy.get('.PageTitle')
    }
	
    getNewSolutionTitle(){
        return cy.get('[data-test="solution-name-input"]')
    }

    getSolutionName() {
        return cy.get('.el-input > [data-test="solution-name-input"]')
    }

    getAddPortfolio(){
        return cy.get('[data-test="add-portfolio-row-button"]')
    }

    getOpenSourceFrontierTech(){
        return cy.get('[data-test="solution-tech-checkbox"]')
    }

    getLearningInvestment(){
        return cy.get('[data-test="solution-learning-checkbox"]')
    }
    
    getInnovationPortfolio(){
        return cy.get('[data-test="portfolio-select-single-0"]')
    }

    getProblemStatements(){
        return cy.get('[data-test="problem-statement-0"]')
    }

    getSaveButton(){
        return cy.get('.NavigationActions > .el-button--primary')
    }

    getCancelButton(){
        return cy.get('.Cancel')
    }

    getCloseButton(){
        return cy.get('.el-message-box__close')
    }
 
    //

	typeSolutionName(name) {
        this.getSolutionName().type(name)
    }
    
    pressAddPortfolio(){
        this.getAddPortfolio().click()
    }

    setOpenSourceFrontierTech(){
        this.getOpenSourceFrontierTech().click()
    }

    setLearningInvestment(){
        this.getLearningInvestment().click()
    }

    setInnovationPortfolio(portfolio){
        this.getInnovationPortfolio().click()
        //
        this.getInnovationPortfolio().scrollIntoView().should('be.visible')
        this.getInnovationPortfolio().type(portfolio)
        cy.get('li').eq(portfolio).last().click({force: true})
        //cy.get('.PortfolioSelectorPopper').eq(portfolio).should('have.value', portfolio).click()

        //cy.get('[class="el-select-dropdown__item"]').eq('portfolio').click({force: true})
        //cy.get('[class="el-select-dropdown__item"]').first().click({force: true})
        //cy.get('select[name="dropdown"]').select('option').eq(0).click();
        //this.getInnovationPortfolio().click({force: true})
    }

    setProblemStatements(problem){
        this.getProblemStatements().click()
        this.getProblemStatements().type(problem)
        this.getProblemStatements().scrollIntoView()
        cy.get('li').last().click({force: true})
        this.getProblemStatements().click()
    }












    saveSolution() {
        this.getSaveButton().click()
    }
	
    cancelSolution() {
        this.getCancelButton().click()
    }

    closePopUpWindow(){
        this.getCloseButton().click()
    }

}
export default NewSolutionPage