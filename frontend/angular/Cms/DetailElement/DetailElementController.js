import angular from 'angular';

import { prettifyDate, itemType, postProcessHtml } from '../utilities';
import { getters, actions } from '../../store/modules/cms';

class DetailElementDialog {
  constructor ($scope, $mdDialog, $ngRedux, content) {
    this.scope = $scope;
    this.dialog = $mdDialog;
    this.prettifyDate = prettifyDate;
    this.postProcessHtml = postProcessHtml;
    this.itemType = itemType;
    this.content = content;
    this.checkExistence = this.checkExistence.bind(this);
    this.unsubscribe = $ngRedux.connect(this.mapState, actions)(this);
    this.init();
  }

  init () {
    this.userProfile = window.$nuxt.$store.getters['user/getProfile'];
    this.editMode = false;
    this.newComment = {
      valid: true,
      text: null
    };
    this.watchers();
  }

  mapState (state) {
    return {
      global: getters.getCmsData(state)
    };
  }

  watchers () {
    this.scope.$watchCollection(s => s.vm.global, this.checkExistence);
  }

  checkExistence (data) {
    if (data && data instanceof Array) {
      const contentExist = data.find(item => {
        return item.id === this.content.id;
      });
      if (contentExist) {
        this.content = contentExist;
      } else {
        this.dialog.cancel();
      }
    }
  }

  scrollToAddNewComment () {
    window.document.querySelector('#add-new-comment').scrollIntoView();
  }

  cancel () {
    this.dialog.cancel();
  }

  edit () {
    this.editMode = !this.editMode;
    if (this.editMode) {
      this.modified = Object.assign({}, this.content);
    }
  }

  async update () {
    await this.saveOrUpdateContent(this.modified);
    this.editMode = false;
  }

  isAuthor () {
    return this.userProfile.id === this.content.author;
  }

  async addComment () {
    await this.addNewComment(this.newComment, this.content);
    this.newComment.text = false;
  }

  static factory (content) {
    function detailElement ($scope, $mdDialog, $ngRedux) {
      return new DetailElementDialog($scope, $mdDialog, $ngRedux, content);
    }

    detailElement.$inject = ['$scope', '$mdDialog', '$ngRedux'];
    return detailElement;
  }
}

class DetailElementController {
  constructor ($mdDialog) {
    this.dialog = $mdDialog;
  }

  scrollToAddNewComment (scrollToComment) {
    if (scrollToComment) {
      window.document.querySelector('#add-new-comment').scrollIntoView();
      document.documentElement.scrollTop = 0;
    }
  }

  showDetailDialog (event, scrollToComment) {
    const self = this;
    self.scrollTop = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop);
    document.documentElement.scrollTop = 0;
    this.dialog.show({
      controller: DetailElementDialog.factory(self.item),
      controllerAs: 'vm',
      template: require('./DetailElementDialog.html'),
      parent: angular.element(document.body),
      targetEvent: event,
      clickOutsideToClose: true,
      onComplete: () => self.scrollToAddNewComment(scrollToComment)
    }).finally(() => {
      document.documentElement.scrollTop = self.scrollTop;
    });
  }

  static factory () {
    require('./DetailElement.scss');

    function detailElement ($mdDialog) {
      return new DetailElementController($mdDialog);
    }

    detailElement.$inject = ['$mdDialog'];
    return detailElement;
  }
}

export default DetailElementController;
export { DetailElementDialog };
