export const phaseInfo = (type) => {
  let info = {}
  switch (type) {
    case 'Ended':
      info = {
        color: '#D86422',
        rotation: 180,
        dash: [],
        point: 'triangle',
      }
      break
    case 'Start':
      info = {
        color: '#76BF41',
        rotation: 90,
        dash: [10, 5],
        point: 'triangle',
      }
      break
    default:
      // color = '#E0E0E0';
      info = {
        color: '#008DC9',
        rotation: 0,
        dash: [],
        point: 'circle',
      }
      break
  }
  return info
}

export const lastLabelType = (arr) => arr[arr.length - 1][1]

export const fillArr = (len, fill) => new Array(len).fill(fill)

export const axisYColors = (phases, labels, data) => {
  const axisColors = fillArr(phases.length, '#E0E0E0')
  axisColors[data[data.length - 1]] = phaseInfo(lastLabelType(labels)).color
  return axisColors.reverse()
}

export const dataInfoFill = (len, fill, change = undefined, type = 'front') => {
  const arrFill = fillArr(len, fill)

  if (change) {
    if (type === 'front') {
      arrFill[0] = change
      return arrFill
    }
    arrFill[arrFill.length - 1] = change
    return arrFill
  }
  return arrFill
}
