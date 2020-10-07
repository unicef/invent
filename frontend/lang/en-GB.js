import langReq from './langReq'
export default () => {
  return new Promise(function (resolve) {
    langReq('en').then((res) => {
      resolve(res.data.catalog)
    })
  })
}
