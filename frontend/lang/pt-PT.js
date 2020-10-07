import langReq from './langReq'
export default () => {
  return new Promise(function (resolve) {
    langReq('pt').then((res) => {
      resolve(res.data.catalog)
    })
  })
}
