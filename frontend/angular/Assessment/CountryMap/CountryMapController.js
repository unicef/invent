import keys from 'lodash/keys'
import reduce from 'lodash/reduce'
import forOwn from 'lodash/forOwn'

// eslint-disable-next-line
import * as topojson from 'topojson'
import svgPanZoom from 'svg-pan-zoom'
import d3 from 'd3'

class CountryMapController {
  constructor($element, $scope, $state, $mdDialog, gettextCatalog) {
    this.el = $element
    this.scope = $scope
    this.state = $state
    this.$mdDialog = $mdDialog
    this.EE = window.EE
    this.tooltipOver = false
    this.preventMouseOut = false
    this.checkIfDistrictDataChanged = this.checkIfDistrictDataChanged.bind(this)
    this.createInMemoryDOMElement = this.createInMemoryDOMElement.bind(this)
    this.drawMapShape = this.drawMapShape.bind(this)
    this.$onInit = this.onInit
    this.$onDestroy = this.onDestroy
    this.createDialogs = this.createDialogs.bind(this, gettextCatalog)
    this.showErrorDialog = this.showErrorDialog.bind(this)
  }

  onInit() {
    this.showPlaceholder = !this.big
    this.svgPanZoom = svgPanZoom
    this.covLib = {}
    this.svgLib = {}
    this.drawnMap = null
    this.createInMemoryDOMElement()
    this.watchers()
    this.createDialogs()
    this.showMapErrorDialog = false
    this.drawMapShape(this.mapData)
  }

  createDialogs(gettextCatalog) {
    this.mapError = this.$mdDialog.alert({
      title: gettextCatalog.getString('Attention'),
      textContent: gettextCatalog.getString(
        'The map failed to load or loaded partially'
      ),
      ok: gettextCatalog.getString('Close'),
      theme: 'alert',
    })
  }

  createInMemoryDOMElement() {
    this.elementContainer = d3
      .select(this.el[0])
      .append('div')
      .attr('class', 'countrymapcontainer')

    const width = this.elementContainer[0][0].offsetWidth
    const height = this.big ? d3.select('#map')[0][0].offsetHeight : 409

    const inMemoryElement = document.createElement('div')
    this.mapDOMElement = d3.select(inMemoryElement).append('svg')

    this.mapDOMElement
      .attr('class', 'countrymap')
      .attr('width', width)
      .attr('height', height)
  }

  onDestroy() {
    this.data = false
    this.countryMapData = false
  }

  watchers() {
    this.scope.$watch(
      (s) => s.vm.districtLevelCoverage,
      this.checkIfDistrictDataChanged,
      true
    )
    this.scope.$watch((s) => s.vm.showMapErrorDialog, this.showErrorDialog)
  }

  async showErrorDialog(show) {
    if (show) {
      await this.$mdDialog.show(this.mapError)
      this.showMapErrorDialog = false
    }
  }

  checkIfDistrictDataChanged(newDistrictData) {
    if (newDistrictData) {
      this.boundNrs = reduce(
        newDistrictData,
        (ret, value, key) => {
          if (key === 'date') {
            return ret
          }
          forOwn(value, (val, k) => {
            ret[k] = (ret[k] || 0) + val
          })
          return ret
        },
        {}
      )
      this.fillDistrictData(newDistrictData)
    }
  }

  setGlobal() {
    this.showNationalLevelCoverage = true
    const districts = document.getElementsByClassName('d3district')
    Array.prototype.forEach.call(districts, (distr) => {
      distr.classList.add('global')
    })
  }

  setTotal() {
    this.showNationalLevelCoverage = false
    const districts = document.getElementsByClassName('d3district')
    Array.prototype.forEach.call(districts, (distr) => {
      distr.classList.remove('global')
    })
  }

  makeGeoFromTopo(topo) {
    const subKey = keys(topo.objects)[0]
    // eslint-disable-next-line
    const ret = topojson.feature(topo, topo.objects[subKey])
    return ret
  }

  calculateScale(topoJSON) {
    return (
      Math.max.apply(
        null,
        topoJSON.transform.scale.map((nr) => {
          return 1 / nr
        })
      ) * 10
    )
  }

  makeSvgPannableAndZoomable(element) {
    const zoomOptions = {
      panEnabled: true,
      controlIconsEnabled: false,
      zoomEnabled: true,
      mouseWheelZoomEnabled: false,
      preventMouseEventsDefault: true,
      zoomScaleSensitivity: 0.2,
      minZoom: 0.5,
      maxZoom: 10,
      contain: false,
      center: true,
      refreshRate: 'auto',
    }

    this.svgZoom = this.svgPanZoom(element, zoomOptions)
    this.svgZoom.zoomOut()
  }

  drawMapShape(countryMapData) {
    this.showPlaceholder = true
    const self = this
    if (this.drawnMap) {
      d3.select(this.el[0]).select('.countrymapcontainer').remove()
      this.createInMemoryDOMElement()
    }
    this.countryName = countryMapData.name
    this.flagUrl = countryMapData.flag

    try {
      const geoData = this.makeGeoFromTopo(countryMapData.geoJson)
      const projection = d3.geo
        .mercator()
        .scale(this.calculateScale(countryMapData.geoJson))

      const path = d3.geo.path().projection(projection)
      geoData.features.forEach((feature) => {
        try {
          const mapName =
            feature.properties.id ||
            feature.properties.name ||
            feature.properties['en:name'] ||
            feature.properties['wof:name']
          const districtsName = countryMapData.districts.find(
            (dn) => dn.id === mapName || dn.name === feature.properties.name
          )
          this.svgLib[districtsName.id] = this.mapDOMElement
            .append('path')
            .datum({
              type: geoData.type,
              geocoding: geoData.geocoding,
              features: [feature],
              name: districtsName.name,
            })
            .attr('d', path)
            .classed('d3district', true)
            .classed('global', this.showNationalLevelCoverage)
            .classed(`name-${districtsName.id}`, true)
            .on('click', () => {
              this.scope.$evalAsync(() => {
                this.activeDistrict = {
                  name: districtsName.name,
                  data: self.svgLib[districtsName.id]
                    ? self.svgLib[districtsName.id].districtData
                    : null,
                }
              })
            })
        } catch (e) {
          console.log(feature.properties)
          console.log(countryMapData)
          this.showMapErrorDialog = true
          console.error(e)
        }
      })

      this.elementContainer.append(() => {
        return this.mapDOMElement.node()
      })

      this.makeSvgPannableAndZoomable(this.mapDOMElement.node())
    } catch (e) {
      console.error(e)
      this.showMapErrorDialog = true
    }

    this.showPlaceholder = false
  }

  fillDistrictData(districtLevelCoverage) {
    for (const district in this.svgLib) {
      const node = this.svgLib[district]
      if (districtLevelCoverage[district]) {
        node.classed('d3district-data', true)
        node.districtData = districtLevelCoverage[district]
      } else {
        node.classed('d3district-data', false)
        node.districtData = null
      }
    }
  }

  goToProject(project) {
    this.state.go('editProject', { appName: project.id, editMode: 'publish' })
  }

  static countrymapFactory() {
    require('./Countrymap.scss')

    function countrymap($element, $scope, $state, $mdDialog, gettextCatalog) {
      return new CountryMapController(
        $element,
        $scope,
        $state,
        $mdDialog,
        gettextCatalog
      )
    }

    countrymap.$inject = [
      '$element',
      '$scope',
      '$state',
      '$mdDialog',
      'gettextCatalog',
    ]

    return countrymap
  }
}

export default CountryMapController
