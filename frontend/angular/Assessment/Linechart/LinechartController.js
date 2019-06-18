import cloneDeep from 'lodash/cloneDeep';
import forOwn from 'lodash/forOwn';
import isEqual from 'lodash/isEqual';
import d3 from 'd3';

class LinechartController {
  constructor ($scope, $element, $timeout, $ngRedux, gettextCatalog) {
    this.scope = $scope;
    this.EE = window.EE;
    this.$ngRedux = $ngRedux;
    this.el = $element;
    this.timeout = $timeout;
    this.gettextCatalog = gettextCatalog;
    this.$onInit = this.onInit.bind(this);
    this.$onDestroy = this.onDestroy.bind(this);
    this.draw = this.draw.bind(this);
    this.watchers = this.watchers.bind(this);
    this.processDataForDomainChart = this.processDataForDomainChart.bind(this);
    this.processDataForAxisChart = this.processDataForAxisChart.bind(this);
    this.processDataForCoverageChart = this.processDataForCoverageChart.bind(this);
    this.monitorGraphData = this.monitorGraphData.bind(this);
  }

  onInit () {
    this.resizeCount = 0;
    this.dataBit = 0;
    if (this.datachooser) {
      const domainData = window.$nuxt.$store.getters['projects/getMapsDomainData'];
      this.chartConfig = this.processDataForDomainChart(domainData);
    } else if (this.notpercentage) {
      const coverageData = window.$nuxt.$store.getters['projects/getCoverageData'];
      this.chartConfig = this.processDataForCoverageChart(coverageData);
    } else {
      const axisData = window.$nuxt.$store.getters['projects/getMapsAxisData'];
      this.chartConfig = this.processDataForAxisChart(axisData);
    }

    this.watchers();
    window.$nuxt.$root.$on('angularjs:dashResized', this.resizeTick.bind(this));
  }

  onDestroy () {
    window.$nuxt.$root.$off('angularjs:dashResized');
  }

  processDataForDomainChart (data) {
    const result = {};
    const activeAxis = data.labels[0];
    result.data = data;
    result.labels = data.labels;
    result.activeAxis = activeAxis;
    result.chosenData = data[activeAxis].data;
    result.chosenLabels = data[activeAxis].labels;
    return result;
  }

  processDataForAxisChart (data) {
    const result = {};
    result.data = data.data;
    result.labels = data.labels;
    result.chosenLabels = data.labels;
    return result;
  }

  processDataForCoverageChart (data) {
    const gettextCatalog = this.gettextCatalog;
    const labels = [gettextCatalog.getString('Clients'),
      gettextCatalog.getString('Health Workers'),
      gettextCatalog.getString('Facilities')];
    const result = {};
    result.data = data.data;
    result.maxValue = this.calculateMaxData(data);
    result.labels = labels;
    result.chosenLabels = labels;
    return result;
  }

  watchers () {
    this.scope.$watch(s => s.vm.chartConfig, this.monitorGraphData, true);
    this.scope.$watchGroup([s => s.vm.dataBit, s => s.vm.resizeCount], () => {
      const config = cloneDeep(this.chartConfig);
      this.draw(config);
    });
  }

  monitorGraphData (config, old) {
    const isSameData = isEqual(config.data, old.data);
    if (isSameData && this.dataBit === 0) {
      this.dataBit += 1;
    } else if (!isSameData) {
      this.dataBit += 1;
    }
  }

  calculateMaxData (data) {
    return data.data.reduce((ret, version) => {
      forOwn(version, (val, key) => {
        if (key !== 'date' || key !== 'x') {
          ret = val > ret ? val : ret;
        }
      });
      return ret;
    }, 0);
  }

  resizeTick () {
    this.resizeCount += 1;
  }

  draw ({ data, chosenData, chosenLabels, labels, maxValue }) {
    d3.select(this.el[0]).select('.linechartcontainer').remove();
    data = this.datachooser && chosenData ? chosenData : data;
    labels = this.datachooser && chosenLabels ? chosenLabels : labels;

    const outer = d3.select(this.el[0])
      .append('div')
      .attr('class', 'linechartcontainer')
      .classed('secondary-colors', this.notpercentage);

    const outerWidth = outer[0][0].offsetWidth;
    const outerHeight = outer[0][0].offsetHeight;

    // Decorate data with indices
    data.forEach((el, i) => {
      el.x = i + 1;
    });

    // Should recalculate on first open || resize
    const margin = {
      top: 0,
      right: 0,
      bottom: 40,
      left: 45
    };
    const width = outerWidth - margin.left - margin.right;
    const height = outerHeight - margin.top - margin.bottom;

    const element = outer
      .append('svg')
      .attr('class', 'visualization');

    element
      .attr('width', outerWidth)
      .attr('height', outerHeight);

    let tooltip;
    if (!d3.select('.chart-tooltip')[0][0]) {
      tooltip = d3.select('body')
        .append('div')
        .attr('class', 'chart-tooltip');
    } else {
      tooltip = d3.select('.chart-tooltip');
    }

    const xScale = d3.scale.linear()
      .range([margin.left, width - margin.right]) // the area
      .domain([0.8, (this.showdotted ? data.length : data.length - 1) + 0.2]); // min and max values

    const percScale = d3.scale.linear()
      .range([height - margin.top, margin.bottom])
      .domain([0, 1]);

    const simpleScale = d3.scale.linear()
      .range([height - margin.top, margin.bottom])
      .domain([0, maxValue]);

    const yScale = this.notpercentage ? simpleScale : percScale;

    const xAxis = d3.svg.axis()
      .scale(xScale)
      .ticks(this.showdotted ? data.length : (data.length - 1))
      .tickFormat(d => {
        const canShowDate = (width - margin.left - margin.right) / ((data.length - 1) * 80) >= 1.2;
        return canShowDate ? d + '. ' + data[d - 1].date : d;
      })
      .orient('bottom');

    const yAxis = d3.svg.axis()
      .scale(yScale)
      .orient('left')
      .tickFormat(this.notpercentage ? d3.format('d') : d3.format('.0%'));

    // Appending the X axis
    element.append('svg:g')
      .attr('class', 'axis x-axis')
      .attr('transform', 'translate(0,' + (height - margin.bottom) + ')')
      .call(xAxis);

    // Appending the Y axis
    element.append('svg:g')
      .attr('class', 'axis y-axis')
      .attr('transform', 'translate(' + (margin.left) + ',0)')
      .call(yAxis);

    // Appending horizontal ruler lines
    for (let i = 0; i <= 10; i += 1) {
      element.append('svg:line')
        .attr('class', 'linechart-ruler')
        .attr('x1', margin.left)
        .attr('y1', percScale(i / 10))
        .attr('x2', width - margin.right)
        .attr('y2', percScale(i / 10));
    }

    // LINES
    for (let i = 1; i <= labels.length; i += 1) {
      const line = d3.svg.line()
        .x(d => xScale(d.x))
        .y(d => yScale(d['axis' + i] || 0));

      // Full lines
      element.append('svg:path')
        .attr('class', 'line-axis line-axis' + i)
        .attr('d', line(data.slice(0, -1)));

      // Dashed lines
      if (this.showdotted) {
        element.append('svg:path')
          .attr('class', 'line-axis line-axis-dashed line-axis' + i)
          .attr('d', line(data.slice(-2)));
      }
    }

    // DOTS
    const dotData = this.showdotted ? data : data.slice(0, -1);

    dotData.forEach(el => {
      for (let i = 1; i <= labels.length; i += 1) {
        element.append('circle')
          .attr('class', 'dot-axis dot-axis' + i)
          .attr('r', 5)
          .attr('cx', xScale(el.x))
          .attr('cy', yScale(el['axis' + i] || 0))
          .on('mouseover', () => {
            const divString = [
              'Score: ' + Math.round(el['axis' + i] * 100) + '%',
              '<br>',
              'Date: ' + el.date
            ];
            divString[0] = this.notpercentage ? el['axis' + i] : divString[0];

            tooltip.html(divString.join(''))
              .style('top', (d3.event.pageY - 15 + 'px'))
              .style('left', (d3.event.pageX + 15 + 'px'))
              .style('opacity', 1);
          })
          .on('mouseout', () => {
            tooltip.style('opacity', 0);
          });
      }
    });
    function labelHoverFn () {
      for (let i = 1; i <= labels.length; i += 1) {
        d3.select(this.el[0]).select('.labelhov' + i)
          .on('mouseover', () => {
            element.classed('activelabel' + i, true);
          })
          .on('mouseout', () => {
            element.classed('activelabel' + i, false);
          });
      }
    }

    // Label events to trigger classes, that opaques lines via css
    // timeout is sometimes needed, because the labels arent in the DOM yet after redraw
    if (d3.select(this.el[0]).select('.labelhov' + labels.length).empty()) {
      this.timeout(labelHoverFn.bind(this), 250);
    } else {
      labelHoverFn.bind(this)();
    }

    // Redraw on window size change
  }

  // Ng-options change
  axisChange (newAxis) {
    this.chartConfig.chosenData = this.chartConfig.data[newAxis].data;
    this.chartConfig.chosenLabels = this.chartConfig.data[newAxis].labels;
    this.draw(this.chartConfig);
  }

  static linechartFactory () {
    require('./Linechart.scss');
    require('d3');

    function linechart ($scope, $element, $timeout, $ngRedux, gettextCatalog) {
      return new LinechartController($scope, $element, $timeout, $ngRedux, gettextCatalog);
    }

    linechart.$inject = ['$scope', '$element', '$timeout', '$ngRedux', 'gettextCatalog'];

    return linechart;
  }
}

export default LinechartController;
