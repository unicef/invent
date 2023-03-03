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
        cy.origin(`https://login.microsoftonline.com`,  { args: sentArgs },({ email, pass })=> {
            cy.get('[type="email"]').type(email);
            cy.get('[type="submit"]').click();
            cy.get('[type="password"]').type(pass, {log:false});
            cy.get('[type="submit"]').click();
        });
        const homePage = new HomePage()
        homePage.getWelcomeSection().should('be.visible')
    }



}

export default LoginPage