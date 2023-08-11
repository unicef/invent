/// <reference types="Cypress" />

class CountryPage {

    //get
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

    getGear() {
        return cy.get('[data-test="sectors-select"]')
    }

    getGearMenuTitle() {
        return cy.get('[class="el-popover__title"]')
    }

    getGearMenuList() {
        return cy.get('[class="ColumnList"]')
    }

    getGearMenuSelectedItems() {
        return cy.get('[class="ColumnList"] > [class="Item Selected"]')
    }

    getGearMenuUnselectedItems() {
        return cy.get('[class="ColumnList"] > [class="Item"]')
    }

    getGearMenuCancel() {
        return cy.get('[data-test="select-sectors-cancel"]')
    }

    getGearMenuDeselectAll() {
        return cy.get('[data-test="select-sectors-deselect-all"]')
    }

    getGearMenuSelectAll() {
        return cy.get('[data-test="select-sectors-select-all"]')
    }

    getGearMenuUpdate() {
        return cy.get('[data-test="select-sectors-update"]')
    }

    getCaption() {
        return cy.get('.caption')
    }

    getMap() {
        return cy.get('.vue2leaflet-map')
    }

    get2PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_46     is-leaf']")
    }

    get3PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_47     is-leaf']")
    }

    get4PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_48     is-leaf']")
    }

    get5PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_49     is-leaf']")
    }

    get6PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_50     is-leaf']")
    }

    get7PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_51     is-leaf']")
    }

    get8PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_52     is-leaf']")
    }

    get9PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_53     is-leaf']")
    }

    get10PhaseColumnTitle() {
        return cy.get("[class='el-table_1_column_54     is-leaf']")
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

    //Press

    pressCountryInitiativeLink() {
        this.getInventoryLink().click()
    }

    pressBoardSwitch() {
        this.getBoardSwitch().click()
    }

    pressHeightSwitch() {
        this.getHeightSwitch().click()
    }

    pressGear() {
        this.getGear().click()
    }

    //Boards

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

    //


    // map

    visibleMap() {
        this.getMap().should('be.visible')
    }

}
export default CountryPage