
import angular from 'angular';
import ngSanitize from 'angular-sanitize';
import 'angular-material';
import 'angular-gettext';

import thematicComponent from './thematicComponent';

angular.module('ngHtmlCompile', [])
  .directive('ngHtmlCompile', ['$compile', ($compile) => {
    return {
      restrict: 'A',
      link (scope, element, attrs) {
        scope.$watch(attrs.ngHtmlCompile, (newValue) => {
          element.html(newValue);
          $compile(element.contents())(scope);
        });
      }
    };
  }]);

function run (gettextCatalog) {
  const ln = window.$nuxt.$i18n.locale;
  gettextCatalog.setCurrentLanguage(ln);
  gettextCatalog.setStrings(ln, window.$nuxt.$i18n.messages[ln]);
};

run.$inject = ['gettextCatalog'];

export const factory = (axis, domain, buttontitle, buttonclass, buttontext) => {
  angular.module('thematic', [
    'ngMaterial',
    'gettext',
    ngSanitize,
    'ngHtmlCompile'
  ])
    .component(thematicComponent.name, thematicComponent)
    .run(run);

  const thematicjs = document.querySelector('#thematicjs');
  const component = document.createElement('thematic');
  component.setAttribute('axis', axis);
  component.setAttribute('domain', domain);
  component.setAttribute('buttontitle', buttontitle);
  component.setAttribute('buttonclass', buttonclass);
  component.setAttribute('buttontext', buttontext);
  thematicjs.appendChild(component);

  angular.bootstrap(thematicjs, ['thematic']);
};
