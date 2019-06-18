
class AxisController {
  constructor ($scope, $ngRedux) {
    this.scope = $scope;
    this.$ngRedux = $ngRedux;
    this.EE = window.EE;
    this.$onInit = this.onInit.bind(this);
    this.$onDestroy = this.onDestroy.bind(this);
    this.changeDomain = this.changeDomain.bind(this);
  }

  onInit () {
    this.axisId = parseInt(this.axisIndex, 10) + 1;
    if (this.axisId === null || this.axisId === void 0) {
      this.axisId = 0;
    }
    this.domainId = this.domainIndex ? parseInt(this.domainIndex, 10) + 1 : null;
    this.axis = window.$nuxt.$store.getters['toolkit/getAxisDetail'](this.axisId);
    this.axisClass = this.axis.axis.split('.')[0].replace(' ', '').toLowerCase();
    this.axisPicture = require('./images/icon-' + this.axisClass + '.svg');
    const axisScorePercentage = this.axis.axis_score;
    const axisCompletion = this.axis.axis_completion;
    this.axisScoreClass = this.advanceClassGenerator(axisScorePercentage);
    this.axisCompletionClass = this.advanceClassGenerator(axisCompletion);
    this.domains = this.axis.domains;
    this.axisName = this.axis.name;
  }

  onDestroy () {}

  setDomainActive (id) {
    if (this.domainIndex) {
      return parseInt(this.domainIndex, 10) === id;
    }
    return false;
  }

  changeDomain (domain) {
    window.$nuxt.$root.$emit('angularjs:mapsDomainChange', this.axisIndex, domain.index);
  }

  goToAxis () {
    const axisId = parseInt(this.axisId, 10) - 1;
    window.$nuxt.$root.$emit('angularjs:mapsAxisChange', axisId);
  }

  advanceClassGenerator (value) {
    if (value < 50) {
      return 'red';
    }
    if (value < 100) {
      return 'yellow';
    }

    return 'green';
  }

  static axisFactory () {
    require('./Axis.scss');
    function newAxis ($scope, $ngRedux) {
      return new AxisController($scope, $ngRedux);
    }
    newAxis.$inject = ['$scope', '$ngRedux'];
    return newAxis;
  }
}

export default AxisController;
