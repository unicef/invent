# Contributor's Guide

## Coding Style
The following Code Style Guides and Linters should be used to format code before submitting a pull request:	
* Backend: 
  * Cover new code with tests cases and execute the test suite (see {ref}`installation_manual`)).
  * Code Style Guide: PEP 8 Style Code  for Python code.
  * Linter: Flake8  should be used. Configuration can be found in django/.flake8 . In order to invoke the linter, execute from <GIT_REPOSITORY_NAME> the following: ```docker-compose exec django flake8```
* Frontend: 
  * Cover new code with tests cases and execute the test suite: ```yarn test```
  * Code Style Guide: Vue.js style guide  should be used. 
  * Linter: ESLint should be used. Configuration found in frontend/.eslintrc.js. It contains standard JS rules. In order to invoke the linter, execute from <GIT_REPOSITORY_NAME> the following (configured in frontend/package.json): ```yarn precommit```


## Git branching model
The Git branching model that should be used is the [git-flow branching model](https://nvie.com/posts/a-successful-git-branching-model/) that involves the use of feature branches and multiple primary branches. 

