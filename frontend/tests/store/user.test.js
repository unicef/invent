/* eslint prefer-promise-reject-errors: 0 */
import { state, getters, actions, mutations } from '~/store/user';
import { mockAxios } from '../utils'; ;

test('user state is unique between calls', () => {
  const s = state();
  expect(s).not.toBe(state());
  expect(s).toEqual(state());
});

describe('getters', () => {
  let s = null;

  beforeEach(() => {
    s = state();
  });

  test('getToken', () => {
    expect(getters.getToken(s)).toEqual(s.token);
  });
});

describe('actions', () => {
  const vuex = {};

  beforeEach(() => {
    vuex.commit = jest.fn();
    vuex.dispatch = jest.fn();
    vuex.getters = {};
    vuex.state = state();
    actions.$axios = mockAxios();
  });

  test('setToken', async () => {
    await actions.setToken(vuex, { jwt: null });
    expect(vuex.commit.mock.calls[0]).toEqual(['SET_TOKEN', null]);

    await actions.setToken(vuex, { jwt: 1 });
    expect(vuex.commit.mock.calls[1]).toEqual(['SET_TOKEN', 1]);
  });
});

describe('mutations', () => {
  test('SET_TOKEN', () => {
    const s = {};
    mutations.SET_TOKEN(s, 1);
    expect(s.token).toEqual(1);
  });
});
