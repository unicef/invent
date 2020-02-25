import Cookie from 'js-cookie';

export const safeSaveToken = (name, value) => {
  if (value) {
    if (process.client) {
      window.localStorage.setItem(name, value);
    }
    Cookie.set(name, value, { expires: 365 });
  }
};

export const saveToken = (token, profileId) => {
  if (process.SERVER_BUILD) return;
  safeSaveToken('jwt_token', token);
  safeSaveToken('profile_id', profileId);
};

export const deleteToken = () => {
  if (process.SERVER_BUILD) { return; }
  if (process.client) {
    window.localStorage.removeItem('jwt_token');
    window.localStorage.removeItem('profile_id');
  }
  Cookie.remove('jwt_token');
  Cookie.remove('profile_id');
};

export const getValueFromCookie = (req, value) => {
  const result = req.headers.cookie.split(';').find(c => c.trim().startsWith(`${value}=`));
  return result ? result.split('=')[1] : null;
};

export const getTokenFromCookie = (req) => {
  if (!req.headers.cookie) { return; }
  const jwt = getValueFromCookie(req, 'jwt_token');
  const profileId = getValueFromCookie(req, 'profile_id');
  return { jwt, profileId };
};

export const getTokenFromLocalStorage = () => {
  const jwt = window.localStorage.getItem('jwt_token');
  const profileId = window.localStorage.getItem('profile_id');
  return { jwt, profileId };
};
