/// <reference types="Cypress" />

class AdminPage{
    
    getAdminHeader() {
        return cy.get('[id="site-name"]').contains('UNICEF T4D & Innovation Inventory Portal')
    }

    getUsersButton() {
        return cy.get('[class="model-user"]').contains('Users')
    }

    pressUserUsersButton() {
        this.getUsersButton().click()
    }

    verifyURL() {
        return cy.url()
    }

}
export default AdminPage