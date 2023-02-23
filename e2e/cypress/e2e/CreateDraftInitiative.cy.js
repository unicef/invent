/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginPage from "../pages/LoginPage"
import NavigationBar from "../pages/NavigationBar"

describe('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147948/', () => {
    it('Create Draft Iniative',() => {
        const loginPage = new LoginPage()
        const navigationBar = new NavigationBar()
        loginPage.login(Cypress.env('username'), Cypress.env('password'))
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()            
        initiativePage.typeInitiativeName('Automation Test Initiative')
        initiativePage.selectUnicefOffice('Angola: Dundo')
        initiativePage.typeFocalPointName('Test test')
        initiativePage.typeFocalPointMail('gerasimos.kourkoumelis@sword-group.com')
        initiativePage.selectPartnerType('Investment')
        initiativePage.typePartnerName('Test test')
        initiativePage.saveDraft()
        initiativePage.getPopWindow().contains('Your draft has been saved successfully')
        initiativePage.closePopUpWindow()

        
        
    })
})  
