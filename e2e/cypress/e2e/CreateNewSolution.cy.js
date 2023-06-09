/// <reference types="Cypress" />
import NavigationBar from "../pages/NavigationBar"
import InnovationPortfoliosPage from "../pages/InnovationPortfoliosPage"
import LoginForm from "../pages/LoginForm"
import AllSolutionsPage from "../pages/AllSolutionsPage"
import NewSolutionPage from "../pages/NewSolutionPage"

import HomePage from "../pages/HomePage"
import InitiativePage from "../pages/InitiativePage"
import InventoryPage from "../pages/InventoryPage"
import LoginPage from "../pages/LoginPage"
import MyInitiativesPage from "../pages/MyInitiativesPage"
import SolutionPage from "../pages/SolutionPage"
import Requests from "../support/Requests"


describe('Demo test', () => {
    it('https://unicef.visualstudio.com/ICTD-INVENT/_workitems/edit/',() => {
        const loginForm = new LoginForm()
        loginForm.login(Cypress.env('globalportfolio'), Cypress.env('globalportfolio'))
        const navigationBar = new NavigationBar()
        navigationBar.navigateToInnovationPortfoliosPage()
        const innovationPortfoliosPage = new InnovationPortfoliosPage()
        innovationPortfoliosPage.openAllSolution()
        const allSolutionPage = new AllSolutionsPage
        allSolutionPage.pressCreateNewSolution()
        const newSolutionPage = new NewSolutionPage
        //newSolutionPage.getTitle().contains("Create Solution")
        //newSolutionPage.getNewSolutionTitle().contains("What is the name of the solution?")
        //newSolutionPage.typeSolutionName('Automation Creates a New Solution'+(Math.floor(Math.random() * 1000000000000000)).toString())
        //newSolutionPage.setOpenSourceFrontierTech()
        //newSolutionPage.setLearningInvestment()
        newSolutionPage.pressAddPortfolio()
        newSolutionPage.setInnovationPortfolio('Climate Change')
        //newSolutionPage.cancelSolution()
        //newSolutionPage.saveSolution()



    })
})

