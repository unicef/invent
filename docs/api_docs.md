# API Documentation
The main purpose of the entire Django application is to expose APIs. Almost every feature of the system
is controlled through APIs (the UI uses it extensively). Hence, it's very important to be familiar with
the API endpoints, what they do and how do they work. In this section we will provide the 2 different
documentations that can be used by developers or external clients (external devs) who want to utilize
the API from their 3rd party application.

## Public API Documentation

URL: `GET /api/docs/`

Serves as the number one source for external clients who want to use the API for both fetching projects (initiatives) 
or creating them.

### Access for external parties
Access can be given through the Django Admin interface. The `Auth token > Tokens` section can be used to add 
new tokens. Every token must be associated with a user object, so any new client must also have a new user.
These user accounts however can only be applicable to be used with the API if there is no password set to them.
That ensures that the UI and rest login API won't be able to authenticate that user, but the newly added
non-expiring token can be used in the Authorization header for the purpose of the API calls.

## Private / DEV only API Documentation

URL: `GET /api/devdocs/`

Currently, only reachable if `settings.DEBUG=True`. Lists all APIs of the system and what the frontend uses throughout
the whole application. 
