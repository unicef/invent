/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import InventoryPage from "../pages/InventoryPage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"
import HomePage from "../pages/HomePage"
import InnovationPortfoliosPage from "../pages/InnovationPortfoliosPage"
import MyInitiativesPage from "../pages/MyInitiativesPage"
import PortfolioManagerPage from "../pages/PortfolioManagerPage"


describe('Cancel New Iniative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147949/',() => {
        const loginForm = new LoginForm()
        const navigationBar = new NavigationBar()
        loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()
        initiativePage.typeInitiativeName('Cancel New Initiative')
        initiativePage.cancelInitiative()

        //Verify return to Home page
        const homePage = new HomePage()
        homePage.getWelcomeSection()

        
        // navigationBar.navigateToNewInitiativePage()
        // initiativePage.typeInitiativeName('Cancel New Initiative 2')
        // //Verify Inventory Page
        // const inventoryPage = new InventoryPage()
        // navigationBar.navigateToInventory()
        // inventoryPage.getListView()

        // // Try to create New Initiative
        // initiativePage.typeInitiativeName('Cancel New Initiative 3')
        // navigationBar.navigateToInventory()
        // //Discard New Initiative and go to Innovation Portfolios Page
        // const innovationPortfoliosPage = new InnovationPortfoliosPage()
        // navigationBar.navigateToInnovationPortfolios
        // innovationPortfoliosPage.getInnovationPortfoliosSection()

        // // Try to create New Initiative
        // initiativePage.typeInitiativeName('Cancel New Initiative 4')
        // navigationBar.navigateToInventory()
        // //Discard New Initiative and go to My Initiatives Page
        // const myInitiativesPage = new MyInitiativesPage()
        // navigationBar.navigateToMyInitiativesPage
        // myInitiativesPage.getMyInitiativesSection()

        // // Try to create New Initiative
        // initiativePage.typeInitiativeName('Cancel New Initiative 5')
        // navigationBar.navigateToInventory()
        // //Discard New Initiative and go to Portfolio Manager Page
        // const portfolioManagerPage = new PortfolioManagerPage()
        // navigationBar.navigateToPortfolioManagerPage
        // portfolioManagerPage.getPortfolioManagerSection()

    })
})  
