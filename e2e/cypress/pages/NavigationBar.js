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

    navigateToInventory(){
        this.getInventoryButton().click()
        const inventoryPage = new InventoryPage()
        inventoryPage.getListView().should('be.visible')
    }

    // Innovation Portfolios
    getInnovationPortfoliosButton(){
        return cy.contains('Innovation Portfolios')
    }

    navigateToInnovationPortfolios(){
        this.getInnovationPortfoliosButton().click()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.getInnovationPortfoliosSection().should('be.visible')
    }

    // Portfolio Manager
    getPortfolioManagerButton(){
        return cy.contains('Portfolio Manager')
    }

    navigateToPortfolioManagerPage(){
        this.getPortfolioManagerButton().click()
        const portfolioManagerPage = new PortfolioManagerPage()
        portfolioManagerPage.getPortfolioManagerSection().should('be.visible')
    }

    // My Initiatives
    getMyInitiativesButton(){
        return cy.contains('My Initiatives')
    }

    navigateToMyInitiativesPage(){
        this.getMyInitiativesButton().click()
        const myInitiativesPage = new MyInitiativesPage()
        myInitiativesPage.getMyInitiativesSection().should('be.visible')
    }

    // + New Initiative
    getNewInitiativeButton(){
        return cy.contains('New initiative')
    }

    navigateToNewInitiativePage(){
        this.getNewInitiativeButton().click() 
        const initiativePage = new InitiativePage()
        initiativePage.getGeneralCard().should('be.visible')         
    }
    
    //Avatar
    getUserAvatar(){
        return cy.get('[data-test="user-dropdown"]')
    }

    //Log out
    getLogOutButton(){
        return cy.contains('Logout')
    }
    
    logOut(){
        this.getUserAvatar().click()
        this.getLogOutButton().click()
    }
}

export default NavigationBar