# Organisation

There's only one organisation in the project: **UNICEF**
Because of the data structure and relations described in the [Supplementary Diagrams](supplementary_diagrams.md) the actual record id is needed throughout the application.

:::{admonition} Warning
:class: warning
Make sure there is a record in `user_organisation` table with the name `UNICEF`!  
If there is no `UNICEF` record, the frontend is going to malfunction after logging in.  
The current architecture makes it hard to handle this edge case gracefully.
:::

## Frontend

The organisation is provided by the `getUnicefOrganisation` getter in `system` store.
Mainly the `id` is used in the project form, coverage and profile pages.