import _template from './Countrymap.html';
import CountrymapController from './CountryMapController';

const coutrymap = {
  controller: CountrymapController.countrymapFactory(),
  controllerAs: 'vm',
  template: _template,
  name: 'countrymap',
  bindings: {
    big: '<',
    districtLevelCoverage: '<',
    nationalLevelCoverage: '<',
    mapData: '<'
  }
};

export default coutrymap;
