/// <reference types="Cypress" />
import HomePage from "./HomePage";

class LoginPage {
    getLoginButton() {
        return cy.contains('Login')
    }

    login(username, password) {
        cy.visit('/');
        cy.clearLocalStorage();
        cy.clearCookies();
        this.getLoginButton().click()
        const sentArgs = { email: username, pass: password }
        cy.origin(`https://login.microsoftonline.com`,  { args: sentArgs },({ email, pass }) => {
            cy.get('[type="email"]').type(email);
            cy.get('[type="submit"]').click();
            cy.get('[type="password"]').type(pass, {log:false});
            cy.get('[type="submit"]').click();
        });
        const homePage = new HomePage()
        homePage.getWelcomeSection().should('be.visible')
    }

    openPage() {
        cy.visit('/');
        cy.clearLocalStorage();
        this.getLoginButton().click()
        cy.origin(`https://login.microsoftonline.com`, () => {
            cy.get('[type="submit"]').click();
        });
    }

    getNextButton() {
        return cy.contains('Next')
    }
    
    getSignInButton() {
        return cy.get('#lightbox').contains('Sign in')
    }

    setEmail(username) {
        cy.get('[type="email"]').type(username)
        this.getNextButton().click()
    }

    setPassword(password) {
        cy.get('[type="password"]').type(password)
        this.getSignInButton().click()
    }

    getEnterPasswordHeader() {
        return cy.get('#loginHeader > div').contains("Enter password")
    }

    getUsernameError() {
        return cy.get('#usernameError')
    }

    getPasswordError() {
        return cy.get('#passwordError')
    }












    // openPage2(username, password) {
    //     cy.visit('/');
    //     cy.clearLocalStorage();
    //     cy.clearCookies();
    //     this.getLoginButton().click()
    //     const sentArgs = { email: username, pass: password }
    //     cy.origin(`https://login.microsoftonline.com`,  { args: sentArgs },({ email, pass })=> {
    //         cy.get('[type="email"]').type(email);
    //         cy.get('[type="submit"]').click();
    //         cy.get('[type="password"]').type(pass, {log:false});
    //         cy.get('[type="submit"]').click();
    //     });



}

export default LoginPage