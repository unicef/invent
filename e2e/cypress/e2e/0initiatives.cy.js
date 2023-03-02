/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import HomePage from "../pages/HomePage"

describe('User with 0 Initiatives', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147430',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('username0'), Cypress.env('username0'))
        const homePage = new HomePage()
        // Check if the <<Recently Updated Initiatives>> section is visible
        homePage.getInitiativesSection().contains('Recently Updated Initiatives').should('be.visible')
        // Check if the <<My Initiatives>> section is not visible
        homePage.getInitiativesSection().contains('My Initiatives').should('not.exist')
    })
})