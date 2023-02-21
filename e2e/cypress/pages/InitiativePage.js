/// <reference types="Cypress" />

class InitiativePage {

    getGeneralCard() {
        return cy.get('[id="general"]')
    }

    getInitiativeName() {
        return cy.get('input[data-as-name="Name"]')
    }

    getUnicefOffice(){
        return cy.get('input[placeholder="UNICEF office"]')
    }

    getIniativeOverview(){
        return cy.get('textarea[data-vv-name="overview"]')
    }

    getFocalPointName(){
        return cy.get('input[data-vv-name="contact_name"]')
    }

    getFocalPointMail(){
        return cy.get('input[data-vv-name="contact_email"]')
    }

    typeInitiativeName(name){
        this.getInitiativeName().type(name)
    }

    typeInitiativeOverview(overview){
        this.getIniativeOverview().type(overview)
    }

    selectUnicefOffice(office){
        this.getUnicefOffice().click()
        this.getUnicefOffice().type(office) 
        cy.contains(office).click()
    }
}
export default InitiativePage