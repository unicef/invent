/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import CountryPage from "../pages/CountryPage"

describe('Initiative Phase / Stage Board schema', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/161704',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('TZ')
        countryPage.getVisibleFlag().should('be.visible')
        countryPage.getCaption().contains('Indicates an initiative that has been in this phase for over 6 months')
        // countryPage.get2PhaseColumnTitle().contains('Opportunity and Ideation')
        // countryPage.get3PhaseColumnTitle().contains('Preparation and Scoping')
        // countryPage.get4PhaseColumnTitle().contains('Analysis and Design')
        // countryPage.get5PhaseColumnTitle().contains('Implementation Planning')
        // countryPage.get6PhaseColumnTitle().contains('Developing or Adapting Solution')
        // countryPage.get7PhaseColumnTitle().contains('Piloting and Evidence Generation')
        // countryPage.get8PhaseColumnTitle().contains('Package and Advocacy')
        // countryPage.get9PhaseColumnTitle().contains('Deploying')
        // countryPage.get10PhaseColumnTitle().contains('Scaling Up')
        countryPage.getMap().should('be.visible')
    })
    
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/164996',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('TZ')
        countryPage.pressBoardSwitch()
        countryPage.getVisibleFlag().should('be.visible')
        countryPage.getCaption().contains('Indicates an initiative that has been in this phase for over 6 months')
        // countryPage.get2PhaseColumnTitle().contains('Initiation')
        // countryPage.get3PhaseColumnTitle().contains('Analysis and Design')
        // countryPage.get4PhaseColumnTitle().contains('Develop and Pilot')
        // countryPage.get5PhaseColumnTitle().contains('Package and Deploy')
        // countryPage.get6PhaseColumnTitle().contains('Completion')
        countryPage.getMap().should('be.visible')
    })
})