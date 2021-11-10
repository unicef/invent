export default function ({ route, store }) {
  route.meta.matomo = {
    userId: ['setUserId', store.state.user.profile.email],
  }
}
