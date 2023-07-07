/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import CountryPage from "../pages/CountryPage"
import InventoryPage from "../pages/InventoryPage"

describe('Go to Inventory page from Country Page AND filter on Inventory Page', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165883',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.getInventoryButton().should('be.visible')
        countryPage.getInventoryButton().contains('Afghanistan Inventory')
        countryPage.pressCountryInitiativeButton()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
        //inventoryPage.getInventoryButton().should('be.')
        inventoryPage.getCountryFilter().contains('Afghanistan')

    })

    it('Go to Inventory page from Country Page stages',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.phaseBoardActive()
        countryPage.pressSwitch()
        countryPage.stageBoardActive()
        countryPage.getInventoryButton().should('be.visible')
        countryPage.getInventoryButton().contains('Afghanistan Inventory')
        countryPage.pressCountryInitiativeButton()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
        //inventoryPage.getInventoryButton().should('be.')
        inventoryPage.getCountryFilter().contains('Afghanistan')

    })

    
    // it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165885',() => {
    //     const loginForm = new LoginForm()
    //     loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
    //     const countryPage = new CountryPage()
    //     countryPage.goToCountryPage('AF')
    //     countryPage.getInventoryButton().should('be.visible')
    //     countryPage.pressCountryInitiativeButton()

    // })
})