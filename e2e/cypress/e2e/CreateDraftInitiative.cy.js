/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginPage from "../pages/LoginPage"
import NavigationBar from "../pages/NavigationBar"

describe('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147948/', () => {
    it('Create Draft Iniative',async () => {
        const loginPage = new LoginPage()
        const navigationBar = new NavigationBar()
        loginPage.login(Cypress.env('username'), Cypress.env('password'))
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()            
        initiativePage.typeInitiativeName('Automation Test Initiative')
        initiativePage.selectUnicefOffice('Angola: Dundo')
        initiativePage.typeInitiativeOverview('Initiative created from automation test')

    })
})  
