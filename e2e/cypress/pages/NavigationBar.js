/// <reference types="Cypress" />
import InitiativePage from "./InitiativePage"
import InventoryPage from "./InventoryPage"
import InnovationPortfoliosPage from "./InnovationPortfoliosPage"
import PortfolioManagerPage from "./PortfolioManagerPage"
import MyInitiativesPage from "./MyInitiativesPage"

class NavigationBar{
    
    // Inventory
    getInventoryButton(){
        return cy.contains('Inventory')
    }
    
    // Innovation Portfolios
    getInnovationPortfoliosButton(){
        return cy.contains('Innovation Portfolios')
    }
    
    // Portfolio Manager
    getPortfolioManagerButton(){
        return cy.contains('Portfolio Manager')
    }
    
    // My Initiatives
    getMyInitiativesButton(){
        return cy.contains('My Initiatives')
    }
    
    // + New Initiative
    getNewInitiativeButton(){
        return cy.contains('New initiative')
    }
    
    //Avatar
    getUserAvatar(){
        return cy.get('[data-test="user-dropdown"]')
    }
    
    // Select Language
    getLanguages(){
        return cy.get('[placeholder="Select language"]')
    }
    
    //Log out
    getLogOutButton(){
        return cy.contains('Logout')
    }
    
    navigateToInventoryPage(){
        this.getInventoryButton().click()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
    }
    
    navigateToInnovationPortfoliosPage(){
        this.getInnovationPortfoliosButton().click()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.getInnovationPortfoliosSection().should('be.visible')
    }
    
    navigateToPortfolioManagerPage(){
        this.getPortfolioManagerButton().click()
        const portfolioManagerPage = new PortfolioManagerPage()
        portfolioManagerPage.getPortfolioManagerSection().should('be.visible')
    }
    
    navigateToMyInitiativesPage(){
        this.getMyInitiativesButton().click()
        const myInitiativesPage = new MyInitiativesPage()
        myInitiativesPage.getMyInitiativesSection().should('be.visible')
    }
    
    navigateToNewInitiativePage(){
        this.getNewInitiativeButton().click() 
        const initiativePage = new InitiativePage()
        initiativePage.getGeneralCard().should('be.visible')         
    }
    
    //Log out
    logOut(){
        this.getUserAvatar().click()
        this.getLogOutButton().click()
    }
}

export default NavigationBar