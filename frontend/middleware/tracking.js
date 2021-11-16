export default function ({ route, store }) {
  if (store.state.user.profile) {
    route.meta.matomo = {
      userId: ['setUserId', store.state.user.profile.email],
    }
  }
}
