/// <reference types="Cypress" />

class CountryPage {
    goToCountryPage(countryCode) {
        cy.visit('en/' + countryCode);
    }

    getVisibleFlag() {
        return cy.get('.flag-info')
    }

    getSwitch() {
        return cy.get('.el-switch__core')
    }

    getCaption() {
        return cy.get('.caption')
    }

    getMap() {
        return cy.get('.vue2leaflet-map')
    }

    get2PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_2     is-leaf']")
    }

    get3PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_3     is-leaf']")
    }

    get4PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_4     is-leaf']")
    }

    get5PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_5     is-leaf']")
    }

    get6PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_6     is-leaf']")
    }

    get7PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_7     is-leaf']")
    }

    get8PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_8     is-leaf']")
    }

    get9PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_9     is-leaf']")
    }

    get10PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_10     is-leaf']")
    }











    



















    //

    visibleMap() {
        this.getMap().should('be.visible')
    }

    pressSwitch() {
        this.getSwitch().click()
    }

}
export default CountryPage