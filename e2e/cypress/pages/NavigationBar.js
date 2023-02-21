/// <reference types="Cypress" />
import InitiativePage from "./InitiativePage"

class NavigationBar{

    getUserAvatar(){
        return cy.get('[data-test="user-dropdown"]')
    }

    getLogOutButton(){
        return cy.contains('Logout')
    }

    getNewInitiativeButton(){
        return cy.contains('New initiative')
    }

    logOut(){
        this.getUserAvatar().click()
        this.getLogOutButton().click()
    }

    navigateToNewInitiativePage(){
        this.getNewInitiativeButton().click() 
        const initiativePage = new InitiativePage()
        initiativePage.getGeneralCard().should('be.visible')         
    }



}
export default NavigationBar