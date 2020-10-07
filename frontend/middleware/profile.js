export default function ({ store, redirect, app, route }) {
  const profile = store.getters['user/getProfile']
  const donorTypes = ['D', 'DA', 'SDA']
  const routeName = route.name.split('___')[0]
  if (
    routeName !== 'organisation-edit-profile' &&
    profile &&
    (!profile.name ||
      !profile.country ||
      !profile.organisation ||
      !profile.account_type ||
      (donorTypes.includes(profile.account_type) && !profile.donor))
  ) {
    const path = app.localePath({
      name: 'organisation-edit-profile',
      params: route.params,
      query: { missingProfile: true },
    })
    redirect(path)
  }
}
