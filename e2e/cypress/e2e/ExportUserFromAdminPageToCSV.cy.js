/// <reference types="Cypress" />
/// <reference types="cypress-downloadfile"/>

import AdminLoginForm from "../pages/AdminLoginForm"
import AdminPage from "../pages/AdminPage"
import AdminUsersPage from "../pages/AdminUsersPage"
import AdminChangeUserPage from "../pages/AdminChangeUserPage"

describe('Export user with Job title and Section data on CSV format', () => {

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165892',() => {
        const adminLoginForm = new AdminLoginForm()
        adminLoginForm.loginAdmin(Cypress.env('adminuser'), Cypress.env('adminuser'))
        const adminPage = new AdminPage()
        adminPage.getUsersButton().should('be.visible')
        adminPage.pressUserUsersButton()
        adminPage.verifyURL().should('include', '/auth/user/')
        const adminUsersPage = new AdminUsersPage
        adminUsersPage.getUserPageHeader().should('be.visible')
        adminUsersPage.typeAtSearchBar('FullDataUser')
        adminUsersPage.pressSearchButton()
        adminUsersPage.pressUserCheckbox()
        adminUsersPage.selectExportAction()
        adminUsersPage.selectCSV()
        adminUsersPage.getUserNameLink().should('contain', 'Full Data User')
        //adminUsersPage.pressGoButton() // need to find a solution cypress not wait after click download
        adminUsersPage.pressUserNameLink()
        const adminChangeUserPage = new AdminChangeUserPage
        adminChangeUserPage.getChangeUserPageTitle().should('be.visible')
        cy.scrollTo('bottom')
        adminChangeUserPage.getJobTitleLabel().should('contain', 'Job title:')
        adminChangeUserPage.getJobTitleValue('Chief Beverage Officer')
        adminChangeUserPage.getDepartmentLabel().should('contain', 'Department:')
        adminChangeUserPage.getDepartmentValue('Specialists Parkour Office')
        //adminUsersPage.selectXLS()
        //
        //
        //
        //
    })
})

