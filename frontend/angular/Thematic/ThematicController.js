import angular from 'angular';
import SkeletonController from './SkeletonController.js';

class ThematicController {
  constructor ($mdDialog, $scope) {
    this.modal = $mdDialog;
    this.scope = $scope;
    this.$onInit = this.onInit.bind(this);
  }

  onInit () {
    this.data = window.$nuxt.$store.getters['system/getDomainsForThematic'];
    this.icons = this.data.map((el, i) => require('./images/icon-axis' + (i - 1) + '.svg'));
  }

  showModal () {
    this.axis = parseInt(this.axis, 10);
    this.domain = parseInt(this.domain, 10);
    this.modal.show({
      parent: angular.element(document.body),
      template: require('./modal-skeleton.html'),
      controller: SkeletonController.factory(this.data, this.axis, this.domain, this.icons, this.modal),
      controllerAs: 'vm',
      clickOutsideToClose: true,
      fullScreen: true
    });
  }

  static thematicFactory () {
    const thematic = ($mdDialog, $scope) => {
      require('./Thematic.scss');
      return new ThematicController($mdDialog, $scope);
    };
    thematic.$inject = ['$mdDialog', '$scope'];
    return thematic;
  }
}

export default ThematicController;
