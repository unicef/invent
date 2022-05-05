## Translation (i18n)

### Backend

### Frontend

For translation, we use a system based on `.po` extractions with [easygettext](https://www.npmjs.com/package/easygettext). In order to extract all the literals, we need to implement extraction methods in our components.

#### Files to take in consideration

- `gettext.sh`: extract all text marked it as a translate tag and set it up in a `.po` file for backend use. Backend generate translation inputs with [Rosetta](https://django-rosetta.readthedocs.io/).
- `TranslateWrapper.vue`: Create the tags and filters that can be used to map the translation.
- `langReq.js`: Make API request to backend to download files that will be used by Nuxt.

#### Usage

To work around on enrich html and translation tags, do the following:

```html
<translate :parameters="{/*params*/}">some text</translate>
<p>{{'some text' | gt}} or {{'some text' | gt({/*params*/})}}</p>
```
Inside javascript syntax use the global function:

```js
this.$gettext('some text', {/*params*/})
```
:::{admonition} Quirks and tips
:class: info

- Translation tags on the the same html hierarchy have the tendency to not update because of Vue update mechanism. In order to solve it, we must provide the tag with a key, like `<translate key="translation">I want translation</translate>`.
- It is possible to translate via filters, but due to mapping issues, translate by filter is not recommended. Try to avoid this `<p>{{'some text' | gt}}</p>`.
:::


#### Extraction

##### Setup for Windows 10/11

Install WSL2 on Windows 10/11 as described in the [official Microsoft Guide](https://docs.microsoft.com/en-us/windows/wsl/install)

Start the WSL2 terminal and do the following: `sudo apt update`

Then go to the working directory of the project, and execute the following commands:

`sudo apt install npm`

`sudo apt install gettext`

`sudo npm install yarn --global`

##### Extract translatable texts
Make sure you installed all the packages by running `yarn` in the **frontend** folder.

Run `yarn translation:extract`

In the project's main folder, run `docker-compose exec django python manage.py update_translations master`, this will merge all translatable text and they show up in the translation admin.

### Testing translations
You can make translations in Rosetta. In local dev it can be access via [localhost/translation](http://localhost/translation).
After the translation is done, Django needs to be restarted by running `docker-compose restart django` in the project's main folder.