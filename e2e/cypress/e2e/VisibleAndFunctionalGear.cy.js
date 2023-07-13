/// <reference types="Cypress" />
import LoginForm from "../pages/LoginForm"
import LoginPage from "../pages/LoginPage"
import MyInitiativesPage from "../pages/MyInitiativesPage"
import NavigationBar from "../pages/NavigationBar"
import SolutionPage from "../pages/SolutionPage"
import Requests from "../support/Requests"
import CountryPage from "../pages/CountryPage"

describe('Demo test', () => {

    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/165952',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const countryPage = new CountryPage()
        countryPage.goToCountryPage('AF')
        countryPage.getGear().should('be.visible')



        countryPage.pressGear()
        countryPage.getGearMenuSelectedItems().should('have.length', 29)
        countryPage.getGearMenuUnselectedItems().should('have.length', 0)
        countryPage.getGearMenuTitle().should('have.text', "SELECTED SECTORS (29/29)")
        //
        // countryPage.getGearMenuList().should('be.visible')
        // countryPage.pressGear()
        // countryPage.pressBoardSwitch()
        // countryPage.getGear().should('be.visible')
        // countryPage.pressHeightSwitch()
        // countryPage.getGear().should('be.visible')

        // const testGear = class
        // testGear {
        //     countryPage.getGear().should('be.visible')
        //     countryPage.pressGear()
        //     countryPage.getGearMenuList().should('be.visible')
        // }


        

    })
})

