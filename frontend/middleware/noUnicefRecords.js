import auth from './auth.js'

export default async function ({ store, req, redirect, app }) {
  if (process.client) {
    const authOkay = await auth({ store, req })
    const token = store.getters['user/getToken']
    if (authOkay && token) {
      const unicefOrganisation = store.getters['system/getUnicefOrganisation']
      const unicefDonor = store.getters['system/getUnicefDonor']
      if (!unicefOrganisation || !unicefDonor) {
        store.dispatch('layout/setShowNoUnicefOrgOrDonor', true)
        store.dispatch('user/doLogout')
        if (process.client) {
          window.localStorage.removeItem('jwt_token')
          window.localStorage.removeItem('profile_id')
        }
        redirect(app.localePath({ name: 'auth' }))
      }
    }
  }
}
