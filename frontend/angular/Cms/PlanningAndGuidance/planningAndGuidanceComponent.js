import PlanningAndGuidanceController from './PlanningAndGuidanceController';
import _template from './PlanningAndGuidance.html';

const component = {
  template: _template,
  controller: PlanningAndGuidanceController.factory(),
  controllerAs: 'vm',
  name: 'planningAndGuidance',
  bindings: {}
};

export default component;
