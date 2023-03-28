/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"

describe('Create Draft Iniative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/147948/',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
        const navigationBar = new NavigationBar()
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
        initiativePage.getDraftLabel().should('be.visible')
        initiativePage.getPublishLabel().should('not.exist')
        initiativePage.getViewDraftButton().should('be.visible').and('not.be.enabled')
        initiativePage.getViewPublishButton().should('be.visible').and('not.be.enabled')
        initiativePage.getPublishButton().should('be.visible').and('be.enabled')
    })
})  
