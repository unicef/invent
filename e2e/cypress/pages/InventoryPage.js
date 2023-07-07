/// <reference types="Cypress" />

class InventoryPage {

    getListView() {
        return cy.get('.ActionBarTabs > .el-row')
    }

    // Check all buttons Select Export Contact
    getSelectButton() {
        return cy.get('[class="TableExportOptions el-col el-col-24"]').contains('Select')
    }

    getExportButton() {
        return cy.get('[class="TableExportOptions el-col el-col-24"]').contains('Export')
    }

    getContactButton() {
        return cy.get('[class="TableExportOptions el-col el-col-24"]').contains('Contact')
    }

    getInventoryButton() {
        return cy.get(':nth-child(1) > .HeaderBtn')
    }

    getCountryFilter() {
        return cy.get('[class="el-select CountrySelector"]')
    }

}
export default InventoryPage