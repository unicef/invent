class NavigationBar{

    getUserAvatar(){
        return cy.get('[data-test="user-dropdown"]')
    }

    getLogOutButton(){
        return cy.contains('Logout')
    }

    logOut(){
        this.getUserAvatar().click()
        this.getLogOutButton().click()
    }

}
export default NavigationBar