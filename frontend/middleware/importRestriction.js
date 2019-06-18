export default async function ({ store, redirect, app, route }) {
  const profile = store.getters['user/getProfile'];
  const routeName = route.name.split('___')[0];
  if (routeName === 'organisation-admin-import' && profile && !profile.is_superuser) {
    const path = app.localePath({ name: 'organisation', params: route.params });
    redirect(path);
  }
};
