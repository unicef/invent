## Command to run

`fab up` - start all backend instances in daemon mode
`fab down` - stop all backend instances and make backup of db
`fab migrate` - to run new migrations
`docker-compose build` - if there were new django requirements

## Project structure

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

```0 4 * * * cd /home/whomaps/tiip/django && fab backup_prod```


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


