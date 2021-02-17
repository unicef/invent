describe("User Sign-up and Login", function () {
  before(function () {
    cy.server();
  });

  after(function () {
    // cy.logout();
  });

  it("should redirect unauthenticated user to login page", function () {
    cy.visit("/");
    cy.location("pathname").should("equal", "/en/auth");
    // cy.visualSnapshot("Redirect to Login");
  });

  it("should display label error messages", function () {
    const signinPath = Cypress.env("loginSuffix");

    cy.location("pathname", { log: false }).then((currentPath) => {
      if (currentPath !== signinPath) {
        cy.visit(signinPath);
      }
    });
    cy.getBySel("signin-username").clear();
    cy.getBySel("signin-username").type("error");
    cy.getBySel("signin-password").clear();
    cy.getBySel("signin-username-item").contains(
      "Has to be a valid email address"
    );
    cy.getBySel("signin-username").clear();
    cy.getBySel("signin-password-item").contains("This field is required");
    cy.getBySel("signin-password").clear();
    cy.getBySel("signin-username-item").contains("This field is required");
  });

  it("should login user given the right credentials", function () {
    cy.login(Cypress.env("testUser"), Cypress.env("testPw"));
    cy.url().should("include", "/en/-/inventory/list?country=");
    cy.getBySel("user-dropdown").contains(Cypress.env("username"));
    cy.getBySel("menu-portfolio-link").contains("Innovation Portfolios");
  });

  it("should logout user on the user menu dropdown", function () {
    cy.logout();
    cy.location("pathname").should("equal", "/en/auth");
    cy.visit("en/-/inventory/list");
    cy.location("pathname").should("equal", "/en/auth");
  });
});
