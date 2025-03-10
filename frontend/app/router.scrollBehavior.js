export default function (to, from, savedPosition) {
  if (savedPosition) {
    return savedPosition
  } else {
    let position = { x: 0, y: 0 }

    // If there's a hash but it starts with '#code=...', skip the anchor scroll.
    if (to.hash && !to.hash.startsWith('#code=')) {
      position = { selector: to.hash }
    }
    return position
  }
}
