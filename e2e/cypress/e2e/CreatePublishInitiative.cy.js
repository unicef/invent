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
        initiativePage.typeInitiativeName('Automation Publish Initiative 35')
        initiativePage.selectUnicefOffice('Angola: Dundo')
        initiativePage.typeInitiativeOverview('Automate Publish Initiative')
        initiativePage.typeFocalPointName('Publish Initiative')
        initiativePage.typeFocalPointMail('konstantinos.zagklis@sword-group.com')
        //initiativePage.typeModifyInitiative('gerasimos.kourkoumelis@sword-group.com')
        initiativePage.selectSectorInitiative('ICT')
        initiativePage.selectGoalArea('22. Learn')
        initiativePage.selectStartDate('2002-02-02')
        initiativePage.selectPartnerType('Investment')
        initiativePage.typePartnerName('Automation Test Partner')
        initiativePage.selectSoftwarePLatform('2C2P')
        initiativePage.saveDraft()
        initiativePage.getPopWindow().contains('Your draft has been saved successfully')
        initiativePage.closePopUpWindow()
        initiativePage.publishInitiative()
        initiativePage.getPopWindow().contains('Your draft has been published successfully')
        initiativePage.closePopUpWindow()

    })
})  
