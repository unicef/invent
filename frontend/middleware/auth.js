import { getTokenFromCookie, getTokenFromLocalStorage } from '../utilities/auth'

export default async function ({ store, req }) {
  const tokens = process.server
    ? getTokenFromCookie(req)
    : getTokenFromLocalStorage()
  if (tokens && tokens.jwt && tokens.profileId) {
    try {
      await store.dispatch('user/setToken', tokens)
    } catch (e) {
      return false
    }
    return true
  }
  return false
}
