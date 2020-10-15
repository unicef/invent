export const objectToQueryString = (queryParameters) => {
  return queryParameters
    ? `?${Object.entries(queryParameters).reduce(
        (queryString, [key, val], index) => {
          // const symbol = queryString.length === 0 ? '?' : '&'
          const symbol = '&'
          queryString +=
            typeof val === 'object'
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
