import _template from './Linechart.html';
import LinechartController from './LinechartController';

const linechart = {
  controller: LinechartController.linechartFactory(),
  controllerAs: 'vm',
  template: _template,
  bindings: {
    showdotted: '=',
    datachooser: '=',
    notpercentage: '='
  },
  name: 'linechart'
};

export default linechart;
