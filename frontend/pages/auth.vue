<template>
  <div>
    <div class="AuthComponent">
      <div>
        <el-button type="primary" size="large" @click="loginStart">
          <translate> Login </translate>
        </el-button>
        <p>
          <translate> You must have a UNICEF account to log in. </translate>
        </p>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
    }),
  },
  async mounted() {
    // eslint-disable-next-line
    if (!process.server) {
      const storedNext = localStorage.getItem('next')
      const next = this.$route.query.next
      localStorage.removeItem('next')
      if (next && next !== '/') {
        localStorage.setItem('next', next)
      }
      if (window.location.hash) {
        const codeMatch = window.location.hash.match(/#code=(.*)&session/)
        window.history.replaceState(null, null, ' ')
        if (codeMatch.length > 1) {
          const code = codeMatch[1]
          this.$nextTick(() => {
            this.$nuxt.$loading.start('loginLoader')
          })
          try {
            await this.login({ code })
          } catch (e) {
            this.$nuxt.$loading.finish('loginLoader')
            return
          }
          try {
            if (this.profile.country) {
              this.setSelectedCountry(this.profile.country)
            }
            if (storedNext) {
              this.$router.push(storedNext)
            } else {
              // this.$router.push(this.localePath({ name: 'organisation-dashboard-list', params: { organisation: '-' } }));
              this.$router.push(
                this.localePath({ name: '', params: { organisation: '-' } })
              )
            }
          } catch (e) {
            console.error(e)
          }
          this.$nuxt.$loading.finish('loginLoader')
        }
      }
    }
  },
  methods: {
    ...mapActions({
      login: 'user/doLogin',
      setSelectedCountry: 'dashboard/setSelectedCountry',
    }),
    loginStart() {
      window.location.href = process.env.loginUrl
    },
  },
}
</script>

<style lang="less">
@import '../assets/style/variables.less';
@import '../assets/style/mixins.less';

.AuthComponent {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  /*<!--width: @cardSizeSmall;-->*/
  min-height: calc(100vh - @topBarHeight - @appFooterHeight - 160px);
  margin: 80px auto;
  p {
    margin-top: 20px;
    max-width: 300px;
    color: @colorGray;
  }
}
</style>
