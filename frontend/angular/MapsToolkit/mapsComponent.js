import MapsToolkitController from './MapsToolkitController';
import _template from './MapsToolkitModule.html';
import './MapsToolkit.scss';

const hssComponent = {
  controller: MapsToolkitController.mapsControllerFactory(),
  template: _template,
  controllerAs: 'vm',
  name: 'mapsToolkit',
  bindings: {
    viewMode: '@'
  }
};

export default hssComponent;
