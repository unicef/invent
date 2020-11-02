export default function ({ app, store, route, redirect }) {
  const user = store.state.user.profile
  const routeName = route.name.split('___')[0]
  const routeObserver = [
    'organisation-portfolio-management',
    'organisation-portfolio-management-edit-id',
    'organisation-portfolio-management-new',
    'organisation-portfolio-management-id',
  ]
  const permissions =
    (user && user.is_superuser) ||
    (user && user.global_portfolio_owner) ||
    (user && user.manager.length > 0)
  if (routeObserver.includes(routeName)) {
    if (permissions) {
      if (
        routeName === 'organisation-portfolio-management-new' &&
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
