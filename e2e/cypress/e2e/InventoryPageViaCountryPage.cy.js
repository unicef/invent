/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import CountryPage from "../pages/CountryPage"
import InventoryPage from "../pages/InventoryPage"

describe('Go to Inventory page from Country Page AND filter on Inventory Page', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165883',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('TZ')
        countryPage.getInventoryLink().should('be.visible')
        countryPage.getInventoryLink().contains("See this country's initiatives in the inventory")
        countryPage.pressCountryInitiativeLink()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165885',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.getInventoryLink().should('be.visible')
        countryPage.getInventoryLink().contains("See this country's initiatives in the inventory")
        countryPage.pressCountryInitiativeLink()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
        inventoryPage.getCountryFilter().contains('Afghanistan')
    })
})