# Versioning
Project (Initiative) versioning is enabled by default.
All fields that are in the `project.data` or `project.draft` `JSONFields` are versioned.

#### Versioning excludes the following attributes
- `team`
- `viewers`
- `favorited_by`
- `featured`
- `featured_rank`
- `image`

#### Endpoints triggering a new version
Successful calls to these endpoints will create a new version.
- Project Create `/api/projects/draft/<int:country_office_id>/`
- Publish `/api/projects/publish/<int:project_id>/<int:country_office_id>/`
- Unpublish `/api/projects/unpublish/<int:project_id>/`
- Update Draft `/api/projects/draft/<int:project_id>/<int:country_office_id>/`

:::{admonition} Exemptions
:class: info

If you publish or update draft with the exact same payload as before, new version will not be created
:::

## Django Admin

#### Project > Projects
Click on a project (initiative). Versions are inlined in order.

#### Project > Project versions
Click on a particular project version.

## Versioning History API a.k.a Changelog
`URL: GET /api/projects/<int:pk>/version-history`

Based on user permissions, there are 2 versions of the response.
- For `is_superuser, project.team, project.viewer, country_office.manager` response has **ALL versions**
- For other users, response only included project versions that are **published (not draft)**

The API lists versions of a project, each version is compared to the next in line (meaning version + 1 if
the permission is for ALL versions and next published (if exists) for all others).
Between each pair of versions we derive the changes from the point of view of the current version to previous. 
Basically we want to answer the question: What has changed since the previous version.

Each version object in the list will disclose the following attributes:
```{list-table} Versioning History Response attributes
:header-rows: 1
:name: invent-internal-versioning-history

* - Name of attribute
  - Type
  - Description
* - id
  - int
  - ID of ProjectVersion
* - version
  - int
  - Version number (starts from 1)
* - modified
  - datetime
  - Timestamp when the version was modified
* - user
  - UserProfile
  - User who created the new version
* - changes
  - list
  - The main property to list changes between this and a previous version. It determines changes of two `JSONField` attributes.
* - published
  - bool 
  - Whether this version is draft or published. True if published.
* - beyond_history
  - bool
  - True if the project was created before the versioning system was installed. Not useful for new deployments. Can be controlled with `settings.PROJECT_VERSIONING_INSTALLED_AT` timestamp
* - was_unpublished
  - bool
  - True if the project has been unpublished from the previous version
```

## Display version information

Version history of an initiative is displayed in a timeline view in a dialog (`ProjectHistoryDialog`).  
The Timeline component handles the proper UI flow.

:::{figure-md} changelog_anatomy

<img src="./_static/images/changelog_anatomy.png" alt="Changelog anatomy" class="bg-primary mb-1" width="600px">

**Changelog anatomy**
:::

### Components

```
components
├─ project
│  └─ history
│     │  Timeline.vue            -> Wrap the whole history
│     │  TimelineItem.vue        -> Wrap one version
│     │  TimelineItemBody.vue    -> Contains the list of changes
│     │  TimelineItemNoData.vue  -> Snown when there is no data
│     └─ values
│        │  ValueCoverImage.vue  -> For cover image
│        │  ValuePartners.vue    -> For partners
│        │  ValuePhases.vue      -> For project phases
│        │  ValueSpecial.vue     -> For special values (indicated by backend)
│        │  ValueTags.vue        -> For values with lists (tags)
│        │  ValueText.vue        -> For simple text (values represented by text)
│        │  ValueWebsite.vue     -> For websites
│        │  SimpleMessage.vue    -> For when only want to show a simple message
└─ dialogs
   │  ProjectHistoryDialog.vue   -> The "simple" dialog
```

### Dialog

#### Open

The dialog can be displayed via the `open(projectParams)` method passing the project's key properties.

```{list-table} Dialog options
:header-rows: 1
:name: invent-internal-versioning-history-dialog

* - Name of attribute
  - Type
  - Description
* - id
  - number
  - Project ID
* - created
  - date
  - Project creation date
* - title
  - string
  - Project title
* - teamMember
  - boolean
  - Indicates if the current user of the selected project is a team member or a viewer
```
#### Data structure

The data structure can be seen in the example [mock data](./_static/version_history.mock.json).

#### Data preparation

Backend provides the raw version history data in an array that needs to be converted on frontend.  

As some of the fields are special, it was necessary to define a map for the fields (`fieldMap` variable) with the component, title and a parser function. Some of the fields has to be ignored, those are `undefined` in the `fieldMap`.

```js
country: {
  component: 'ValueText',
  title: this.$gettext('Country'),
  parse: (countryId) => this.parseCountry(countryId),
}
```

The `getProjectHistory` method 
- run through the versions
  - clean up fields in changes (remove the `undefined` fields)
  - parse fields' changes (values)
- check the edge case if the project has been created before the versioning system has been introduced. If so, then add special items to the version list.
- set up current version of the project

UI is rendered based on the prepared data using [Vue Dynamic Components](https://v2.vuejs.org/v2/guide/components.html?redirect=true#Dynamic-Components) mechanism.

