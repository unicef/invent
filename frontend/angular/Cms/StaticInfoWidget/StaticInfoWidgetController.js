class StaticInfoWidgetController {
  static factory () {
    require('./StaticInfoWidget.scss');
    function staticInfoWidgetController () {
      return new StaticInfoWidgetController();
    }
    staticInfoWidgetController.$inject = [];
    return staticInfoWidgetController;
  }
}

export default StaticInfoWidgetController;
