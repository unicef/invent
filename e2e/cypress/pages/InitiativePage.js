/// <reference types="Cypress" />

class InitiativePage {

    getGeneralCard() {
        return cy.get('[id="general"]')
    }
	
    // What is the name of the initiative? ||| Required to save draft + Required to publish
    getInitiativeName() {
        return cy.get('input[data-as-name="Name"]')
    }
	
	typeInitiativeName(name) {
        this.getInitiativeName().type(name)
    }
    
    // Which UNICEF Office supports the initiative? ||| Required to save draft + Required to publish
    getUnicefOffice() {
        return cy.get('input[placeholder="UNICEF office"]')
    }
	
	selectUnicefOffice(office) {      
        this.getUnicefOffice().click()
        this.getUnicefOffice().type(office)
        this.getUnicefOffice().scrollIntoView()
        cy.contains(office).click({force:true})
    }

    // Please provide a brief overview of the initiative. ||| Required to publish
    getIniativeOverview() {
        return cy.get('textarea[data-vv-name="overview"]')
    }
	
	typeInitiativeOverview(overview) {
        this.getIniativeOverview().type(overview)
    }

	// Who is the focal point of contact for this initiative? ||| Required to publish
    getFocalPointName() {
        return cy.get('input[data-vv-name="contact_name"]')
    }
	
	typeFocalPointName(name) {
        this.getFocalPointName().type(name)
    }
	
	// Focal Point Email ||| Required to publish
    getFocalPointMail() {
        return cy.get('input[data-vv-name="contact_email"]')
    }
	
	typeFocalPointMail(email) {
        this.getFocalPointMail().type(email)
    }
	
    // Who else should be able to modify this initiative's entry? ||| Required to save draft + Required to publish
    getModifyInitiative() {
        return cy.get('[data-vv-name="team"]').click()
    }
    
    typeModifyInitiative(email)  {
        this.getModifyInitiative().click({force:true})
        this.getModifyInitiative().type(email)
        cy.contains(email).click({force:true})
    }

	// Please select the sector(s) the initiative serves. ||| Required to publish
    getSectorInitiative() {
        return cy.get('[data-vv-name="unicef_sector"]').click()
    }

	selectSectorInitiative(sector) {
        this.getSectorInitiative().click()
        this.getSectorInitiative().type(sector)
        cy.contains(sector).click({force:true})
        this.getSectorInitiative().click()
   }
   
	// Which Goal Area does the initiative focus on? ||| Required to publish
    getGoalArea() {
        return cy.get('[data-vv-name="goal_area"]').click()
    }
	
	selectGoalArea(goalarea) {
       this.getGoalArea().click().type(goalarea)
       cy.contains(goalarea).click()
   }
	
	// Please select the date the initiative was started. ||| Required to publish
    getStartDate() {
        return cy.get('[data-vv-name="start_date"]').click()
    }
	
	selectStartDate(startdate) {
       this.getStartDate().click()
       this.getStartDate().type(startdate).type('{enter}')
	   }
	
	// Please select the partner type. ||| Required to publish
    getPartnerType() {
        return cy.get('div[data-vv-as="Partner Type"]')
    }
	
	// Please provide the name of your partner. ||| Required to save draft + Required to publish
    getPartnerName() {
        return cy.get('input[data-vv-as="Partner Name"]')
    }
	
    typePartnerName(name) {
        this.getPartnerName().type(name)
    }
	
	selectPartnerType(partner) {
        this.getPartnerType().click({force:true})
        this.getPartnerType().type(partner)
        this.getPartnerType().scrollIntoView()
        cy.contains(partner).click()
    }

    // Select all the software platform(s) used in the deployment of the initiative.
    // Required to publish
    getSoftwarePLatform(){
        return cy.get('[data-vv-name="platforms"]')
    }

	selectSoftwarePLatform(software) {
        this.getSoftwarePLatform().click({force:true})
        this.getSoftwarePLatform().type(software)
        this.getSoftwarePLatform().scrollIntoView()
        cy.get('li').last().click({force: true})
        this.getSoftwarePLatform().click()
    }
	
	//Save draft Button
    saveDraft() {
        this.getSaveDraftButton().click()
    }
	
	getSaveDraftButton() {
        return cy.get('[class="el-button el-button--primary el-button--medium SaveDraft NewProject"]')
    }

    //Verify you are in Draft view
    // draftView() {
    //     this.getdraftView()
    // }

    // getdraftView() {
    //     return cy.get('Draft').should()
    // }

    
    //Publish Button
    publishInitiative() {
        this.getPublishButton().click()
    }
        
    getPublishButton() {
        //cy.get().find().as("")
        return cy.get('.NavigationActions > .el-button--primary')
        
    }
	
    //Cancel Button
    cancelInitiative() {
        this.getCancelButton().click({force:true})
    }
        
    getCancelButton() {
        return cy.get('.NavigationActions > .CancelButton')
    }

	//Pop up Window
    closePopUpWindow(){
        this.getCloseButton().click()
    }

	getPopWindow(){
        return cy.get('[role="dialog"]')
    }
	
	//Close Button
	getCloseButton(){
        return cy.contains('Close')
    }

}
export default InitiativePage