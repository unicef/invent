
class TrixComponentController {
  constructor ($scope, $element) {
    this.scope = $scope;
    this.element = $element;
    this.$onInit = this.onInit.bind(this);
    this.$postLink = this.postLink.bind(this);
    this.updateValue = this.updateValue.bind(this);
  }

  onInit () {
    require('./TrixComponent.scss');
    require('trix');
    this.charCounter = 0;
    this.valid = false;
    this.showError = false;
    this.watchers();
    this.required = this.element[0].hasAttribute('required');
  }

  watchers () {
    this.scope.$watch(() => {
      return this.value;
    }, value => {
      if (value === false) {
        this.editorInstance.editor.loadHTML('');
      }
    });
  }

  postLink () {
    const self = this;
    this.editorInstance = this.element[0].querySelector('trix-editor');
    this.editorInstance.setAttribute('placeholder', this.placeholder);
    this.editorInstance.addEventListener('trix-change', this.updateValue);
    this.editorInstance.addEventListener('trix-initialize', () => {
      self.editorInstance.editor.loadHTML(self.value);
    });
  }

  blur () {
    this.showError = !this.valid;
  }

  updateValue () {
    const rawString = this.editorInstance.editor.getDocument().toString();
    this.scope.$evalAsync(() => {
      this.charCounter = rawString.length - 1;
      this.valid = this.charLimit ? this.charCounter < this.charLimit : true;
      this.valid = this.valid && this.charCounter > 0;
      this.value = this.editorInstance.editor.element.value;
    });
  }

  static factory () {
    function controller ($scope, $element) {
      return new TrixComponentController($scope, $element);
    }

    controller.$inject = ['$scope', '$element'];

    return controller;
  }
}

export default TrixComponentController;
