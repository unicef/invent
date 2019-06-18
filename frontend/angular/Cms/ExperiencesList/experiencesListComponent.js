import ExperiencesListController from './ExperiencesListController';
import _template from './ExperiencesList.html';

const component = {
  template: _template,
  controller: ExperiencesListController.factory(),
  controllerAs: 'vm',
  name: 'cmsExperiencesList',
  bindings: {
    domainId: '<',
    axisId: '<'
  }
};

export default component;
