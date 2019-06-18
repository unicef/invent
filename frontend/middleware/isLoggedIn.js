import auth from './auth.js';

export default async function ({ store, req, redirect, app, route }) {
  const authOkay = await auth({ store, req });
  if (!authOkay) {
    const path = app.localePath({ name: 'organisation-login', params: route.params, query: { ...route.query, next: route.path } });
    redirect(path);
  }
}
