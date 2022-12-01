import axios from 'axios'
export default (ln) => {
  const base =
    process.server && process.env.NODE_ENV === 'production'
      ? 'http://localhost:80'
      : ''
  return axios.get(`${base}/translation/json/`, {
    headers: {
      'Accept-Language': ln,
    },
  })
}
