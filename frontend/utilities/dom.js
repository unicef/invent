export const downloadLinkManager = (data, name) => {
  let link = document.createElement('a');
  link.setAttribute('href', data);
  link.setAttribute('download', name);
  link.click();
  link = null;
};

export const blobDownloader = (data, name, callback) => {
  if (window && window.navigator && window.navigator.msSaveBlob) {
    const blobDownload = new Blob([data]);
    window.navigator.msSaveBlob(blobDownload, name);
  } else {
    const download_url = window.URL.createObjectURL(data);
    downloadLinkManager(download_url, name);
  }
  if (callback) {
    callback();
  }
};

export const uriDownloader = (data, name) => {
  const download_url = encodeURI(data);
  downloadLinkManager(download_url, name);
};

export const uuidv4 = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};
