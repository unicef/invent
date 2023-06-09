/// <reference types="Cypress" />
import NavigationBar from "../pages/NavigationBar"
import InnovationPortfoliosPage from "../pages/InnovationPortfoliosPage"
import LoginForm from "../pages/LoginForm"
import AllSolutionsPage from "../pages/AllSolutionsPage"
import NewSolutionPage from "../pages/NewSolutionPage"

describe('"Create a New Solution" as a non portfolio manager', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/155095',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('noportfolio'), Cypress.env('noportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInnovationPortfoliosPage()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.openAllSolution()
        const allSolutionPage = new AllSolutionsPage
        allSolutionPage.noCreateNewSolution()
    })
})

describe('"Create a New Solution" as a portfolio manager', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/155098',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInnovationPortfoliosPage()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.openAllSolution()
        const allSolutionPage = new AllSolutionsPage
        allSolutionPage.pressCreateNewSolution()
        const newSolutionPage = new NewSolutionPage
        newSolutionPage.getTitle().contains("Create Solution")
        //newSolutionPage.getNewSolutionTitle().contains("What is the name of the solution?") NEed better element to track
        newSolutionPage.typeSolutionName('Automation Creates a New Solution'+(Math.floor(Math.random() * 1000000000000000)).toString())
        newSolutionPage.setOpenSourceFrontierTech()
        newSolutionPage.setLearningInvestment()
        newSolutionPage.pressAddPortfolio()
        newSolutionPage.setInnovationPortfolio('Climate Change')
        newSolutionPage.setProblemStatements()
        newSolutionPage.setOverrideReachValue((Math.floor(Math.random() * 100)))
        newSolutionPage.pressAddCountry()
        newSolutionPage.setCountry('Cuba')
        newSolutionPage.setPeopleReach((Math.floor(Math.random())))
        newSolutionPage.cancelSolution()
        newSolutionPage.cancelCancelButton()
        newSolutionPage.saveSolution()
        newSolutionPage.closeButton()
        
    })
})
