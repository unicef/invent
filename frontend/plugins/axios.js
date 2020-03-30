export default function ({ $axios, store: { getters, dispatch }, redirect, app: { i18n } }) {
  $axios.onRequest(config => {
    const token = getters['user/getToken'];
    const lng = i18n.locale;
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    if (lng) {
      config.headers['Accept-Language'] = lng;
    }
    return config;
  });

  $axios.onError(error => {
    const code = parseInt(error.response && error.response.status);
    if (code === 401) {
      dispatch('user/doLogout');
      redirect('/en/-/');
    }
  });
}
