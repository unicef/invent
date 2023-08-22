/// <reference types="Cypress" />

class Requests {

    getInitiativesList() {
        return cy.getAllLocalStorage().then((result) => {   
            return cy.request({
                method: "GET",
                url: '/api/search/?type=list',
                headers: {
                    'Authorization': 'Token ' + result[`${Cypress.config().baseUrl}`]["jwt_token"]
                }
            }).then((response) => {
                return response
            })
        })
    }

    getMyInitiativesList() {
        return cy.getAllLocalStorage().then((result) => {   
            return cy.request({
                method: "GET",
                url: '/api/projects/user-list/member-of/',
                headers: {
                    'Authorization': 'Token ' + result[`${Cypress.config().baseUrl}`]["jwt_token"]
                }
            }).then((response) => {
                return response
            })
        })
    }
}

export default Requests