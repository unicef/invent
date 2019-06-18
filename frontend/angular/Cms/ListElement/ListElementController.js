import { prettifyDate, itemType, normalizeName, postProcessHtml } from '../utilities';
import { getters, actions } from '../../store/modules/cms';

class ListElementController {
  constructor ($ngRedux) {
    this.$ngRedux = $ngRedux;
    this.prettifyDate = prettifyDate;
    this.postProcessHtml = postProcessHtml;
    this.itemType = itemType;
    this.$onInit = this.onInit.bind(this);
    this.mapState = this.mapState.bind(this);
  }

  mapState (state) {
    return {
      axisAndDomainName: getters.getAxisAndDomainName(state, this.item.domain)
    };
  }

  onInit () {
    this.$ngRedux.connect(this.mapState, actions)(this);
  }

  typeClass (item) {
    return `type-${item.type}`;
  }

  showAxisAndDomain () {
    const result = this.axisAndDomainName;
    return `${result.axisName} - ${result.domainName}`;
  }

  axisAndDomainClass () {
    const r = { ...this.axisAndDomainName };
    r.domainName = normalizeName(r.domainName);
    r.axisName = normalizeName(r.axisName);
    return `axis-${r.axisName} domain-${r.domainName}`;
  }

  static factory () {
    require('./ListElement.scss');
    function listElement ($ngRedux) {
      return new ListElementController($ngRedux);
    }
    listElement.$inject = ['$ngRedux'];
    return listElement;
  }
}

export default ListElementController;
