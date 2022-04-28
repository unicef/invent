 # Django Admin features
The following list is features that a superuser or staff member (`is_superuser`, `is_staff`) can use on the `/admin` UI
 
## Auth Token > Tokens
API Tokens can be added here for external API clients. You will need to associate a token with a user, so if you don't have a user, please create one first. It doesn't have to have a password, so standard login would not work with it, but it would work with the API token.

The API Documentation is available here:
`/api/docs/`

## Authentication and Authorization > Users
The standard Django admin interface where users can be added.

### Extra Action: Export selected users
Export users in a downloadable file

## Core > News items
Add or remove news items that will be featured on the landing page of the website

## Country > Countries
View and add countries.

### Extra Action: Export selected countries
Export countries in a downloadable file

## Country > Regional offices
View, add or remove regional offices.

### Extra Action: Export selected regional offices
Export regional offices in a downloadable file

## Country > UNICEF offices
View, add or remove unicef offices.

### Extra Action: Export selected unicef offices
Export unicef offices in a downloadable file

## Generate Export > Export Jobs
Here you can find all the exports that were requested asynchronously (Use this method when you are exporting a lot of objects)
This is currently only available for Project objects (Initiatives)

## Project > Portfolios
View, add or remove portfolios.

### Extra Action: Export selected portfolios
Export portfolios in a downloadable file

## Project > Projects
View, add or remove projects (initiatives).

### Extra Action: Export selected portfolios
Export portfolios in a downloadable file

### Extra Action: Generate export in the background
Export portfolios in a downloadable file asynchronously (Use this method when you are exporting a lot of objects)

## Project > Software
View, add or remove software.

### Extra Action: Approve/Decline selected software
When approved, software will be included in the official list of available software through the UI.
When declined, software will be removed from every initiative that referenced it in the first place.

## Project > Solutions
View, add or remove solutions.

### Extra Action: Export selected solutions
Export solutions in a downloadable file

## WHO Taxonomies
The following list is supposed to be synced from the Digital Health Atlas that provides WHO taxonomies for health projects.
These are used on INVENT when the initiative is focusing on health. These taxonomies are only readable, but not editable or 
removable through the admin.

- WHO Digital Health Interventions (=UNICEF Health Capability Categories)
- WHO Health Categories
- WHO Health Focus Areas
- WHO Health System Challenge Groups
- WHO Health System Challenges

