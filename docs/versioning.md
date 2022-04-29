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