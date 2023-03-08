/// <reference types="Cypress" />
import NavigationBar from "../pages/NavigationBar"
import LoginForm from "../pages/LoginForm"


describe('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/145746/', () => {
  it('Log out', () => {
    const loginForm = new LoginForm()
    const navigationBar = new NavigationBar()
    loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
    navigationBar.logOut()
    loginPage.getLoginButton().should('be.visible')            
  })
})