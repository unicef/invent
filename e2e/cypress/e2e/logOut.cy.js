import LoginPage from "../pages/LoginPage"
import NavigationBar from "../pages/NavigationBar"

describe('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/145746/', () => {
  it('Log out', () => {
    const loginPage = new LoginPage()
    const navigationBar = new NavigationBar()
    loginPage.login(Cypress.env('username'), Cypress.env('password'))
    navigationBar.logOut()
    loginPage.getLoginButton().should('be.visible')    
  })
})