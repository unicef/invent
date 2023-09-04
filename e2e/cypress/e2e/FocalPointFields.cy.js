/// <reference types="Cypress" />
import InitiativePage from "../pages/InitiativePage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"

describe('Exploratory for Focal Point Fields', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/XXXX/',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('noportfolio'), Cypress.env('noportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()
        initiativePage.getFocalPointLabel().contains('Who is the focal point for this initiative?')
        initiativePage.emptyFocalPointField()
        initiativePage.getFocalPointHint().contains('The focal point is the team member who is leading this work, and will act as the point of contact for anyone wishing to connect with the team.')
        initiativePage.getTeamMembersLabel().contains('Who are the team members for this initiative?')
        initiativePage.getTeamMembersField().contains(Cypress.env('noportfolio'))
        initiativePage.getTeamMembersHint().contains('These team members can modify entries on "+ New Initiative" page.')
        initiativePage.getReceiveUpdatesLabel().contains('Who should receive updates that this initiative has been added or modified?')
        initiativePage.emptyReceiveUpdatesField()
        initiativePage.getReceiveUpdatesHint().contains('These team members will receive a notification when an initiative has been added.')
    })
})

describe('Add member as a focal point on a New Initiative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/159933/',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('noportfolio'), Cypress.env('noportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()
        initiativePage.typeFocalPointField(Cypress.env('globalportfolio'))
        initiativePage.getFocalPointField().contains(Cypress.env('globalportfolio')).should('have.length', 1)
        initiativePage.getTeamMembersField().should('contain', (Cypress.env('globalportfolio'))).and('contain', (Cypress.env('noportfolio')))
    })
})

describe('Add member as a Team Member on a New Initiative', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/159936/',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('noportfolio'), Cypress.env('noportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()
        initiativePage.getTeamMembersField().should('contain', (Cypress.env('noportfolio')))
        initiativePage.typeTeamMembersField(Cypress.env('randomusername'))
        initiativePage.getTeamMembersField().should('contain', (Cypress.env('randomusername'))).and('contain', (Cypress.env('noportfolio')))
    })
})  