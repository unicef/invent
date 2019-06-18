import StaticInfoWidget from './StaticInfoWidgetController';
import _template from './StaticInfoWidget.html';

const component = {
  template: _template,
  controller: StaticInfoWidget.factory(),
  controllerAs: 'vm',
  name: 'cmsStaticInfoWidget',
  bindings: {}
};

export default component;
