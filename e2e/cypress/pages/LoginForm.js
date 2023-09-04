/// <reference types="Cypress" />
import HomePage from "./HomePage";

class LoginForm {

    login(username, password) {
        cy.clearCookies()
        cy.getCookies().should('be.empty')
        cy.clearLocalStorage()
        cy.getAllLocalStorage().should('be.empty')
        cy.clearAllSessionStorage({log: true})
        cy.visit('en/-/login')
        cy.get('[data-test="signin-username"]').click().type(username)
        cy.get('[data-test="signin-password"]').click().type(password)
        cy.get('[data-test="signin-submit"]').click()
        const homePage = new HomePage()
        homePage.getWelcomeSection().should('be.visible')
    }

    start() {
        cy.clearCookies()
        cy.getCookies().should('be.empty')
        cy.clearLocalStorage()
        cy.getAllLocalStorage().should('be.empty')
        cy.clearAllSessionStorage({log: true})
        cy.visit('en/-/login')
    }

    clearBroswerData() {
        cy.clearCookies()
        cy.getCookies().should('be.empty')
        cy.clearLocalStorage()
        cy.getAllLocalStorage().should('be.empty')
        cy.clearAllSessionStorage({log: true})
    }
    
    logInButton() {
        return cy.get('[data-test="signin-submit"]')
    }

    getMissingUsernameError() {
        return cy.get('[data-test="signin-username-item"]')
    }

    getMissingPasswordError() {
        return cy.get('[data-test="signin-password-item"]')
    }
    
    unathorizedusername(username) {
        cy.get('[data-test="signin-username"]').click().type(username)
    }

    unathorizedpassword(password) {
        cy.get('[data-test="signin-password"]').click().type(password)
    }

    getWrongPasswordError() {
        return cy.get('[data-test="signin-error"]')
    }
    
    getLoginError() {
        return cy.get('.el-form-item__error')
    }
}
export default LoginForm