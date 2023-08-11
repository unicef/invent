/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import HomePage from "../pages/HomePage"

describe('User with 0 Initiatives', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147434',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('threeinitiatives'), Cypress.env('threeinitiatives'))
        const homePage = new HomePage()
        // Check if the <<Recently Updated Initiatives>> section is visible
        homePage.getInitiativesSection().contains('Recently Updated').should('not.exist')
        // Check if the <<My Initiatives>> section is visible
        homePage.getInitiativesSection().contains('My Initiatives').should('be.visible')
        homePage.getSeeAll().contains('See all (3)').should('be.visible')
        // Count My initiatives
        homePage.getInitiativeCards().should('have.length', 3)
    })
})