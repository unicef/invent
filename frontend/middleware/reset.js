export default function ({ app, store, route, redirect }) {
  if (!store.state.user.profile) {
    const validPaths = ['auth', 'organisation-login', 'organisation-reset-key']
    let noRedirect = false
    if (route.name) {
      validPaths.forEach(function (pathName) {
        const currentPath = route.name.split('___')[0]
        if (currentPath === pathName) {
          noRedirect = true
        }
      })
    }
    if (!noRedirect) {
      const path = app.localePath({
        name: 'auth',
        query: { next: route.fullPath },
      })
      redirect(path)
    }
  }
}
