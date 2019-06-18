import CommentWidgetController from './CommentWidgetController';
import _template from './CommentWidget.html';

const component = {
  template: _template,
  controller: CommentWidgetController.factory(),
  controllerAs: 'vm',
  name: 'cmsCommentWidget',
  bindings: {
    comment: '<',
    type: '<'
  }
};

export default component;
