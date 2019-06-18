import { prettifyDate, postProcessHtml } from '../utilities';
import { getters, actions } from '../../store/modules/cms';

class CommentWidgetController {
  constructor ($scope, $ngRedux) {
    this.scope = $scope;
    this.prettifyDate = prettifyDate;
    this.postProcessHtml = postProcessHtml;
    this.$onInit = this.onInit.bind(this);
    this.$onDestroy = this.onDestroy.bind(this);
    this.unsubscribe = $ngRedux.connect(this.mapState, actions)(this);
  }
  onInit () {
    this.expanded = false;
    this.editMode = false;
    this.userProfile = window.$nuxt.$store.getters['user/getProfile'];
    this.profiles = window.$nuxt.$store.getters['system/getUserProfiles'];
  }

  onDestroy () {
    this.unsubscribe();
  }

  mapState (state) {
    return {
      global: getters.getCmsData(state)
    };
  }

  isAuthor () {
    return this.userProfile.id === this.comment.user;
  }

  getUsername () {
    const user = this.profiles.find(p => p.id === this.comment.user);
    return user ? user.name : 'No name';
  }

  edit () {
    this.editMode = !this.editMode;
    if (this.editMode) {
      this.modified = Object.assign({}, this.comment);
    }
  }

  async update () {
    await this.updateComment(this.modified);
    this.editMode = false;
  }

  readMore () {
    this.expanded = !this.expanded;
  }

  static factory () {
    require('./CommentWidget.scss');
    function commentWidget ($scope, $ngRedux) {
      return new CommentWidgetController($scope, $ngRedux);
    }
    commentWidget.$inject = ['$scope', '$ngRedux'];
    return commentWidget;
  }
}

export default CommentWidgetController;
