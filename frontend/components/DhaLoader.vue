<template>
  <transition name="el-fade-in">
    <div v-if="show" class="GlobalLoader">
      <div>
        <div class="Loader">
          <div />
          <span><translate>Loading</translate></span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
      percent: 0,
      show: false,
      canSuccess: true,
      throttle: 200,
      duration: 3000,
      reversed: false,
      skipTimerCount: 0,
      continuous: false,
      rtl: false,
    }
  },
  beforeDestroy() {
    this.clear()
  },
  methods: {
    clear() {
      clearInterval(this._timer)
      clearTimeout(this._throttle)
      this._timer = null
    },
    start(id) {
      if (id) {
        this._skipUntill = id
      }
      this.clear()
      this.percent = 0
      this.reversed = false
      this.skipTimerCount = 0
      this.canSucceed = true
      if (this.throttle) {
        this._throttle = setTimeout(() => this.startTimer(), this.throttle)
      } else {
        this.startTimer()
      }
      return this
    },
    set(num) {
      this.show = true
      this.canSucceed = true
      this.percent = Math.min(100, Math.max(0, Math.floor(num)))
      return this
    },
    get() {
      return this.percent
    },
    increase(num) {
      this.percent = Math.min(100, Math.floor(this.percent + num))
      return this
    },
    decrease(num) {
      this.percent = Math.max(0, Math.floor(this.percent - num))
      return this
    },
    pause() {
      clearInterval(this._timer)
      return this
    },
    resume() {
      this.startTimer()
      return this
    },
    finish(id) {
      if (this._skipUntill && id !== this._skipUntill) {
        return this
      }
      this.percent = this.reversed ? 0 : 100
      this._skipUntill = null
      this.hide()
      return this
    },
    hide() {
      this.clear()
      setTimeout(() => {
        this.show = false
        this.$nextTick(() => {
          this.percent = 0
          this.reversed = false
        })
      }, 500)
      return this
    },
    fail() {
      this.canSucceed = false
      return this
    },
    startTimer() {
      if (!this.show) {
        this.show = true
      }
      if (typeof this._cut === 'undefined') {
        this._cut = 10000 / Math.floor(this.duration)
      }
      this._timer = setInterval(() => {
        if (this.skipTimerCount > 0) {
          this.skipTimerCount--
          return
        }
        if (this.reversed) {
          this.decrease(this._cut)
        } else {
          this.increase(this._cut)
        }
        if (this.continuous) {
          if (this.percent >= 100) {
            this.skipTimerCount = 1
            this.reversed = !this.reversed
          } else if (this.percent <= 0) {
            this.skipTimerCount = 1
            this.reversed = !this.reversed
          }
        }
      }, 100)
    },
  },
}
</script>

<style lang="less">
.GlobalLoader {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 5000;
  background-color: rgba(255, 255, 255, 0.5);

  > div {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 5px;
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.12);
  }

  p {
    color: white;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 24px;
  }
}
</style>
