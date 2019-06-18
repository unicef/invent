import TrixComponentController from './TrixComponentController';
import _template from './TrixComponent.html';

const component = {
  template: _template,
  controller: TrixComponentController.factory(),
  controllerAs: 'vm',
  name: 'trixComponent',
  bindings: {
    value: '=?',
    placeholder: '@?',
    charLimit: '<?',
    valid: '=',
    showError: '<?'
  }
};

export default component;
