<template>
  <div>
    <div class="AuthComponent">
      <div>
        <el-button type="primary" size="large" @click="loginStart" :disabled="disabled" >
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
  data: function() {
return {
  disabled: false
}
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
            this.disabled = true
          })
          try {
            await this.login({ code })
      
            if (this.profile.country) {
            await  this.setSelectedCountry(this.profile.country)
            }
            if (storedNext) {
              this.$router.push(storedNext)
            } else {
              
              // this.$router.push(this.localePath({ name: 'organisation-dashboard-list', params: { organisation: '-' } }));
              this.$router.push(this.localePath({ name: 'organisation', params: { organisation: '-' } }))
            }
          } catch (e) {
            console.error(e)
          } finally {
            this.$nuxt.$loading.finish('loginLoader')
            this.disabled = false
          }
        }
      } else if ( this.user && this.$route.name.split('___')[0] === 'auth' ) {
        
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
