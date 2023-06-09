/// <reference types="Cypress" />
import AllSolutionsPage from "../pages/AllSolutionsPage"
import InnovationPortfoliosPage from "../pages/InnovationPortfoliosPage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"
import SolutionPage from "../pages/SolutionPage"

describe('Solution name column sorting on "all solutions" page', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/160064',() => {
        //var PortfolioName = 'WASH'
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInnovationPortfoliosPage()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.openAllSolution()
        const allSolutionPage = new AllSolutionsPage()
        allSolutionPage.getTitle().contains('Solutions')



    })
})



