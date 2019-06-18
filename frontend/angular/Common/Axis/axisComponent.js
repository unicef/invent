import _template from './Axis.html';
import AxisController from './AxisController';

const axisComponent = {
  controller: AxisController.axisFactory(),
  template: _template,
  controllerAs: 'vm',
  name: 'axis',
  bindings: {
    axisIndex: '<',
    showCurrent: '@',
    domainIndex: '<'
  }
};

export default axisComponent;
