/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import CountryPage from "../pages/CountryPage"

describe('Explore Phase And Stage board with no Active Initiative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/164997',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('GR')
        countryPage.getVisibleFlag().should('be.visible')
        countryPage.getVisibleFlag().contains('Welcome to country view. This view is scoped to show all initiatives of the chosen country')
        countryPage.getCaption().contains('Indicates an initiative that has been in this phase for over 6 months')
        countryPage.getMap().should('be.visible')
        countryPage.isPhasesTableEmpty()
        countryPage.getBoardSwitch()
        countryPage.isStagesTableEmpty()
    })
})