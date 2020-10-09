import angular from 'angular'
import ngSanitize from 'angular-sanitize'
import 'angular-ui-router'
import 'angular-messages'
import 'angular-material'
import 'ng-redux'
import 'angular-gettext'
import ngFileUpload from 'ng-file-upload'

import { actions } from '../store/modules/cms'
import { reducers, middleware } from '../store/index'

import trixComponent from '../Common/TrixComponent/trixComponent'
import addNewContent from './AddNewContent/addNewContentComponent'
import commentWidget from './CommentWidget/commentWidgetComponent'
import detailElement from './DetailElement/detailElementComponent'
import listElement from './ListElement/listElementComponent'
import reportButton from './ReportDeleteButton/reportDeleteButtonComponent'
import planningAndGuidanceComponent from './PlanningAndGuidance/planningAndGuidanceComponent'

function config($stateProvider, $locationProvider, $ngReduxProvider) {
  $stateProvider.state('cms', {
    url: '/:lng/:org/cms',
    template: '<planning-and-guidance></planning-and-guidance>',
    resolve: {
      cms: [
        '$ngRedux',
        ($ngRedux) => {
          return $ngRedux.dispatch(actions.loadCmsData())
        },
      ],
    },
  })
  $locationProvider.html5Mode(true)

  $ngReduxProvider.createStoreWith(reducers, middleware)
}

config.$inject = ['$stateProvider', '$locationProvider', '$ngReduxProvider']

const run = (gettextCatalog) => {
  const ln = window.$nuxt.$i18n.locale
  gettextCatalog.setCurrentLanguage(ln)
  gettextCatalog.setStrings(ln, window.$nuxt.$i18n.messages[ln])
}

run.$inject = ['gettextCatalog']

export const cmsFactory = () => {
  angular
    .module('cms', [
      'ui.router',
      'ngMaterial',
      'ngMessages',
      'ngRedux',
      'gettext',
      ngSanitize,
      ngFileUpload,
    ])
    .component(addNewContent.name, addNewContent)
    .component(commentWidget.name, commentWidget)
    .component(detailElement.name, detailElement)
    .component(listElement.name, listElement)
    .component(reportButton.name, reportButton)
    .component(planningAndGuidanceComponent.name, planningAndGuidanceComponent)
    .component(trixComponent.name, trixComponent)
    .config(config)
    .run(run)

  const cmsjs = document.querySelector('#cmsjs')
  const uiView = document.createElement('ui-view')
  cmsjs.appendChild(uiView)

  angular.bootstrap(cmsjs, ['cms'])
}
