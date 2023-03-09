/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"

describe('Create Publish Iniative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/148113/',() => {
        const loginForm = new LoginForm()
        const navigationBar = new NavigationBar()
        loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()
        initiativePage.typeInitiativeName('Automation Publish Initiative'+(Math.floor(Math.random() * 1000000000000000)).toString())
        initiativePage.selectUnicefOffice('Angola: Dundo')
        initiativePage.typeInitiativeOverview('Automate Publish Initiative')
        initiativePage.typeFocalPointName('Publish Initiative')
        initiativePage.typeFocalPointMail('konstantinos.zagklis@sword-group.com')
        initiativePage.selectSectorInitiative('C4D')
        initiativePage.selectGoalArea('22. Learn')
        initiativePage.selectStartDate('2002-02-02')
        initiativePage.selectPartnerType('Investment')
        initiativePage.typePartnerName('Automation Test Partner')
        initiativePage.selectSoftwarePLatform('2C2P')
        initiativePage.saveDraft()
        initiativePage.getPopWindow().contains('Your draft has been saved successfully')
        initiativePage.closePopUpWindow()
        initiativePage.getDraftLabel().should('be.visible')
        initiativePage.getPublishLabel().should('not.exist')
        initiativePage.publishInitiative()
        initiativePage.getPopWindow().contains('Your draft has been published successfully')
        initiativePage.closePopUpWindow()
        initiativePage.getPublishLabel().should('be.visible')
        initiativePage.getDraftLabel().should('not.exist')
        initiativePage.getViewDraftButton().should('be.visible').and('be.enabled')
        initiativePage.getViewPublishButton().should('be.visible').and('not.be.enabled')
        initiativePage.getPublishButton().should('be.visible').and('be.enabled').and('be.enabled')
        initiativePage.getPublishAsLatestButton().contains('Publish as latest').should('be.visible')
        initiativePage.getGoToDashboard().should('be.visible')

        

    })
})  
