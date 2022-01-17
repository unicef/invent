import auth from './auth.js'

export default async function ({ store, req, redirect, app }) {
  const authOkay = await auth({ store, req })
  if (authOkay) {
    const unicefOrganisation = store.getters['system/getUnicefOrganisation']
    const unicefDonor = store.getters['system/getUnicefDonor']
    if (!unicefOrganisation || !unicefDonor) {
      store.dispatch('layout/setShowNoUnicefOrgOrDonor', true)
      store.dispatch('user/doLogout')
      redirect(app.localePath({ name: 'auth' }))
    }
  }
}
