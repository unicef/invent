<template>
  <div class="SingupComponent">
    <el-card
      :shadow="shadow"
      :body-style="{ padding: '0px' }"
    >
      <div slot="header">
        <translate>Sign up for Digital Health Atlas</translate>
      </div>
      <el-form
        ref="form"
        :model="signupForm"
        :rules="rules"
        label-position="top"
        @submit.native.prevent="signup"
      >
        <fieldset>
          <div class="FieldsetLegend">
            <translate>Please fill out the form below:</translate>
          </div>
          <el-form-item
            :label="$gettext('Email address') | translate"
            prop="email"
          >
            <el-input
              v-model="signupForm.email"
            />
          </el-form-item>

          <el-form-item
            :label="$gettext('Password') | translate"
            prop="password1"
          >
            <el-input
              v-model="signupForm.password1"
              type="password"
            />
          </el-form-item>

          <el-form-item
            :label="$gettext('Password (again)') | translate"
            prop="password2"
          >
            <el-input
              v-model="signupForm.password2"
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
          >
            <el-col
              :span="12"
              class="SecondaryAction LoginLink"
            >
              <h6><translate>Already signed up?</translate></h6>
              <nuxt-link
                :to="localePath({name: 'organisation-login', params: $route.params})"
                class="NuxtLink Small"
              >
                <span><translate>Login here</translate></span>
              </nuxt-link>
            </el-col>
            <el-col
              :span="12"
              class="PrimaryAction"
            >
              <el-button
                type="primary"
                size="medium"
                native-type="submit"
              >
                <translate>Sign up now</translate>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import FormAPIErrorsMixin from './mixins/FormAPIErrorsMixin';

export default {
  mixins: [FormAPIErrorsMixin],
  props: {
    shadow: {
      type: String,
      default: 'always'
    }
  },
  data () {
    return {
      signupForm: {
        email: '',
        password1: '',
        password2: ''
      },
      rules: {
        email: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { type: 'email', message: this.$gettext('Has to be a valid email address'), trigger: 'blur' },
          { validator: this.validatorGenerator('email'), trigger: 'blur' }
        ],
        password1: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { min: 8, message: this.$gettext('This field should be at least 8 characters'), trigger: 'blur' },
          { validator: this.validatorGenerator('password1'), trigger: 'blur' }
        ],
        password2: [
          { required: true, message: this.$gettext('This field is required'), trigger: 'blur' },
          { validator: this.passwordMatching, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    ...mapActions({
      'doSignup': 'user/doSignup'
    }),
    passwordMatching (rule, value, callback) {
      value === this.signupForm.password1 ? callback() : callback(Error(this.$gettext('The password must match')));
    },
    signup () {
      this.deleteFormAPIErrors();
      this.$refs.form.validate(async valid => {
        if (valid) {
          try {
            // locale needs to be saved in this place due to i18n being unavailable right after the signup call
            const message = this.$gettext('User created succesfully');
            const locale = this.$i18n.locale;
            this.$nuxt.$loading.start();
            await this.doSignup({
              account_type: 'I',
              password1: this.signupForm.password1,
              password2: this.signupForm.password2,
              email: this.signupForm.email
            });
            const path = this.localePath({ ...this.$route, name: 'organisation-edit-profile' }, locale);
            this.$router.push(path);
            this.$message({
              message,
              type: 'success',
              showClose: true
            });
          } catch (e) {
            console.log(e);
            this.$nuxt.$loading.finish();
            this.setFormAPIErrors(e);
            this.$refs.form.validate(() => {});
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

  .SingupComponent {
    width: @cardSizeSmall;
    min-height: calc(100vh - @topBarHeight - @actionBarHeight - @appFooterHeight - 160px);
    margin: 80px auto;

    fieldset {
      padding: 40px 80px;
    }

    .SecondaryAction {
      h6 {
        margin: 0 0 2px;
        font-size: @fontSizeSmall;
        font-weight: 400;
        color: @colorTextSecondary;
      }
    }
  }
</style>
