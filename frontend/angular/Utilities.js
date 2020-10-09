export const getSubDomain = () => {
  const defaultDomain = 'who'
  const hostArray = window.location.hostname.split('.')
  const subDomain = hostArray.length > 1 ? hostArray.shift() : defaultDomain
  if (subDomain !== defaultDomain && subDomain.length !== 2) {
    return defaultDomain
  }
  return subDomain
}

export const calculateHeight = () => {
  const contentHeight = window.innerHeight - 48
  return contentHeight + 'px'
}

export const fixUrl = (url) => {
  if (!/^(?:f|ht)tps?:\/\//.test(url)) {
    url = 'http://' + url
  }
  return url
}
