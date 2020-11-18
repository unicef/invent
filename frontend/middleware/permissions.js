export default function ({ app, store, route, redirect }) {
  const user = store.state.user.profile
  const routeName = route.name.split('___')[0]
  const routeObserver = [
    'organisation-portfolio-management',
    'organisation-portfolio-managementmanagement-id-edit',
    'organisation-portfolio-managementmanagement-new',
    'organisation-portfolio-managementmanagement-id',
  ]
  const permissions =
    (user && user.is_superuser) ||
    (user && user.global_portfolio_owner) ||
    (user && user.manager.length > 0)
  if (routeObserver.includes(routeName)) {
    if (permissions) {
      if (
        routeName === 'organisation-portfolio-managementmanagement-new' &&
        !user.global_portfolio_owner
      ) {
        redirect(
          app.localePath({
            name: 'organisation',
            params: { organisation: '-' },
          })
        )
      }
    } else {
      redirect(
        app.localePath({
          name: 'organisation',
          params: { organisation: '-' },
        })
      )
    }
  }
}
