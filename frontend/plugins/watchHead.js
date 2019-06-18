// workaround for this problem: https://github.com/pulilab/who-maps/issues/1141
// idea from: https://github.com/ElemeFE/element/issues/4207#issuecomment-462612793

export default function watchTitle () {
  let isRefreshing = false;

  const observer = new MutationObserver(function (mutations) {
    const newValue = mutations[0].target.nodeValue;
    if (newValue || isRefreshing) {
      isRefreshing = false;
      return;
    }
    isRefreshing = true;
    $nuxt.$meta().refresh();
  });

  const target = document.querySelector('head > title');
  const config = { subtree: true, characterData: true, childList: true };
  observer.observe(target, config);
}
