/// <reference types="Cypress" />

class InitiativePage {

    getGeneralCard() {
        return cy.get('[id="general"]')
    }

    getInitiativeName() {
        return cy.get('input[data-as-name="Name"]')
    }

    getUnicefOffice() {
        return cy.get('input[placeholder="UNICEF office"]')
    }

    getIniativeOverview() {
        return cy.get('textarea[data-vv-name="overview"]')
    }

    getFocalPointName() {
        return cy.get('input[data-vv-name="contact_name"]')
    }

    getFocalPointMail() {
        return cy.get('input[data-vv-name="contact_email"]')
    }

    typeInitiativeName(name) {
        this.getInitiativeName().type(name)
    }

    typeInitiativeOverview(overview) {
        this.getIniativeOverview().type(overview)
    }

    getPartnerType() {
        return cy.get('div[data-vv-as="Partner Type"]')
    }

    getPartnerName() {
        return cy.get('data-vv-name="partner_name0"')
    }



    selectUnicefOffice(office) {
        this.getUnicefOffice().click()
        this.getUnicefOffice().type(office)
        cy.contains(office).click()
    }

    typeFocalPointName(name) {
        this.getFocalPointName().type(name)
    }

    typeFocalPointMail(email) {
        this.getFocalPointMail().type(email)
    }

    selectPartnerType(partner) {
        this.getPartnerType().click()
        this.getPartnerType().type(partner)
        cy.contains(partner).click()
    }

    typePartnerName(name) {
        this.getPartnerName().type(name)
    }

}
export default InitiativePage