# Contributor's Guide

## Coding Style
The following Code Style Guides and Linters should be used to format code before submitting a pull request:	
* Backend: 
  * Cover new code with tests cases and execute the test suite (see [](installation_manual.md)).
  * Code Style Guide: PEP 8 Style Code for Python code.
  * Linter: Flake8  should be used. Configuration can be found in django/.flake8 . In order to invoke the linter, execute from <GIT_REPOSITORY_NAME> the following: ```docker-compose exec django flake8```
* Frontend: 
  * Cover new code with tests cases and execute the test suite: ```yarn test```
  * Code Style Guide: Vue.js style guide should be used. 
  * Linter: ESLint should be used. Configuration found in frontend/.eslintrc.js. It contains standard JS rules. In order to invoke the linter, execute `yarn precommit` in the `frontend ` folder.


## Git branching model
The Git branching model that should be used is the [git-flow branching model](https://nvie.com/posts/a-successful-git-branching-model/) that involves the use of feature branches and multiple primary branches. 

## Testing (Backend)
Either TDD or not, we want to maintain 100% code coverage, so the main thing is to have any new feature and bug fix tested.
Each Django application has their corresponding tests that can be found within the app's folder.

### Running tests for code coverage
Make sure that the containers are running, then:
```bash
docker-compose exec django py.test --cov --cov-report html --cov-fail-under 100 --cov-report term-missing --cov-config. Coveragerc
```

### Executing a single test
Alternatively, in order to execute a test suite for a specific Django application (see section 3.3.1.1) execute the following:
```bash
docker-compose exec django py.test -s -k <test_name>
```

## Make and applying migrations
Django uses Migrations as a way of propagating changes made on models into the database schema. For more information, see [Django Migrations](https://docs.djangoproject.com/en/4.0/topics/migrations/). The following commands should run on the local development environment in order to interact with migrations and Django’s handling of database schema.
```bash
docker-compose exec django python manage.py makemigrations
```
To run those new migrations that were created:
```bash
docker-compose exec django python manage.py migrate
```

## Frontend local development environment

### Prerequisites

As described in the [frontend part](architecture.md#requirements) of the architecture

After cloning the repository navigate to `frontend` folder.
- install the packages: `yarn install`
- copy `.env.template` into `.env`
- either import a database dump or create 