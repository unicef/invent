/// <reference types="Cypress" />

class AdminChangeUserPage{

    getChangeUserPageTitle () {
        return cy.get('#content > h1').contains('Change user')
    }
    
    getJobTitleLabel() {
        return cy.get('[for="id_userprofile-0-job_title"]')
    }

    getJobTitleValue() {
        return cy.get('[input[id="id_userprofile-0-job_title"]')
    }

    verifyJobTitleValue(job) {
        this.getJobTitleValue().contains(job)
    }

    getDepartmentLabel() {
        return cy.get('[for="id_userprofile-0-department"]')
    } 

    getDepartmentValue() {
        return cy.get('')
    } 
}
export default AdminChangeUserPage