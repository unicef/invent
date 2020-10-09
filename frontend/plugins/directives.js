import Vue from 'vue'

let handleOutsideClick

Vue.directive('outside', {
  bind(el, binding, vnode) {
    handleOutsideClick = (e) => {
      e.stopPropagation()
      const { handler, exclude } = binding.value

      let clickedOnExcludedEl = false
      exclude.forEach((refName) => {
        if (!clickedOnExcludedEl) {
          const excludedEl = vnode.context.$refs[refName]
          clickedOnExcludedEl = excludedEl.contains(e.target)
        }
      })

      if (!el.contains(e.target) && !clickedOnExcludedEl) {
        vnode.context[handler]()
      }
    }

    document.addEventListener('click', handleOutsideClick)
    document.addEventListener('touchstart', handleOutsideClick)
  },

  unbind() {
    document.removeEventListener('click', handleOutsideClick)
    document.removeEventListener('touchstart', handleOutsideClick)
  },
})

let handlePaste

Vue.directive('paste', {
  bind(el, binding, vnode) {
    handlePaste = (e) => {
      e.stopPropagation()

      const { handler } = binding.value
      const paste = (e.clipboardData || window.clipboardData).getData('text')

      if (el.contains(e.target)) {
        vnode.context[handler](paste, e)
      }
    }

    document.addEventListener('paste', handlePaste)
  },

  unbind() {
    document.removeEventListener('paste', handlePaste)
  },
})
