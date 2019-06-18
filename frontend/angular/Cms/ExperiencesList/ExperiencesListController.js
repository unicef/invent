import { getters, actions } from '../../store/modules/cms';

class ExperienceListController {
  constructor ($scope, $ngRedux) {
    this.scope = $scope;
    this.$ngRedux = $ngRedux;
    this.$onInit = this.onInit.bind(this);
    this.mapState = this.mapState.bind(this);
  }

  onInit () {
    this.watchers();
    this.unsubscribe = this.$ngRedux.connect(this.mapState, actions)(this);
  }

  mapState (state) {
    const domains = getters.getDomainStructureForCms(state);
    const axisIndex = parseInt(this.axisId, 10);
    const domainIndex = parseInt(this.domainId, 10);
    const domain = domains[axisIndex].domains[domainIndex];

    const newExperience = {
      body: null,
      valid: false,
      name: null,
      domain: domain.id,
      type: 3
    };

    return {
      data: getters.getCmsData(state),
      domains,
      domain,
      newExperience
    };
  }

  watchers () {
    this.scope.$watchCollection(() => {
      return this.data;
    }, data => {
      this.experiences = data.filter(exp => {
        return exp.domain === this.domain.id && exp.type === 3;
      });
    });
  }

  async saveExperience () {
    await this.saveOrUpdateContent(this.newExperience);
    this.newExperience.body = false;
    this.newExperience.name = null;
    this.form.$setUntouched();
    this.form.$setPristine();
  }

  disableAddButton (experience) {
    return !experience.valid || !experience.name || experience.name.length > 120;
  }

  static factory () {
    require('./ExperiencesList.scss');
    function experienceListController ($scope, $ngRedux) {
      return new ExperienceListController($scope, $ngRedux);
    }
    experienceListController.$inject = ['$scope', '$ngRedux'];
    return experienceListController;
  }
}

export default ExperienceListController;
