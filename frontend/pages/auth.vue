<template>
  <div>
    <div class="AuthComponent">
      <div>
        <el-button
          type="primary"
          size="large"
          @click="loginStart"
        >
          <translate>
            Login with Azure
          </translate>
        </el-button>
        <p>
          <translate>
            If you don't have an Azure account please contact an administrator.
          </translate>
        </p>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters({
      profile: 'user/getProfile'
    })
  },
  async mounted () {
    if (!process.server && window.location.hash) {
      const codeMatch = window.location.hash.match(/#code=(.*)&session/);
      window.history.replaceState(null, null, ' ');
      if (codeMatch.length > 1) {
        const code = codeMatch[1];
        this.$nextTick(() => {
          this.$nuxt.$loading.start('loginLoader');
        });
        try {
          await this.login({ code });
        } catch (e) {
          this.$nuxt.$loading.finish('loginLoader');
          return;
        }
        try {
          if (this.profile.country) {
            this.setSelectedCountry(this.profile.country);
          }
          if (this.$route.query && this.$route.query.next) {
            const path = this.$route.query.next;
            const query = { ...this.$route.query, next: undefined };
            this.$router.push({ path, query });
          } else {
            // console.log(this.profile);
            // console.log(this.localePath({ name: 'organisation-dashboard-list' }));
            // const path = this.$i18n.locale;
            this.$router.push(this.localePath({ name: 'organisation-dashboard-list', params: { organisation: '-' }, query: { country: [this.profile.country] } }));
          }
        } catch (e) {
          console.error(e);
        }
        this.$nuxt.$loading.finish('loginLoader');
      }
    }
  },
  methods: {
    ...mapActions({
      login: 'user/doLogin',
      setSelectedCountry: 'dashboard/setSelectedCountry'
    }),
    loginStart () {
      window.location.href = process.env.loginUrl;
    }
  }
};
</script>

<style lang="less">
  @import "../assets/style/variables.less";
  @import "../assets/style/mixins.less";

  .AuthComponent {
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    /*<!--width: @cardSizeSmall;-->*/
    min-height: calc(100vh - @topBarHeight - @appFooterHeight - 86px);
    margin: 80px auto;
    p {
      margin-top: 20px;
      max-width: 300px;
      color: @colorGray;
    }
  }
</style>
