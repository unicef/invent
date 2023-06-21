/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"
import InitiativePage from "../pages/InitiativePage"


describe('Verify Sector functionality', () => {
    it('',() => {

        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToNewInitiativePage()
        const initiativePage = new InitiativePage()   
        initiativePage.selectLeadSectorInitiative('Communications')
        initiativePage.selectSupportingSectorsInitiative('C4D')
        initiativePage.getLeadSectorInitiative().click()
        initiativePage.getDropDownList().eq(19).find('[class="el-select-dropdown__item is-disabled"]').should('have.text',"C4D")
        initiativePage.getDropDownList().eq(19).find('[class="el-select-dropdown__item selected hover"]').should('have.text',"Communications")
    })
})  