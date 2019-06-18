const dialog = {
  cancel: jest.fn(),
  hide: jest.fn(),
  alert: jest.fn().mockReturnValue({ type: 'alert' }),
  confirm: jest.fn().mockReturnValue({ type: 'confirm' }),
  show: jest.fn().mockImplementation((config) => {
    if (config.onComplete) {
      config.onComplete();
    }
    return Promise.resolve();
  })
};

const $state = () => ({
  params: {},
  current: {},
  go: jest.fn()
});

const $scope = (controller) => {
  return {
    $watchGroup: jest.fn().mockImplementation((toCallArray, action) => {
      action(toCallArray.map(call => call({ vm: controller })));
    }),
    $watchCollection: jest.fn().mockImplementation((toCall, action) => action(toCall({
      vm: controller
    }))),
    $watch: jest.fn().mockImplementation((toCall, action) => action(toCall({
      vm: controller
    }))),
    $evalAsync: jest.fn().mockImplementation(toCall => {
      if (toCall) {
        toCall();
      }
    })
  };
};

const toast = {};

toast.show = jest.fn().mockReturnValue(toast);
toast.simple = jest.fn().mockReturnValue(toast);
toast.parent = jest.fn().mockReturnValue(toast);
toast.position = jest.fn().mockReturnValue(toast);
toast.textContent = jest.fn().mockReturnValue(toast);
toast.hideDelay = jest.fn().mockReturnValue(toast);

const $timeout = toCall => {
  return toCall();
};

const $interpolate = jest.fn().mockReturnValue(() => {});
const $anchorScroll = jest.fn().mockImplementation(a => a);

const EE = {
  emit: jest.fn(),
  on: jest.fn(),
  removeAllListeners: jest.fn(),
  removeListener: jest.fn()
};

const $ngRedux = {
  connect: jest.fn().mockReturnValue(() => jest.fn().mockReturnValue('unsubscribeFn')),
  dispatch: jest.fn().mockImplementation(toCall => toCall()),
  getState: jest.fn(),
  subscribe: jest.fn()
};

const angularForm = {
  $setUntouched: jest.fn(),
  $setPristine: jest.fn()
};

const $element = {};

const $location = {
  hash: jest.fn().mockImplementation(input => input)
};

const dispatch = jest.fn();
const getState = state => jest.fn().mockReturnValue(state);

const defaultAxiosSuccess = Promise.resolve({ data: 1 });

const gettextCatalog = {
  getString: jest.fn()
};

export {
  dialog,
  $state,
  $scope,
  $interpolate,
  $anchorScroll,
  toast,
  $timeout,
  EE,
  $ngRedux,
  angularForm,
  $element,
  $location,
  dispatch,
  defaultAxiosSuccess,
  getState,
  gettextCatalog
};
