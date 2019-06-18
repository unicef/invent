import _template from './Thematic.html';
import ThematicController from './ThematicController';

const thematicComponent = {
  controller: ThematicController.thematicFactory(),
  template: _template,
  controllerAs: 'vm',
  name: 'thematic',
  bindings: {
    'axis': '<',
    'domain': '<',
    'buttonclass': '@',
    'buttontext': '@',
    'buttontitle': '@',
    'buttonicon': '@'
  }
};

export default thematicComponent;
