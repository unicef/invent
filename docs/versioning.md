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