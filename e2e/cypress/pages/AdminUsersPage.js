/// <reference types="Cypress" />

class AdminUsersPage{

    getUserPageHeader() {
        return cy.get('#content > h1').contains('Select user to change')
    }

    getActionsMenu() {
        return cy.get('[name="action"]')
    }

    getFromatMenu() {
        return cy.get('[name="file_format"]')
    }

    getSearchBar() {
        return cy.get('[id="searchbar"]')
    }

    getButton() {
        return cy.get('[type="submit"]')
    }

    getUserCheckbox() {
        return cy.get('[class="action-select"]')
    }

    getUserNameLink() {
        return cy.get('[class="field-userprofile"]')
    }

    typeAtSearchBar(user) {
        this.getSearchBar().type(user)
    }

    pressSearchButton() {
        this.getButton().contains('Search').click()
    }

    pressGoButton() {
        //this.getButton().contains('Go').click()
        this.getButton().contains('Go').then(el => { 
            el.attr('Go', '')
          }).click()
    }

    pressUserCheckbox() {
        this.getUserCheckbox().click()
    }

    pressUserNameLink() {
        this.getUserNameLink().click()
    }

    selectExportAction() {
        this.getActionsMenu().select('Export selected users').should('have.value', 'export_admin_action')
    }

    selectDeleteAction () {
        this.getActionsMenu().select('Delete selected users').should('have.value', 'delete_selected')
    }

    selectCSV () {
        this.getFromatMenu().select('csv').should('have.value', '0')
    }

    selectXLS () {
        this.getFromatMenu().select('xls').should('have.value', '1')
    }

}
export default AdminUsersPage