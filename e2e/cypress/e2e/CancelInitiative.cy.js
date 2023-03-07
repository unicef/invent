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
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/148113/',() => {
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

    })
})  
