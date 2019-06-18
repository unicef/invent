<template>
  <div class="LoginComponent">
    <el-card
      v-if="!showForgotten && !successfulReset"
      key="loginCard"
      :body-style="{ padding: '0px' }"
    >
      <div slot="header">
        <translate>Log in to Digital Health Atlas</translate>
      </div>

      <el-form
        ref="loginForm"
        :rules="rules"
        :model="{ username, password }"
        label-position="top"
        status-icon
        @submit.native.prevent="loginLocal"
      >
        <fieldset>
          <el-form-item
            :label="$gettext('E-mail') | translate"
            prop="username"
          >
            <el-input
              v-model="username"
              type="text"
            />
          </el-form-item>

          <el-form-item
            :label="$gettext('Password') | translate"
            prop="password"
          >
            <el-input
              v-model="password"
              type="password"
            />
            <div
              v-if="nonFieldErrors"
              class="el-form-item__error ModifiedFormError"
            >
              {{ nonFieldErrors }}
            </div>
          </el-form-item>
        </fieldset>

        <div class="CardActionsBottom">
          <el-row
            type="flex"
            justify="space-between"
            align="middle"
            class="cardActions"
          >
            <el-col
              :span="6"
              class="SecondaryAction"
            >
              <nuxt-link
                :to="localePath({name: 'organisation-signup', params: $route.params})"
                type="text"
                class="NuxtLink Small"
              >
                <translate>Signup</translate>
              </nuxt-link>
              <div class="Separator" />
              <el-button
                type="text"
                size="small"
                class="CancelButton"
                @click="toForgotten"
              >
                <translate>Forgot password?</translate>
              </el-button>
            </el-col>
            <el-col
              :span="6"
              class="PrimaryAction"
            >
              <el-button
                type="primary"
                size="medium"
                native-type="submit"
              >
                <translate>Log in</translate>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <el-card
      v-if="showForgotten"
      key="forgottenCard"
      :body-style="{ padding: '0px' }"
    >
      <div slot="header">
        <translate>Reset forgotten password</translate>
      </div>

      <p class="Instruction">
        <translate>Enter your email address and follow the instructions you will get by email.</translate>
      </p>

      <el-form
        ref="forgotForm"
        :rules="forgettenPasswordRules"
        :model="{ email }"
        label-position="top"
        status-icon
        @submit.native.prevent="forgotEmail"
      >
        <fieldset>
          <el-form-item
            :label="$gettext('E-mail') | translate"
            prop="email"
          >
            <el-input
              v-model="email"
              type="text"
            />
          </el-form-item>
        </fieldset>

        <div class="CardActionsBottom">
          <el-row
            type="flex"
            justify="space-between"
            align="middle"
            class="cardActions"
          >
            <el-col
              :span="6"
              class="SecondaryAction"
            >
              <el-button
                type="text"
                size="small"
                @click="showForgotten = false"
              >
                <translate>Go back to login</translate>
              </el-button>
            </el-col>
            <el-col
              :span="6"
              class="PrimaryAction"
            >
              <el-button
                type="primary"
                size="medium"
                native-type="submit"
              >
                <translate>Reset</translate>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <el-card
      v-if="successfulReset"
      key="resetCard"
      :body-style="{ padding: '0px' }"
      class="Success"
    >
      <div slot="header">
        <translate>Congratulations!</translate>
      </div>

      <p class="Instruction">
        <translate>An email with instructions to reset your password have been sent.</translate>
      </p>

      <div class="CardActionsBottom">
        <el-row
          type="flex"
          justify="space-between"
          align="middle"
          class="cardActions"
        >
          <el-col
            :span="6"
            class="SecondaryAction"
          />
          <el-col
            :span="6"
            class="PrimaryAction"
          >
            <el-button
              type="primary"
              size="medium"
              @click="successfulReset = false"
            >
              <translate>Go back to login</translate>
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import FormAPIErrorsMixin from './mixins/FormAPIErrorsMixin.js';

export default {
  mixins: [FormAPIErrorsMixin],

  data () {
    return {
      username: '',
      password: '',
      email: '',
      showForgotten: false,
      successfulReset: false,
      rules: {
        username: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { type: 'email', message: this.$gettext('Has to be a valid email address'), trigger: 'blur' },
          { validator: this.validatorGenerator('username') }
        ],
        password: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { validator: this.validatorGenerator('password') }
        ]
      },
      forgettenPasswordRules: {
        email: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { type: 'email', message: this.$gettext('Has to be a valid email address'), trigger: 'blur' },
          { validator: this.validatorGenerator('email') }
        ]
      }
    };
  },
  computed: {
    ...mapGetters({
      profile: 'user/getProfile'
    })
  },
  methods: {
    ...mapActions({
      login: 'user/doLogin',
      resetPassword: 'user/resetPassword',
      setSelectedCountry: 'dashboard/setSelectedCountry'
    }),
    handleRoutingErrors (e) {
      this.$alert(
        this.$gettext('An error occured during login, please reload the page and try again'),
        this.$gettext('Warning'),
        {
          confirmButtonText: this.$gettext('OK')
        }
      );
      if (this.$sentry) {
        this.$sentry.captureMessage('Un-caught validation error in project page', {
          level: 'warning',
          extra: {
            e
          }
        });
      }
    },
    async loginLocal () {
      this.$nuxt.$loading.start('loginLoader');
      this.deleteFormAPIErrors();
      try {
        await this.$refs.loginForm.validate();
        await this.login({
          username: this.username,
          password: this.password
        });
      } catch (e) {
        if (e) {
          this.setFormAPIErrors(e);
          this.$refs.loginForm.validate(() => {});
        }
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
          this.$router.push(this.localePath({ name: 'organisation-dashboard', params: this.$route.params, query: { country: [this.profile.country] } }));
        }
      } catch (e) {
        this.handleRoutingErrors(e);
      }
      this.$nuxt.$loading.finish('loginLoader');
    },

    toForgotten () {
      this.email = this.username;
      this.showForgotten = true;
    },

    forgotEmail () {
      this.deleteFormAPIErrors();
      this.$refs.forgotForm.validate(async valid => {
        if (valid) {
          try {
            await this.resetPassword({
              email: this.email
            });
            this.showForgotten = false;
            this.successfulReset = true;
          } catch (err) {
            this.setFormAPIErrors(err);
            this.$refs.loginForm.validate(() => {});
          }
        }
      });
    }
  }
};
</script>

<style lang="less">
  @import "../assets/style/variables.less";
  @import "../assets/style/mixins.less";

  .LoginComponent {
    width: @cardSizeSmall;
    min-height: calc(100vh - @topBarHeight - @actionBarHeight - @appFooterHeight - 160px);
    margin: 80px auto;

    .Instruction {
      font-size: @fontSizeMedium;
      line-height: 24px;
      text-align: center;
      color: @colorTextSecondary;
      padding: 40px 120px 20px;

      + .el-form {
        fieldset {
          padding-top: 0;
        }
      }

      + .CardActionsBottom {
        margin-top: 40px;
      }
    }

    fieldset {
      padding: 40px 80px;
    }

    .CardActionsBottom {
      .Separator {
        height: 20px;
        margin: 0 12px;
        vertical-align: middle;
      }
    }
  }
</style>
