/// <reference types="Cypress" />
import AdminPage from "./AdminPage"

class AdminLoginForm {

    loginAdmin(username, password) {
        cy.clearLocalStorage()
        cy.clearCookies()
        cy.visit('admin')
        cy.get('[for="id_username"]').click().type(username)
        cy.get('[for="id_password"]').click().type(password)
        cy.get('[class="submit-row"]').click()
        const adminPage = new AdminPage()
        adminPage.getAdminHeader().should('be.visible')
    }
}

export default AdminLoginForm