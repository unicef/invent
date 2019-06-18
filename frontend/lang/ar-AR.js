import langReq from './langReq';
export default () => {
  return new Promise(function (resolve) {
    langReq('ar').then(res => {
      resolve(res.data.catalog);
    });
  });
};
