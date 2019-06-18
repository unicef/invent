import angular from 'angular';
import ngSanitize from 'angular-sanitize';
import 'angular-ui-router';
import 'angular-messages';
import 'angular-material';
import 'ng-redux';
import 'angular-gettext';
import { reducers, middleware } from '../store/index';
import { actions } from '../store/modules/cms';

import mapsComponent from './mapsComponent';
import scorecardComponent from './Scorecard/scorecardComponent';
import axisFooterComponent from './AxisFooter/axisFooterComponent';
import staticInfoWidgetComponent from '../Cms/StaticInfoWidget/staticInfoWidgetComponent';
import experiencesListComponent from '../Cms/ExperiencesList/experiencesListComponent';
import listElementComponent from '../Cms/ListElement/listElementComponent';
import detailElementComponent from '../Cms/DetailElement/detailElementComponent';
import commentWidgetComponent from '../Cms/CommentWidget/commentWidgetComponent';
import axisComponent from '../Common/Axis/axisComponent';
import trixComponent from '../Common/TrixComponent/trixComponent';
import thematicComponent from '../Thematic/thematicComponent';

const config = ($stateProvider, $locationProvider, $ngReduxProvider) => {
  $stateProvider
    .state('mapsToolkit', {
      url: '/:lng/:org/projects/:id/toolkit/?:axisId&:domainId',
      params: {
        axisId: '0',
        domainId: '0',
        lng: window.$nuxt.$i18n.locale,
        id: window.$nuxt.$route.params.id,
        org: window.$nuxt.$route.params.organisation
      },
      template: '<maps-toolkit layout="column" layout-fill></maps-toolkit>',
      resolve: {
        cms: ['$ngRedux', ($ngRedux) => {
          return $ngRedux.dispatch(actions.loadCmsData());
        }]
      }
    })
    .state('scorecard', {
      url: '/:lng/:org/projects/:id/toolkit/scorecard?:axisId',
      params: {
        axisId: '0',
        lng: window.$nuxt.$i18n.locale,
        id: window.$nuxt.$route.params.id,
        org: window.$nuxt.$route.params.organisation
      },
      template: '<scorecard ></scorecard>'
    })
    .state('summary', {
      url: '/:lng/:org/projects/:id/toolkit/summary',
      params: {
        lng: window.$nuxt.$i18n.locale,
        id: window.$nuxt.$route.params.id,
        org: window.$nuxt.$route.params.organisation
      },
      template: '<scorecard layout-fill layout="column" summary="true"></scorecard>'
    });

  $locationProvider.html5Mode(true);

  const reduxDevTools = window.__REDUX_DEVTOOLS_EXTENSION__;
  const storeExtension = reduxDevTools ? [reduxDevTools()] : undefined;
  $ngReduxProvider.createStoreWith(reducers, middleware, storeExtension);
};

config.$inject = ['$stateProvider', '$locationProvider', '$ngReduxProvider'];

const run = (gettextCatalog) => {
  const ln = window.$nuxt.$i18n.locale;
  gettextCatalog.setCurrentLanguage(ln);
  gettextCatalog.setStrings(ln, window.$nuxt.$i18n.messages[ln]);
};

run.$inject = ['gettextCatalog'];

export const factory = () => {
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

  angular.module('mapsToolkit', [
    'ui.router',
    'ngMaterial',
    'ngMessages',
    'ngRedux',
    'gettext',
    'ngHtmlCompile',
    ngSanitize
  ])
    .component(mapsComponent.name, mapsComponent)
    .component(scorecardComponent.name, scorecardComponent)
    .component(axisFooterComponent.name, axisFooterComponent)
    .component(staticInfoWidgetComponent.name, staticInfoWidgetComponent)
    .component(experiencesListComponent.name, experiencesListComponent)
    .component(listElementComponent.name, listElementComponent)
    .component(detailElementComponent.name, detailElementComponent)
    .component(commentWidgetComponent.name, commentWidgetComponent)
    .component(trixComponent.name, trixComponent)
    .component(axisComponent.name, axisComponent)
    .component(thematicComponent.name, thematicComponent)
    .config(config)
    .run(run);

  const toolkitjs = document.querySelector('#toolkitjs');
  const uiView = document.createElement('ui-view');
  toolkitjs.appendChild(uiView);

  angular.bootstrap(toolkitjs, ['mapsToolkit']);
};
