[![CircleCI](https://circleci.com/gh/unicef/invent.svg?style=shield)](https://circleci.com/gh/unicef/invent)
[![Documentation Status](https://readthedocs.org/projects/unicef-invent/badge/?version=latest)](https://unicef-invent.readthedocs.io/en/latest/?badge=latest)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Developer documentation

[https://unicef-invent.readthedocs.io](https://unicef-invent.readthedocs.io/en/latest/)

## Run the Invent application locally

### Table of Contents


1. [Prerequisites](#prerequisites)
2. [Start the Environment](#start-the-environment)
3. [Setting up the Environment](#setting-up-the-environment)
4. [Troubleshooting](#troubleshooting)

### Prerequisites

Before you proceed, ensure that you have the following software installed on your machine:
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) - (With Kubernetes [enabled](https://docs.docker.com/desktop/kubernetes/))
2. [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
3. [Helm](https://github.com/helm/helm/releases/latest)
4. [Tilt](https://docs.tilt.dev/install.html)
5. [Python](https://www.python.org/downloads/)
6. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Start the Environment
Clone the repository using the following command:
```bash
git clone https://github.com/unicef/invent.git -b master
```
Navigate to the project folder:
```bash
cd invent
```
Start the environment:
```bash
kubectl config use-context docker-desktop
tilt up
```
By navigating to http://localhost:10350/r/(all)/overview you can see the status of the resources. 
The "copy-dump" and "import-dump" Tilt resources are ok to crash if you don't have a sql dump named "dump_anon.sql" present in the root of the repository.
### Setting up the Environment
Once all the services in Tilt (Postgres, Redis, Mailhog, Backend, Frontend) are up and running, 
initiate the DB:
```bash
kubectl exec deployments/invent-django -- python manage.py migrate
```
Create a superuser by providing the necessary information:
```bash
kubectl exec -it deployments/invent-django -- python manage.py createsuperuser
```
Next, go to the URL http://localhost/admin and login using the user you just created.

To create a User that can login to the Invent application, got to the [Users](http://localhost/admin/auth/user/) section, under the "AUTHENTICATION AND AUTHORIZATION".
Click on ["ADD USER +"](http://localhost/admin/auth/user/add/) and fill out the fields as follows:

| Field                  | Value                                                |
|------------------------|------------------------------------------------------|
| Username               | Unimportant (you’ll use the email address to log in) |
| Password               | and confirmation As per hint                         |
| Account type           | Investor viewer (most accounts are of this type)     |
| Name                   | A name that will be displayed in the INVENT front end|
| Organisation           | UNICEF (choose the one in all CAPS!)                 |
| Country                | As wished (does this even do anything?)              |
| Donor                  | UNICEF                                               |
| Language               | English                                              |
| Global portfolio owner | Leave unchecked for a “normal” user                  |
| Country manager of     | Leave unchanged for a “normal” user                  |

Once ready, click "Save" (on the bottom right of the screen) and the page will reload with some additional fields.

Add the email address (which will be used to log in and for notifications).
Leave all the other fields alone for a “normal” user.

To login with the "normal" user you just created, go to http://localhost/en/-/login and use the e-mail and password of the user.

### Project structure

Static files (png, css, etc.) should go to:

`nginx/site/static/`

And can be accessed like:

http://localhost/static/css/some.css

http://localhost -- deployed frontend
http://localhost/admin -- backend admin

## Country map handling

1. Download the maps with the link in the admin page of the selected country
2. Unzip the map and load it in [MAPSHAPER](http://mapshaper.org/)
3. Simplify the map as much as possible without loosing quality
4. Export the map from mapshaper as a geojson
5. Load the exported map file in the admin console and save the form
6. After the map is loaded use the admin interface to select the admin levels and hit save ( in the map tool )
7. Add a value in Map activated on ( be use the Today and Now buttons)
8. Save the form.

## Production settings

On production, install a cron for the user (`crontab -e`) to autobackup the DB

```0 4 * * * cd /path/to/project/django && fab backup_prod```


## Rebuilding search
You can rebuild search any time you want or if you realise there's some data missing from search

`manage.py rebuild_search`

## Donor tools
When you delete a Donor from Django admin (as a superuser) and want to sync the donors in all projects:

`manage.py remove_stale_donors`

When you want to eg. remove a duplicate donor or a typo, you can migrate the project that use the typo or duplicate
donor to the one that you want to keep for all projects:

`manage.py switch_donor_form_to <DONOR_ID_YOU_WANT_TO_MIGRATE_FROM> <TO_DONOR_ID>`

After migrating all projects, you can delete the typo / duplicate donor objects from the admin (don't forget to issue
the `remove_stale_donors` after that.)


## Translations command:

On Osx prerequisite is:

`brew install gettext`

after this command completes:

`brew link --overwrite --force gettext` may be needed


To scrape the code and extract translations:
`yarn translation:extract`

To Update the translations files in the backend:
```bash
cd django
fab update_translations
```

To see the new string and modify translations:
`http://localhost/translation`

(click on Save and Translate next block to save them)

To have translation appear in the frontend (after saving them at the previous step):
`docker-compose restart django`

### Quirks:
Translations are picked up from `<translate></translate>` blocks this block is declared as a global vue component so it can be used without importing it.
If a translation string needs parameters (ie: {{userProfile.name}} hello!) the syntax is `<translate :parameters="{name: userProfile.name}"> {name} hello </translate>`
Also, `$gettext('english/base string')` method is available in every Vue component via a mixin in the i18n plugin.


