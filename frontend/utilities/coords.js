import polylabel from '@mapbox/polylabel'

export const circleOfCoords = ({ lat, lng }, amount) => {
  const radius = 1000 // meters
  const result = []
  for (let i = 0; i < amount; i++) {
    const angle = (Math.PI * 2 * i) / amount
    const dx = radius * Math.cos(angle)
    const dy = radius * Math.sin(angle)
    const latlng = {}
    latlng.lat = lat + (180 / Math.PI) * (dy / 6378137)
    latlng.lng =
      lng + ((180 / Math.PI) * (dx / 6378137)) / Math.cos((lat * Math.PI) / 180)
    result.push(latlng)
  }
  return result
}
export const calculatePolyCenter = (geometry) => {
  try {
    let coordinates = [...geometry.coordinates]
    if (geometry.type !== 'Polygon') {
      coordinates = coordinates.sort((a, b) => b[0].length - a[0].length)[0]
    }
    const r = polylabel(coordinates)
    return { lat: r[1], lng: r[0] }
  } catch (e) {
    console.warn('error in polycenter calculation', e)
  }
}
