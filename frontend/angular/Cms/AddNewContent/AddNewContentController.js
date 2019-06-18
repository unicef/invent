import angular from 'angular';
import { getters, actions } from '../../store/modules/cms';

class AddNewContentDialog {
  constructor ($scope, $mdDialog, Upload, toast, $ngRedux, content) {
    this.scope = $scope;
    this.dialog = $mdDialog;
    this.upload = Upload;
    this.toast = toast;
    this.showTrixError = false;
    this.disableSubmit = false;
    this.newContent = content;
    this.unsubscribe = $ngRedux.connect(this.mapState, actions)(this);
    this.userProfile = window.$nuxt.$store.getters['user/getProfile'];
    this.isSuperUser = this.userProfile.is_superuser;
    window.THIS = this;
  }

  mapState (state) {
    return {
      axes: getters.getDomainStructureForCms(state),
      global: getters.getCmsData(state)
    };
  }

  cancel () {
    this.dialog.cancel();
  }

  async submit () {
    if (this.form.$valid && this.newContent.textValid) {
      try {
        this.saveOrUpdateContent(this.newContent);
        this.dialog.hide(this.newContent);
      } catch (e) {
        console.log(e);
        this.showToast('Validation error');
      }
    } else {
      if (!this.newContent.textValid) {
        this.showTrixError = true;
      }
      this.showToast('Validation error');
    }
  }

  beforeImageSelect () {
    this.disableSubmit = true;
  }

  imageSelected () {
    this.disableSubmit = false;
  }

  showToast (text) {
    this.toast.show(
      this.toast.simple()
        .parent(window.document.querySelector('md-dialog'))
        .textContent(text)
        .position('bottom right')
        .hideDelay(3000)
    );
  }

  static factory (content, isSuperUser) {
    function addNewContent ($scope, $mdDialog, Upload, $mdToast, $ngRedux) {
      return new AddNewContentDialog($scope, $mdDialog, Upload, $mdToast, $ngRedux, content, isSuperUser);
    }

    addNewContent.$inject = ['$scope', '$mdDialog', 'Upload', '$mdToast', '$ngRedux'];
    return addNewContent;
  }
}

class AddNewContentController {
  constructor ($scope, $mdDialog) {
    this.scope = $scope;
    this.dialog = $mdDialog;
  }

  showAddNewContentDialog (event) {
    const self = this;
    const content = this.toEdit ? Object.assign({}, this.toEdit) : {};
    self.scrollTop = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop);
    document.documentElement.scrollTop = 0;

    this.dialog.show({
      controller: AddNewContentDialog.factory(content),
      controllerAs: 'vm',
      template: require('./AddNewContentDialog.html'),
      parent: angular.element(document.body),
      targetEvent: event,
      clickOutsideToClose: true
    }).finally(() => {
      document.documentElement.scrollTop = self.scrollTop;
    });
  }

  static factory () {
    require('./AddNewContent.scss');

    function addNewContent ($scope, $mdDialog) {
      return new AddNewContentController($scope, $mdDialog);
    }

    addNewContent.$inject = ['$scope', '$mdDialog'];
    return addNewContent;
  }
}

export default AddNewContentController;
export { AddNewContentDialog };
