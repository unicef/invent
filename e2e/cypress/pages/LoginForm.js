/// <reference types="Cypress" />
import HomePage from "./HomePage";

class LoginForm {
    getLoginButton() {
        return cy.contains('Log in')
    }
    login(username, password) {
        cy.clearLocalStorage();
        cy.clearCookies();
        cy.visit('/login');
        cy.get('[data-test="signin-username"]').click().type(username);
        cy.get('[data-test="signin-password"]').click().type(password);
        cy.get('[data-test="signin-submit"]').click();
        const homePage = new HomePage()
        homePage.getWelcomeSection().should('be.visible')
    }
}

export default LoginForm