/// <reference types="Cypress" />

class InventoryPage {

    getListView() {
        return cy.get('class="DashboardArea"')
    }

}
export default InventoryPage