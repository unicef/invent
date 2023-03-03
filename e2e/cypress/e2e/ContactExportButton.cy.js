/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"
import InventoryPage from "../pages/InventoryPage"

describe('Contact & Export Button', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/146446',() => {
        // Contact Button (enable/disable)
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInventoryPage()
        const inventoryPage = new InventoryPage()
        inventoryPage.getSelectButton().should('be.visible').and('be.enabled')
        inventoryPage.getContactButton().should('be.visible').should('not.be.enabled')
        inventoryPage.getSelectButton().click()
        inventoryPage.getContactButton().should('be.visible').should('be.enabled')

    })
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/146385', () => {
        // Export Button (enable/disable)
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInventoryPage()
        const inventoryPage = new InventoryPage()
        // inventoryPage.getSelectButton().click()
        inventoryPage.getExportButton().should('be.visible').should('not.be.enabled')
        inventoryPage.getSelectButton().click()
        inventoryPage.getExportButton().should('be.visible').should('be.enabled')

    })
})