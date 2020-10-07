import Vue from 'vue'
import {
  LMap,
  LTileLayer,
  LMarker,
  LTooltip,
  LPopup,
  LControlZoom,
  LGeoJson,
  LFeatureGroup,
  LIcon,
} from 'vue2-leaflet'
import { Icon } from 'leaflet'
import CustomMarkerCluster from '@/components/common/map/CustomMarkerCluster'

delete Icon.Default.prototype._getIconUrl

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
})

Vue.component('LMap', LMap)
Vue.component('LTilelayer', LTileLayer)
Vue.component('LMarker', LMarker)
Vue.component('LTooltip', LTooltip)
Vue.component('LPopup', LPopup)
Vue.component('LControlZoom', LControlZoom)
Vue.component('CustomMarkerCluster', CustomMarkerCluster)
Vue.component('LGeoJson', LGeoJson)
Vue.component('LFeatureGroup', LFeatureGroup)
Vue.component('LIcon', LIcon)
