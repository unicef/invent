# Tools

## Sentry

[Sentry](https://sentry.io/) is used to catch and track errors in the application.
### Backend

### Frontend

To log errors into Sentry the proper DSN has to be set in .env `SENTRY_DSN` key.

The [nuxt/sentry](https://sentry.nuxtjs.org/) modul automatically reports error and exception.
It also provides a global object (`$sentry`) by which custom events can be captured. 

```js
this.$sentry.captureMessage('Un-caught validation error in project page', {
  level: 'error',
  extra: {
    apiErrors: this.apiErrors,
    errors,
  },
})
```

For further options, please refer to the official [documentation](https://sentry.nuxtjs.org/guide/usage).


## Circle CI

## Jira