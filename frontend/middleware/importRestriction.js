export default function ({ store, redirect, app, route }) {
  const profile = store.getters['user/getProfile']
  const routeName = route.name.split('___')[0]
  if (
    routeName === 'organisation-admin-import' &&
    profile &&
    !profile.is_superuser &&
    !(
      profile.account_type_approved &&
      ['DA', 'SDA'].includes(profile.account_type)
    )
  ) {
    const path = app.localePath({ name: 'organisation', params: route.params })
    redirect(path)
  }
}
