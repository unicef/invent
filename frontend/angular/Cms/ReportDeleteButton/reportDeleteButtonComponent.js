import ReportDeleteButtonController from './ReportDeleteButtonController';
import _template from './ReportDeleteButton.html';

const component = {
  template: _template,
  controller: ReportDeleteButtonController.factory(),
  controllerAs: 'vm',
  name: 'cmsReportDeleteButton',
  bindings: {
    item: '<',
    type: '@?'
  }
};

export default component;
