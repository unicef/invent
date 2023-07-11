/// <reference types="Cypress" />
import HomePage from "../pages/HomePage"
import InitiativePage from "../pages/InitiativePage"
import InventoryPage from "../pages/InventoryPage"
import LoginForm from "../pages/LoginForm"
import LoginPage from "../pages/LoginPage"
import MyInitiativesPage from "../pages/MyInitiativesPage"
import NavigationBar from "../pages/NavigationBar"
import SolutionPage from "../pages/SolutionPage"
import Requests from "../support/Requests"
import CountryPage from "../pages/CountryPage"
import AdminLoginForm from "../pages/AdminLoginForm"


describe('Demo test', () => {

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165952',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.getGear().should('be.visble')
        countryPage.pressBoardSwitch()
        countryPage.getGear().should('be.visble')
        countryPage.pressHeightSwitch()
        countryPage.getGear().should('be.visble')



        countryPage.pressGear()

    })
})

