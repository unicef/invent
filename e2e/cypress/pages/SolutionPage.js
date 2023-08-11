/// <reference types="Cypress" />

class SolutionPage{

    getGeneralSection(){
        return cy.get('[class="CardTitle"]').contains("1. General")
    }

    getActivitySection(){
        return cy.get('#activity-and-reach').contains("Activity and Reach")
    }

    getViewTitle(){
        return cy.get('[class="PageTitle"]')
    }

    getBreadcrumb(){
        return cy.get('[class="breadcrumb"]')
    }

    getURL(){
        return cy.url()
    }

    getSolutionName(){}

    getNameSection(){}

    getPhaseSection(){}

    getOpenSourceSection(){}

    getLeraningSection(){}

    getInnovationTable(){}

}
export default SolutionPage