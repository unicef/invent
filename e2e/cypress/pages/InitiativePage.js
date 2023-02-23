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
        cy.contains(office).click()
    }

    selectSectorInitiative(sector) {
        this.getSectorInitiative().click()
        this.getSectorInitiative().type(sector).type('{enter}')
        cy.contains(sector).click()
        this.getSectorInitiative().click()
   }

   selectGoalArea(goalarea) {
       this.getGoalArea().click()
       this.getGoalArea().type(goalarea)
       cy.contains(goalarea).click()
   }

   selectStartDate(startdate) {
       this.getStartDate().click()
       this.getStartDate().type(startdate).type('{enter}')
   }

    selectPartnerType(partner) {
        this.getPartnerType().click()
        this.getPartnerType().type(partner)
        this.getPartnerType().scrollIntoView()
        cy.contains(partner).click()
    }

    selectSoftwarePLatform(software) {
        this.getSoftwarePLatform().click()
        this.getSoftwarePLatform().type(software)
        this.getSoftwarePLatform().scrollIntoView()
        cy.find(software).click()
        //cy.get('[style="min-width: 862px; transform-origin: center top; z-index: 2071; position: absolute; top: 8325px; left: 81px;"] > .el-scrollbar > .el-select-dropdown__wrap > .el-scrollbar__view > .hover')
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