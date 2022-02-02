# Installation Manual

## Environment Prerequisites
Before the installation make sure that the DEV-local environment has properly installed and configure the following pre-requisites (instructions how to install are not provided):


```{list-table} Environment Prerequisites
:header-rows: 1
:name: frontend-modules-table

* - Prerequisite
  - Version
  - Description
* - OS
  - Linux (tested with Ubuntu 21.04), Mac and Windows supported
  - OS of the DEV-local environment
* - Python
  - 3.x (tested 3.7.11)
  - Python should be installed in the DEV-local environment; e.g. to execute manage.py
* - npm
  - 7.5.x (tested with 7.5.2)
  - Package manager for Javascript, used to install yarn
* - yarn
  - 1.22.x (tested with 1.22.17)
  - Package manager for code, recommended to install through npm package manager, which comes bundled with Node.js. Used to deploy the frontend application
* - docker
  - 20.x (tested with 20.17)
  - Software platform to create, manage and run applications. Backend applications are containerized.
* - docker-compose
  - 1.29.x (tested with 1.29.2)
  - Tool to define and run the multi-container Docker applications.
* - Web Browser
  - Chrome, Firefox, Safari or Edge latest versions
  - Used to access the SPA
```

:::{figure-md} deployment-diagram

<img src="./_static/images/deployment_diagram.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**Deployment Diagram**
:::


## Clone repository
```bash
git clone <GIT_REPOSITORY_URL>
cd <GIT_REPOSITORY_NAME>
```

## Configure 
Copy``` <GIT_REPOSITORY_NAME>/django/.env.template``` to ```<GIT_REPOSITORY_NAME>/django/.env``` and provide the appropriate values (```required in django/tiip/settings.py```):
```bash
SECRET_KEY=<a random generated long alphabetic string eg dskgsjgssosdsfhaplfnfbkjnndbff>
DEBUG=False
AZURE_CLIENT_ID=
AZURE_SECRET=
AZURE_TENANT=
AZURE_CALLBACK_URL=
```

Where:
```{list-table} Backend .env contents description
:header-rows: 1
:name: backend-env-table

* - Key
  - Optional/Mandatory
  - Description
* - ```SECRET_KEY```
  - Mandatory
  - A secret key for a particular Django installation. It provides cryptographic signing and it should be set to a unique, unpredictable value.
* - ```DEBUG```
  - Mandatory
  - A boolean that turns on/off debug mode
* - ```ZURE_CLIENT_ID```
  - Optional
  - The client(application) ID of an App Registration in the tenant. 
* - ```AZURE_SECRET```
  - Optional
  - A client secret that was generated for the App Registration. 
* - ```AZURE_TENANT```
  - Optional
  - The Azure Active Directory tenant(directory) ID. 
* - ```AZURE_CALLBACK_URL```
  - Ooptional
  - Azure login redirect URI 
```

Copy``` <GIT_REPOSITORY_NAME>/frontend/.env.template``` to ```<GIT_REPOSITORY_NAME>/frontend/.env``` and provide the appropriate values:
```bash
HOST=localhost
PORT=3000
AZURE_CLIENT_ID=
AZURE_REDIRECT_URI=
AZURE_TENANT=
```

Where:
```{list-table} Frontend .env contents description
:header-rows: 1
:name: frontend-env-table

* - Key
  - Optional/Mandatory
  - Description
* - ```HOST```
  - Mandatory
  - The host url for frontend.
* - ```PORT```
  - Mandatory
  - The port that frontend is loaded. 
* - ```AZURE_CLIENT_ID```
  - Optional
  - The client(application) ID of an App Registration in the tenant.
* - ```AZURE_REDIRECT_URI```
  - Optional
  - The redirect_uri of the application, where authentication responses can be sent and received.
* - ```AZURE_TENANT```
  - Optional
  - The Azure Active Directory tenant(directory) ID. 
```


Configure database connection in ```django/tiip/settings.py```:
here:
```{list-table} Backend .env contents description
:header-rows: 1
:name: backend-env-table

* - Location
  - Description
  - Example
* - ```DATABASES.default.ΝΑΜΕ```
  - Schema name
  - postgres
* - ```DATABASES.default.USER```
  - Username 
  - postgres
* - ```DATABASES.default.HOST```
  - Hostname
  - localhost
* - ```DATABASES.default.PORT```
  - Port
  - 5432
```

:::{admonition} Warning
:class: warning

This configuration assumes that PostgreSQL trusts connections from localhost else a password is required.
:::

Configure emails:
```{list-table} Backend .env contents description
:header-rows: 1
:name: backend-env-table

* - Location
  - Description
  - Example
* - ```DEFAULT_FROM_EMAIL```
  - Used in ```send_mail methods``` to define the sender (FROM
  - UNICEF T4D & Innovation Inventory Portal <noreply@invent.unicef.org>
```

## Build
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>
```

Build containers:
```bash
docker-compose build
```

This command will use the default ```docker-compose.yml``` file


::::{important}
Code changes are applied immediately in backend without the need to restart django.
::::

## Tests Execution
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>
```
In order to execute all the tests, execute the following:
```bash
docker-compose exec django py.test --cov --cov-report html --cov-fail-under 100 --cov-report term-missing --cov-config. Coveragerc
```

Alternatively, in order to execute a test suite for a specific Django application (see section 3.3.1.1) execute the following:
```bash
docker-compose exec django ptw – <DJANGO_APPLICATION> -s –testmon
```

For example for ```django/project/tests```:
```bash
docker-compose exec django ptw -- project -s –testmon
```

For example, for ```django/core/tests.py```:
```bash
docker-compose exec django ptw -- core -s –testmon
```

There is also the option to run a single test from the application’s test suite by executing the following:
```bash
docker-compose exec django py.test -s -k <DJANGO_APPLICATION_TEST>
```

For example, for ```django/user/tests```:
```bash
docker-compose exec django py.test -s -k test_non_expiring_api_token_auth
```

## Deploy backend
### Start containers
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>
```

Start containers:
```bash
docker-compose up
```

This will load configuration from the file ```docker-compose.yml``` and load the following containers:


```{list-table} Docker Images
:header-rows: 1
:name: docker-images-table

* - Image
  - Description
* - nginx:1.15.6
  - Downloads docker image of nginx from Docker Hub and creates tiip_nginx container
* - postgres:10.4
  - Downloads docker image of postgres from Docker Hub and creates tiip_postgres container. Set environment for postgresql environment: {POSTGRESQL_DB=postgres, POSTGRESQL_USER=postgres, POSTRESQL_PASSWORD= postgres}
* - redis:4.0.10
  - Downloads docker image of Redis from Docker Hub and creates tiip_redis container
* - django
  - Creates tiip_django container and starts the django application with the command ```/usr/local/bin/gunicorn tiip.wsgi:application -w 2 -b :8000 --reload --timeout 120```
* - redis
  - Creates tiip_celery container and starts celery with the command ```/usr/local/bin/celery -A scheduler worker -B -l info```
```


### Create DB
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>
```

Execute the following command to create the DB schema:
```bash
docker-compose exec django python manage.py migrate --noinput
```

### Deploy frontend
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>/frontend
```

Execute the following to add the dependencies from frontend/package.json file and create node_modules folder:
```bash
yarn install
```
Execute the following to start the frontend server:
```bash
yarn dev
```


### Create superuser (at least one is required)
Change directory to the project’s root folder.
```bash
cd <GIT_REPOSITORY_NAME>
```

Execute the following to create a superuser:
```bash
docker-compose exec django python manage.py createsuperuser
```

Provide the required information, username, email and password.

A superuser can create more superusers as described in {ref}(administration_manual).

### Validate successful installation


#### Login as superuser
Visit with the browser the URL http://localhost/admin and login:


:::{figure-md} superuser-login

<img src="./_static/images/superuser_login.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**Superuser Login Screen**
:::

After a successful login the admin page is loaded:


:::{figure-md} superuser-homepage

<img src="./_static/images/superuser_homepage.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**Superuser Homepage Screen**
:::


#### Login as user (local authentication)
Navigate to http://localhost:3000/en/-/login and enter the user’s credentials to login:

:::{figure-md} user-login

<img src="./_static/images/user_login.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**User Login Screen**
:::

After a successful login the user is redirected to INVENTORY dashboard by clicking on “unicef” icon on the top left corner the home page is loaded.


:::{figure-md} user-homepage

<img src="./_static/images/user_homepage.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**UserHomepage Screen**
:::


### Login as user (Azure Single Sign-On)


:::{figure-md} user-azure-login

<img src="./_static/images/user_azure_login.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**Superuser Login Screen**
:::



:::{figure-md} user-azure-login2

<img src="./_static/images/user_azure_login2.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**Superuser Login Screen 2**
:::






