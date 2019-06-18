import AssessmentModuleController from './AssessmentModuleController';
import _template from './Assessment.html';
import './Assessment.scss';

const assessmentComponent = {
  controller: AssessmentModuleController.factory(),
  template: _template,
  controllerAs: 'vm',
  name: 'assessment',
  bindings: {
    viewMode: '@'
  }
};

export default assessmentComponent;
