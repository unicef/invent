/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginPage from "../pages/LoginPage"
import NavigationBar from "../pages/NavigationBar"

describe('Create Publish Iniative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147949/',() => {
        const loginPage = new LoginPage()
        const navigationBar = new NavigationBar()
        loginPage.login(Cypress.env('username'), Cypress.env('password'))
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()            
        initiativePage.typeInitiativeName('Automation Publish Initiative')
        initiativePage.selectUnicefOffice('Angola: Dundo')
        initiativePage.typeInitiativeOverview('Automate Publish Initiative')
        initiativePage.typeFocalPointName('Publish Initiative')
        initiativePage.typeFocalPointMail('konstantinos.zagklis@sword-group.com')
        initiativePage.selectSectorInitiative('C4D')
        initiativePage.selectGoalArea('22. Learn')
        initiativePage.selectStartDate('2002-02-02')
        initiativePage.selectPartnerType('Investment')
        initiativePage.typePartnerName('Test test')
        initiativePage.selectSoftwarePLatform('Zalo')
        //initiativePage.saveDraft()
        //initiativePage.getPopWindow().contains('Your draft has been saved successfully')
        //initiativePage.closePopUpWindow()

        
        
    })
})  
