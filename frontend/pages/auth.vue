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
      user: 'user/getProfile',
      profile: 'user/getProfile',
    }),
  },
  async mounted() {
    // eslint-disable-next-line
    if (!process.server) {
      const storedNext = localStorage.getItem('next')
      const next = this.$route.query.next
      console.log('route next ' + next + 'stored next ' + storedNext)
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
            console.log('Login sucesfull!')
            if (this.profile.country) {
              await this.setSelectedCountry(this.profile.country)
            }
            if (storedNext) {
              this.$router.push(storedNext)
            } else {
              console.log('hash and no next route, redirect to homepage')
              // this.$router.push(this.localePath({ name: 'organisation-dashboard-list', params: { organisation: '-' } }));
              this.$router.push(this.localePath({ name: 'organisation', params: { organisation: '-' } }))
            }
          } catch (e) {
            console.error(e)
          } finally {
            this.$nuxt.$loading.finish('loginLoader')
          }
        }
      } else if ( this.user && this.$route.name.split('___')[0] === 'auth' ) {
        console.log('User set and auth route, redirect to homepage')
        this.$router.push(this.localePath({ name: 'organisation', params: { organisation: '-' } }))
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
    goToHomepage() {
      this.$router.push(
            this.localePath({
              name: 'index',
              params: this.$route.params,
            })
          )
    }
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
    max-width: 400px;
    color: @colorGray;
  }
}
</style>
