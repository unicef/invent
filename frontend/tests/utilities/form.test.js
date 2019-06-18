
import { mapGettersActions } from '~/utilities/form';
import debounce from 'lodash/debounce';
jest.mock('lodash/debounce', () => jest.fn(fn => fn));

// we need this in the next tests so the test is a fully fledged function
describe('mapGettersActions', function () {
  const initStore = () => {
    this.$store = {
      value: null,
      dispatch: jest.fn((action, val) => { this.$store.value = 'fromStore'; }),
      getters: {}
    };
  };
  const initProxy = (timeout, skipGetter) => {
    initStore();
    const self = this;
    const { toTest } = mapGettersActions({
      toTest: ['testModule', 'getTest', 'setTest', timeout, skipGetter]
    });
    Object.defineProperty(this.$store.getters, 'testModule/getTest', {
      get () {
        return self.$store.value;
      }
    });
    toTest.set = toTest.set.bind(self);
    toTest.get = toTest.get.bind(self);
    return toTest;
  };
  beforeEach(() => {
    debounce.mockClear();
  });
  it('returns the getterValue if localValue is null', () => {
    const toTest = initProxy(1, false);
    this.$store.value = 'fromStore';
    expect(toTest.get()).toEqual('fromStore');
  });
  it('debounce with wait time bigger than zero', () => {
    const toTest = initProxy(1, false);
    toTest.set(1);
    expect(debounce).toHaveBeenCalledTimes(2);
  });
  it('does not debounce with zero wait time', () => {
    const toTest = initProxy(0, false);
    toTest.set(1);
    expect(debounce).toHaveBeenCalledTimes(1);
  });
  it('keeps in sync with vuex: fixes issue #1184', () => {
    const toTest = initProxy(300, true);
    toTest.set('fromModule');
    expect(toTest.get()).toEqual('fromStore');
  });
  it('does not try to sync if the store is not set', () => {
    const toTest = initProxy(300, true);
    this.$store = null;
    toTest.set('fromModule');
    expect(toTest.get()).toEqual('fromModule');
  });
});
