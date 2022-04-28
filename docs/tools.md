# Tools

## Sentry

[Sentry](https://sentry.io/) is used to catch and track errors in the application.
### Backend

We use Sentry for error collection for both frontend and backend applications. Setting it up is very easy, you just need to register an account on https://sentry.io and make environments for your servers + applications. We usually have 2 per server (1 for frontend, 1 for backend)

To use Sentry follow these steps:

create an environment for an application (eg: DEV BACKEND)
get the DSN (SENTRY_DSN) for your new environment and place it in the corresponding .env file in the application folder on the deployed application. (eg. django/.env)
rebuild and restart your docker containers and you are ready to go.

### Frontend

To log errors into Sentry the proper DSN has to be set in .env `SENTRY_DSN` key.

The [nuxt/sentry](https://sentry.nuxtjs.org/) modul automatically reports error and exception.
It also provides a global object (`$sentry`) by which custom events can be captured. 

```js
this.$sentry.captureMessage('Un-caught validation error in project page', {
  level: 'error',
  extra: {
    apiErrors: this.apiErrors,
    errors,
  },
})
```

For further options, please refer to the official [documentation](https://sentry.nuxtjs.org/guide/usage).

## Circle CI

For our own and even for the open source repository we use CircleCI for CI and CD.

There are 2 official repositories followed by CircleCI:
- https://github.com/unicef/invent - official open source repository, uses CI only
- https://github.com/pulilab/TIIP - all our current development goes here first, uses CI+CD

The configuration file for Circle is located in `.circleci/config.yml` in the repo.

## Job descriptions

There are several jobs within our configuration, like `build-and-test`, `deploy-dev`, `e2e-dev`, `deploy-qa`
and two workflows `build-and-deploy` and `build-and-test-only`. Let's go through these one by one.

### Job: `build-and-test`

This is the main job of CI, specifically to install requirements for both frontend and backend applications
and then run the test suites, coverage and check for missing migrations.

### Job: `deploy-dev`

Using the fabric script, it deploys current `dev` branch to DEV server. The host of the DEV server is set on CircleCI
as an env var.

`DEV_HOST_STRING` - Host of DEV (eg: user@host.com)

### Job: `deploy-qa`

Using the fabric script, it deploys a tag or a tagged release to QA server. The host of the QA server is set on CircleCI
as an env var.

`QA_HOST_STRING` - Host of QA (eg: user@host.com)

### Job: `e2e-dev`

Runs Cypress E2E tests and saves screenshots and videos of failed tests. (Currently not in use)

### Workflow: `build-and-deploy`

This workflow is only used for the https://github.com/pulilab/TIIP repo (hence the filters).

### Workflow: `build-and-test-only`

This workflow is used for every fork except the original https://github.com/pulilab/TIIP repo (hence the filters).
