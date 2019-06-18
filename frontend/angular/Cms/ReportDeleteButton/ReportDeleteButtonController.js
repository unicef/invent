import { actions } from '../../store/modules/cms';

class ReportDeleteButtonController {
  constructor ($ngRedux) {
    this.$onInit = this.onInit.bind(this);
    this.unsubscribe = $ngRedux.connect(() => { return {}; }, actions)(this);
  }

  onInit () {
    this.isDelete = this.type && this.type === 'delete';
    this.status = this.item.state === 2 && !this.isDelete ? 'reported' : 'close';
  }

  open () {
    this.status = 'active';
  }

  close () {
    this.status = 'close';
  }

  doReport () {
    if (this.item.user) {
      this.reportComment(this.item);
    } else {
      this.reportContent(this.item);
    }
    this.status = 'reported';
  }

  doDelete () {
    if (this.item.user) {
      this.deleteComment(this.item);
    } else {
      this.deleteContent(this.item);
    }
  }

  doAction () {
    this.isDelete ? this.doDelete() : this.doReport();
  }

  static factory () {
    require('./ReportDeleteButton.scss');
    function reportButton ($ngRedux) {
      return new ReportDeleteButtonController($ngRedux);
    }
    reportButton.$inject = ['$ngRedux'];
    return reportButton;
  }
}

export default ReportDeleteButtonController;
