/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm" 
import LoginPage from "../pages/LoginPage"

describe('Unathorized User from Login Form', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/152873',() => {
        const loginForm = new LoginForm()
        loginForm.start()
        loginForm.logInButton().click()
        loginForm.getMissingUsernameError().contains('This field is required')
        loginForm.getMissingPasswordError().contains('This field is required')
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/152874',() => {
        const loginForm = new LoginForm()
        loginForm.start()
        loginForm.unathorizedusername(Cypress.env('wrongusername'))
        loginForm.logInButton().click()
        loginForm.getMissingPasswordError().contains('This field is required')
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/152875',() => {
        const loginForm = new LoginForm()
        loginForm.start()
        loginForm.unathorizedpassword(Cypress.env('wrongusername'))
        loginForm.logInButton().click()
        loginForm.getMissingUsernameError().contains('This field is required')
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/152876',() => {
        const loginForm = new LoginForm()
        loginForm.start()
        loginForm.unathorizedusername(Cypress.env('wrongusername'))
        loginForm.unathorizedpassword(Cypress.env('wrongusername'))
        loginForm.logInButton().click()
        loginForm.getWrongPasswordError().contains(('Unable to log in with provided credentials.'))
    })
})

describe('Unathorized User from Login Page', () => {

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/152897',() => {
        const loginPage = new LoginPage()
        loginPage.clearBroswer()
        loginPage.openPage()
        loginPage.getUsernameError().contains('Enter a valid email address, phone number, or Skype name.')
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/145742 (step 3)',() => {
        const loginPage = new LoginPage()
        loginPage.clearBroswer()
        loginPage.openPage()
        loginPage.setEmail(Cypress.env('wrongformatusername'))
        loginPage.getUsernameError().contains("Enter a valid email address, phone number, or Skype name.")
    })

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/145742 (step 4)',() => {
        const loginPage = new LoginPage()
        loginPage.clearBroswer()
        loginPage.openPage()
        loginPage.setEmail(Cypress.env('wrongusername'))
        loginPage.getUsernameError().contains("We couldn't find an account with that username.")
    })
})