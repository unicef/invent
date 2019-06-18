import _template from './AxisFooter.html';
import AxisFooterController from './AxisFooterController';

const axisFooterComponent = {
  controller: AxisFooterController.axisFooterFactory(),
  template: _template,
  controllerAs: 'vm',
  bindings: {
    axes: '<'
  },
  name: 'axisFooter'
};

export default axisFooterComponent;
