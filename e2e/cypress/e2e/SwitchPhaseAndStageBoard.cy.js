/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import CountryPage from "../pages/CountryPage"

describe('Switch from Phase board to Stage board and vice versa', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/164988',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.getVisibleFlag().should('be.visible')
        countryPage.getMap().should('be.visible')
        countryPage.phaseBoardActive()
        countryPage.pressSwitch()
        countryPage.stageBoardActive()
        countryPage.pressSwitch()
        countryPage.phaseBoardActive()
        countryPage.pressSwitch()
        countryPage.stageBoardActive()
    })
})