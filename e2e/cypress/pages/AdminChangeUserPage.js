/// <reference types="Cypress" />

class AdminChangeUserPage{

    getChangeUserPageTitle () {
        return cy.get('#content > h1').contains('Change user')
    }
    
    getJobTitleLabel() {
        return cy.get('[for="id_userprofile-0-job_title"]')
    }

    getJobTitleValue(jobvalue) {
        return cy.get('[name="userprofile-0-job_title"]').invoke('val').should('equal', jobvalue)
    }

    getDepartmentLabel() {
        return cy.get('[for="id_userprofile-0-department"]')
    }

    getDepartmentValue(departmentvalue) {
        return cy.get('[name="userprofile-0-department"]').invoke('val').should('equal', departmentvalue)
    }
}
export default AdminChangeUserPage