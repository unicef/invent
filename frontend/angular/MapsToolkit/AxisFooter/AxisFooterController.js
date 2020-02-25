class AxisFooterController {
  constructor ($scope, $state) {
    this.scope = $scope;
    this.state = $state;
    this.$onInit = this.onInit.bind(this);
    this.$onDestroy = this.onDestroy.bind(this);
    this.changeAxis = this.changeAxis.bind(this);
  }

  onInit () {
    this.activeAxis = this.state.params.axisId;
    this.processedAxis = this.axes.map((axis, index) => {
      const stored = window.$nuxt.$store.getters['toolkit/getAxisDetail'](axis.id);
      axis = Object.assign({}, axis, stored);
      axis.axisId = axis.axis.split('.')[0];
      axis.id = index;
      axis.isActive = this.activeAxis === '' + index;
      return axis;
    });
  }

  onDestroy () {
  }

  classGenerator (axis) {
    const classArray = [];
    classArray.push(axis.axisId.replace(' ', '_').toLowerCase());
    classArray.push(axis.isActive ? 'active' : 'notActive');
    return classArray.join(' ');
  }

  changeAxis (axis) {
    if (!axis.isActive) {
      window.$nuxt.$root.$emit('angularjs:mapsAxisChange', axis.id);
    }
  }

  static axisFooterFactory () {
    const axisFooter = ($scope, $state) => {
      require('./AxisFooter.scss');
      return new AxisFooterController($scope, $state);
    };
    axisFooter.$inject = ['$scope', '$state'];
    return axisFooter;
  }
}

export default AxisFooterController;
