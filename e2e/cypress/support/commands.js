import "@percy/cypress";

// custom command to make taking snapshots with full name
// formed from the test title + suffix easier
// cy.visualSnapshot() // default full test title
// cy.visualSnapshot('clicked') // full test title + ' - clicked'
// also sets the width and height to the current viewport
Cypress.Commands.add("visualSnapshot", (maybeName) => {
  let snapshotTitle = cy.state("runnable").fullTitle();
  if (maybeName) {
    snapshotTitle = snapshotTitle + " - " + maybeName;
  }
  cy.percySnapshot(snapshotTitle, {
    widths: [cy.state("viewportWidth")],
    minHeight: cy.state("viewportHeight"),
  });
});

Cypress.Commands.add("getBySel", (selector, ...args) => {
  return cy.get(`[data-test=${selector}]`, ...args);
});

Cypress.Commands.add("getBySelLike", (selector, ...args) => {
  return cy.get(`[data-test*=${selector}]`, ...args);
});

Cypress.Commands.add("signUp", () => {
  cy.visit(Cypress.env("server"));
  cy.randomAlphaNumeric(10).then((response) => {
    Cypress.env("testUser", "cypress_testUser_" + response + "@example.com"); // save user to env
    cy.getBySel("signin-username").type(Cypress.env("testUser"));
    cy.getBySel("signin-password").type(Cypress.env("testPw"));
    cy.getBySel("signin-repeat-password").type(Cypress.env("testPw"));
    cy.contains("Sign up now").click();
    cy.location("pathname", { timeout: 5000 }).should(
      "include",
      "/edit-profile"
    );
  });
});

Cypress.Commands.add("login", (username, password, rememberUser = false) => {
  const signinPath = Cypress.env("loginSuffix");
  const log = Cypress.log({
    name: "login",
    displayName: "LOGIN",
    message: [`🔐 Authenticating | ${username} with ${password}`],
    autoEnd: false,
  });

  cy.server();
  // cy.route("POST", "/login").as("loginUser");
  // cy.route("GET", "checkAuth").as("getUserProfile");

  cy.location("pathname", { log: false }).then((currentPath) => {
    if (currentPath !== signinPath) {
      cy.visit(signinPath);
    }
  });

  cy.getBySel("signin-username").clear();
  cy.getBySel("signin-password").clear();
  log.snapshot("before");
  cy.getBySel("signin-username").type(username);
  cy.getBySel("signin-password").type(password);

  if (rememberUser) {
    cy.getBySel("signin-remember-me").find("input").check();
  }

  cy.getBySel("signin-submit").click();
  // cy.wait("@loginUser").then((loginUser: any) => {
  //   log.set({
  //     consoleProps() {
  //       return {
  //         username,
  //         password,
  //         rememberUser,
  //         userId: loginUser.response.body.user?.id,
  //       };
  //     },
  //   });

  //   log.snapshot("after");
  //   log.end();
  // });
});

Cypress.Commands.add("logout", () => {
  const log = Cypress.log({
    name: "logout",
    displayName: "LOGOUT",
    message: [`logout of the system`],
    autoEnd: false,
  });
  cy.getBySel("user-dropdown").click();
  cy.getBySel("logout-submit").click();
});

Cypress.Commands.add("randomAlphaNumeric", (length) => {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let charactersLength = characters.length;
  return Array.from({ length: length }, () => {
    return characters.charAt(Math.floor(Math.random() * charactersLength));
  }).join("");
});
