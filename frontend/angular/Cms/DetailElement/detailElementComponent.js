import DetailElementController from './DetailElementController';
import _template from './DetailElement.html';

const component = {
  template: _template,
  controller: DetailElementController.factory(),
  controllerAs: 'vm',
  name: 'cmsDetailElement',
  bindings: {
    item: '<'
  }
};

export default component;
