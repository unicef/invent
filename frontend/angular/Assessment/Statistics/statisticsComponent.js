import StatisticsController from './StatisticsController';
import _template from './Statistics.html';
import './Statistics.scss';

export default {
  controller: StatisticsController.factory(),
  template: _template,
  controllerAs: 'vm',
  name: 'statistics'
};
