/// <reference types="Cypress" />

class AdminPage{
    
    getAdminHeader() {
        return cy.get('[id="header"]')
    }
}
export default AdminPage