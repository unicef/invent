export const objectToQueryString = (queryParameters) => {
  return queryParameters
    ? `?${Object.entries(queryParameters).reduce(
        (queryString, [key, val], index) => {
          // const symbol = queryString.length === 0 ? '?' : '&'
          const symbol = '&'
          queryString +=
            typeof val === 'object' &&
            !(val === '' || val === null || val === undefined)
              ? val.map((value) => `${symbol}${key}=${value}`).join('')
              : !(val === '' || val === null || val === undefined)
              ? `${symbol}${key}=${val}`
              : ''
          return queryString
        },
        ''
      )}`
    : ''
}

export const queryStringToObject = (url) => {
  const obj = [...new URLSearchParams(url.split('?')[1])].reduce(
    (a, [k, v]) => {
      if (a[k]) {
        return (a[k] = typeof a[k] === 'object' ? [...a[k], v] : [a[k], v]), a
      }
      return (a[k] = v), a
    },
    {}
  )
  return obj
}
