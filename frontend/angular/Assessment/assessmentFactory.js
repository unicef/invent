import angular from 'angular';
import ngSanitize from 'angular-sanitize';
import 'angular-ui-router';
import 'angular-messages';
import 'angular-material';
import 'ng-redux';
import 'angular-gettext';

import { reducers, middleware } from '../store/index';
import { actions } from '../store/modules/cms';

import assessmentComponent from './assessmentComponent';
import lineChartComponent from './Linechart/linechart';
import statisticsComponent from './Statistics/statisticsComponent';
import countryMapComponent from './CountryMap/countrymap';
import axisComponent from '../Common/Axis/axisComponent';
import cmsDahsboardWidget from '../Cms/DashboardWidget/dashboardWidgetComponent';
import listElement from '../Cms/ListElement/listElementComponent';
import detailElement from '../Cms/DetailElement/detailElementComponent';
import commentWidget from '../Cms/CommentWidget/commentWidgetComponent';
import reportButton from '../Cms/ReportDeleteButton/reportDeleteButtonComponent';
import trixComponent from '../Common/TrixComponent/trixComponent';

function config ($stateProvider, $locationProvider, $ngReduxProvider) {
  $stateProvider
    .state('assessment', {
      url: '/:lng/:org/projects/:id/assessment',
      template: '<assessment></assessment>',
      resolve: {
        cms: ['$ngRedux', ($ngRedux) => {
          return $ngRedux.dispatch(actions.loadCmsData());
        }]
      }
    });
  $locationProvider.html5Mode(true);

  const reduxDevTools = window.__REDUX_DEVTOOLS_EXTENSION__;
  const storeExtension = reduxDevTools ? [reduxDevTools()] : undefined;
  $ngReduxProvider.createStoreWith(reducers, middleware, storeExtension);
}

config.$inject = ['$stateProvider', '$locationProvider', '$ngReduxProvider'];

const run = (gettextCatalog) => {
  const ln = window.$nuxt.$i18n.locale;
  gettextCatalog.setCurrentLanguage(ln);
  gettextCatalog.setStrings(ln, window.$nuxt.$i18n.messages[ln]);
};

run.$inject = ['gettextCatalog'];

export const assesmentFactory = () => {
  angular.module('assessment', [
    'ui.router',
    'ngMaterial',
    'ngMessages',
    'ngRedux',
    'gettext',
    ngSanitize
  ])
    .component(assessmentComponent.name, assessmentComponent)
    .component(lineChartComponent.name, lineChartComponent)
    .component(statisticsComponent.name, statisticsComponent)
    .component(countryMapComponent.name, countryMapComponent)
    .component(axisComponent.name, axisComponent)
    .component(cmsDahsboardWidget.name, cmsDahsboardWidget)
    .component(listElement.name, listElement)
    .component(detailElement.name, detailElement)
    .component(commentWidget.name, commentWidget)
    .component(reportButton.name, reportButton)
    .component(trixComponent.name, trixComponent)
    .config(config)
    .run(run);

  const assessmentjs = document.querySelector('#assessmentjs');
  const uiView = document.createElement('ui-view');
  assessmentjs.appendChild(uiView);

  angular.bootstrap(assessmentjs, ['assessment']);
};
