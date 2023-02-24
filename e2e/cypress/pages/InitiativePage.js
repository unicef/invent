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

    getSectorInitiative() {
        return cy.get('[data-vv-name="unicef_sector"]').click()
    }

    getGoalArea() {
        return cy.get('[data-vv-name="goal_area"]').click()
    }

    getStartDate() {
        return cy.get('[data-vv-name="start_date"]').click()
    }

    getPartnerType() {
        return cy.get('div[data-vv-as="Partner Type"]')
    }

    getPartnerName() {
        return cy.get('input[data-vv-as="Partner Name"]')
    }

    getSoftwarePLatform(){
        return cy.get('[data-vv-name="platforms"]')
    }

    typeInitiativeName(name) {
        this.getInitiativeName().type(name)
    }

    typeInitiativeOverview(overview) {
        this.getIniativeOverview().type(overview)
    }

    typeFocalPointName(name) {
        this.getFocalPointName().type(name)
    }

    typeFocalPointMail(email) {
        this.getFocalPointMail().type(email)
    }

    typePartnerName(name) {
        this.getPartnerName().type(name)
    }

    getSaveDraftButton() {
        return cy.get('[class="el-button el-button--primary el-button--medium SaveDraft NewProject"]')
    }

    getPopWindow(){
        return cy.get('[role="dialog"]')
    }

    getCloseButton(){
        return cy.contains('Close')
    }

    selectUnicefOffice(office) {      
        this.getUnicefOffice().click()
        this.getUnicefOffice().type(office)
        this.getUnicefOffice().scrollIntoView()
        cy.contains(office).click({force:true})
    }

    selectSectorInitiative(sector) {
        this.getSectorInitiative().click({force:true}).type(sector)
        cy.contains(sector).click()
        this.getSectorInitiative().click()
   }

   selectGoalArea(goalarea) {
       this.getGoalArea().click().type(goalarea)
       cy.contains(goalarea).click()
   }

   selectStartDate(startdate) {
       this.getStartDate().click()
       this.getStartDate().type(startdate).type('{enter}')
   }

    selectPartnerType(partner) {
        this.getPartnerType().click({force:true})
        this.getPartnerType().type(partner)
        this.getPartnerType().scrollIntoView()
        cy.contains(partner).click()
    }

    selectSoftwarePLatform(software) {
        this.getSoftwarePLatform().click({force:true})
        this.getSoftwarePLatform().type(software)
        this.getSoftwarePLatform().scrollIntoView()
        cy.get('li').last().click({force: true})
        this.getSoftwarePLatform().click()
    }

    saveDraft() {
        this.getSaveDraftButton().click()
    }

    closePopUpWindow(){
        this.getCloseButton().click()
    }

}
export default InitiativePage