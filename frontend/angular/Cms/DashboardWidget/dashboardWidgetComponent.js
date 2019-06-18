import DashboardWidgetController from './DashboardWidgetController';
import _template from './DashboardWidget.html';

const component = {
  template: _template,
  controller: DashboardWidgetController.factory(),
  controllerAs: 'vm',
  name: 'cmsDashboardWidget',
  bindings: {
    scores: '<'
  }
};

export default component;
