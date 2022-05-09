# Country focal point

The contry focal point is a permission level by which a user will have permission to a given country's all projects as a `team member`.

## Frontend

User's profile is provided by `getProfile` getter in `user` store. The property `manager_of` contains a list of country Ids that the user is focal point of.
The membership or permission to an actual project is calculated by looking for the project's `country id` in this `manager_of` property of the currently logged in user.