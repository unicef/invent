/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import HomePage from "../pages/HomePage"
import Requests from "../support/Requests"

describe('User with 1 Initiatives', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147434',() => {
        const loginForm = new LoginForm()
        const requests = new Requests()
        loginForm.login(Cypress.env('username1'), Cypress.env('username1'))
        const homePage = new HomePage()
        requests.getInitiativesList().then((response)=>{
            homePage.getInitiativeCardsSmall().contains(response.body.results.projects[0].name)
            homePage.getInitiativeCardsSmall().contains(response.body.results.projects[1].name)
            homePage.getInitiativeCardsSmall().contains(response.body.results.projects[2].name)
        })
        requests.getMyInitiativesList().then((response)=>{
            cy.log(response.body.results[0].name)
            homePage.getInitiativeCards().contains(response.body.results[0].name)
        })
        // Check if the <<Recently Updated Initiatives>> section is visible
        homePage.getInitiativesSection().contains('Recently Updated').should('be.visible')
        // Check if the <<My Initiatives>> section is visible
        homePage.getInitiativesSection().contains('My Initiatives').should('be.visible')
        homePage.getSeeAll().contains('See all (1)').should('be.visible')
        // Count My initiatives
        homePage.getInitiativeCards().should('have.length', 1)
        // Count Recently update initiatives
        homePage.getInitiativeCardsSmall().should('have.length', 3)
   


    })
})