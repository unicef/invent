export default function ({ store, req, app, redirect, route }) {
  const profile = store.getters['user/getProfile']
  if (profile && profile.language && profile.language !== app.i18n.locale) {
    const name = route.name.split('___')[0]
    const path = app.localePath({ ...route, name }, profile.language)
    redirect(path)
  }
}
