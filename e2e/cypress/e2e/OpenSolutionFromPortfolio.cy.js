/// <reference types="Cypress" />
import InnovationPortfoliosPage from "../pages/InnovationPortfoliosPage"
import LoginForm from "../pages/LoginForm"
import NavigationBar from "../pages/NavigationBar"
import SolutionPage from "../pages/SolutionPage"

describe('Open a Solution Page from Portfolio', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/149436',() => {
        var PortfolioName = 'WASH'
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInnovationPortfoliosPage()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.getViewPortfolios()
        innovationPortfoliosPage.openPortfolio(PortfolioName)
        innovationPortfoliosPage.openSolution()
        const solutionPage = new SolutionPage()
        solutionPage.getViewTitle().contains("View Solution Information")
        solutionPage.getURL().should('contain', '/portfolio/innovation/solutions/')
        solutionPage.getBreadcrumb().should('contain', 'Innovation Portfolio')
        solutionPage.getBreadcrumb().should('contain', PortfolioName)
        solutionPage.getSolutionName()
        //solutionPage.getBreadcrumb().should('contain', )




    })
})

