import AddNewContentController from './AddNewContentController';
import _template from './AddNewContent.html';

const component = {
  template: _template,
  controller: AddNewContentController.factory(),
  controllerAs: 'vm',
  name: 'cmsAddNewContent',
  bindings: {
    toEdit: '<?'
  }
};

export default component;
