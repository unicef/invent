import langReq from './langReq'
export default () => {
  return new Promise(function (resolve) {
    langReq('fr').then((res) => {
      resolve(res.data.catalog)
    })
  })
}
