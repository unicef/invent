import { loadSkeletonImages, loadSkeletonStatic } from '../webpackRequires'
class SkeletonController {
  constructor($scope, $interpolate, data, axis, domain, icons, $mdDialog) {
    this.scope = $scope
    this.interpolate = $interpolate
    this.axis = axis
    this.domain = domain
    this.data = data
    this.icons = icons
    this.modal = $mdDialog

    this.domainActivationSetter(this.axis, this.domain, true)
    this.images = this.importImages()
    this.templates = this.importHtmlTemplates()

    this.data.forEach((a, aInd) => {
      a.expand = aInd - 2 === this.axis
      return a
    })
  }

  hideDialog() {
    this.modal.hide()
  }

  importImages() {
    const templates = {}
    const templateRequire = loadSkeletonImages()
    templateRequire.keys().forEach((item) => {
      const key = item.split('.')[1].replace('/', '')
      templates[key] = templateRequire(item)
    })
    return templates
  }

  importHtmlTemplates() {
    const scope = {
      vm: {
        images: this.images,
      },
    }
    const templates = {}
    const templateRequire = loadSkeletonStatic()
    templateRequire.keys().forEach((item) => {
      templates[item.slice(2)] = this.interpolate(templateRequire(item))(scope)
    })
    return templates
  }

  axisClick(axis, id) {
    axis.expand = true
    this.changeSpot(id - 2, 0)
  }

  changeSpot(axisId, domainId) {
    domainId = domainId || 0
    this.domainActivationSetter(this.axis, this.domain, false)
    this.axis = axisId
    this.domain = domainId
    this.domainActivationSetter(this.axis, this.domain, true)
    window.document.querySelectorAll('.right-content')[0].scrollTop = 0
  }

  domainActivationSetter(axisId, domainId, state) {
    this.data[axisId + 2].domains[domainId].active = state
  }

  static factory(data, axis, domain, icons, modal) {
    const skeleton = ($scope, $interpolate) => {
      return new SkeletonController(
        $scope,
        $interpolate,
        data,
        axis,
        domain,
        icons,
        modal
      )
    }
    skeleton.$inject = ['$scope', '$interpolate']
    return skeleton
  }
}

export default SkeletonController
