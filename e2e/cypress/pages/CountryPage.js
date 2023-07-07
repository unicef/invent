/// <reference types="Cypress" />

class CountryPage {
    goToCountryPage(countryCode) {
        cy.visit('en/' + countryCode);
    }

    getVisibleFlag() {
        return cy.get('[class="flag-info"]')
    }

    getBoardSwitch() {
        return cy.get('[data-test="phases-stages-switch"]')
    }

    getHeightSwitch() {
        return cy.get('[data-test="height-switch"]')
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

    getPhasesTable() {
        return cy.get('[class="el-table__body-wrapper is-scrolling-left"]')
    }

    getStagesTable() {
        return cy.get('[class="el-table__body-wrapper is-scrolling-none"]')
    }

    getInventoryLink() {
        return cy.get('[data-test="country-inventory-link"]')
    }

    phaseBoardActive() {
        this.getBoardSwitch().should('have.class', 'el-switch Switch is-checked')
    }

    stageBoardActive() {
        this.getBoardSwitch().should('have.class', 'el-switch Switch')
    }

    isPhasesTableEmpty() {
        this.getPhasesTable().contains('No initiatives available')
    }

    isStagesTableEmpty() {
        this.getStagesTable().contains('No initiatives available')
    }

    visibleMap() {
        this.getMap().should('be.visible')
    }

    pressCountryInitiativeLink() {
        this.getInventoryLink().click()
    }

    pressBoardSwitch() {
        this.getBoardSwitch().click()
    }

    pressHeightSwitch() {
        this.getHeightSwitch().click()
    }

}
export default CountryPage