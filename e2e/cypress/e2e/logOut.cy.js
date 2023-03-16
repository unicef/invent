/// <reference types="Cypress" />
import NavigationBar from "../pages/NavigationBar"
import LoginForm from "../pages/LoginForm"
import LoginPage from "../pages/LoginPage"


describe('Log out', () => {
  it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/145746/', () => {
    const loginForm = new LoginForm()
    const loginPage = new LoginPage()
    const navigationBar = new NavigationBar()
    loginForm.login(Cypress.env('demousername'), Cypress.env('demopassword'))
    navigationBar.logOut()
    loginPage.getLoginButton().should('be.visible')            
  })
})