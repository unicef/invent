import { combineReducers } from 'redux';
import thunk from 'redux-async-thunk';
// import user from './modules/user';
// import projects from './modules/projects';
// import system from './modules/system';
import cms from './modules/cms';
// import countries from './modules/countries';
// import toolkit from './modules/toolkit';

const reducers = combineReducers({
  // user,
  // projects,
  // system,
  cms
  // countries
  // toolkit
});

const middleware = [thunk];

export {
  reducers,
  middleware
};
