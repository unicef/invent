/// <reference types="Cypress" />
import HomePage from "./HomePage";

class LoginForm {
    getLoginButton() {
        return cy.contains('Log in')
    }
    login() {
        cy.clearLocalStorage();
        cy.clearCookies();
        cy.visit('/login');
        cy.get('[data-test="signin-username"]').click().type('konstantinos@sword-group.com');
        cy.get('[data-test="signin-password"]').click().type('House-Office+Car*Birthdays99', {log:false});
        cy.get('[data-test="signin-submit"]').click();
        const homePage = new HomePage()
        homePage.getWelcomeSection().should('be.visible')
    }
}

export default LoginForm