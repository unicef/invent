# End to end testing
## Installation
This is only required for running the GUI mode locally, for running in the console, we've a docker compose configuration available.
## Running Cypress
Install [node](https://nodejs.org/en/) if you don't have it. Then, on you favorite terminal:

```bash
# be sure to be inside e2e folder

# linux
$ sudo apt update && sudo apt install yarn
$ yarn
$ yarn test:dev
# or
$ yarn test:pro

# macOS
$ npm install -g yarn
$ yarn
$ yarn test:dev
# or
$ yarn test:pro
```
## GUI mode

To open the GUI for end to end testing, in your terminal, go to the `e2e/` folder and:

```bash
$ yarn test:dev
# or
$ yarn test:pro
```
## Running on docker

On your terminal, type:

```bash
# in root directory from project
# with `-d` optional parameter for running in daemon mode
$ docker-compose -f docker-compose.yml -f docker-compose.e2e.yml up -d
```

This command start up all of our docker containers, with `http://localhost/` as the root url.

### e2e test run

Go `e2e/` folder: 

```bash
$ docker run --network host -it -v $PWD:/e2e -w /e2e cypress/included:6.2.1
```
This command starts up a premade *Cypress* container and runs the test sets using the host computer's network settings.
## FAQ

- Need to change configuration of test? `cypress.dev.json` and `cypress.pro.json` contain the configuration files for Cypress.
- If you need inspiration, there's a [real world example](https://github.com/cypress-io/cypress-realworld-app) for state of the art testing with cypress.
