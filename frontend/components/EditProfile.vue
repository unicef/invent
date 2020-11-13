<template>
  <div class="EditProfile">
    <div class="PageTitle">
      <h2><translate>Edit my profile</translate></h2>
    </div>

    <el-card :body-style="{ padding: '0px' }" class="ProfileCard">
      <el-form
        ref="editProfileForm"
        :rules="rules"
        :model="innerProfile"
        label-position="top"
        class="FormPart"
        @submit.native.prevent
      >
        <el-row type="flex">
          <el-col :span="12" class="UserForm">
            <el-form-item
              :label="$gettext('First and Last Name') | translate"
              prop="name"
            >
              <el-input v-model="innerProfile.name" type="text" />
            </el-form-item>

            <el-form-item
              :label="$gettext('Email address') | translate"
              class="is-required"
            >
              <el-input v-model="innerProfile.email" disabled type="text" />
            </el-form-item>

            <el-form-item
              :label="$gettext('Country') | translate"
              prop="country"
            >
              <country-select v-model="innerProfile.country" />
              <div
                v-if="nonFieldErrors"
                class="el-form-item__error ModifiedFormError"
              >
                {{ nonFieldErrors }}
              </div>
            </el-form-item>

            <el-form-item
              :label="$gettext('Site language') | translate"
              prop="language"
            >
              <language-select v-model="innerProfile.language" />
            </el-form-item>
          </el-col>
        </el-row>

        <div class="CardActionsBottom">
          <el-row
            type="flex"
            justify="space-between"
            align="middle"
            class="cardActions"
          >
            <el-col :span="6" class="SecondaryAction">
              <el-button
                type="text"
                class="CancelButton IconLeft"
                @click="dismissChanges"
              >
                <fa icon="reply" />
                <translate>Dismiss changes</translate>
              </el-button>
            </el-col>
            <el-col :span="6" class="PrimaryAction">
              <el-button
                type="primary"
                size="medium"
                native-type="submit"
                @click="submit"
              >
                <translate>Save settings</translate>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import FormAPIErrorsMixin from './mixins/FormAPIErrorsMixin'
import LanguageSelect from './common/LanguageSelect'
import CountrySelect from './common/CountrySelect'

export default {
  components: {
    LanguageSelect,
    CountrySelect,
  },
  mixins: [FormAPIErrorsMixin],
  data() {
    return {
      innerProfile: {
        name: null,
        language: null,
        country: null,
        account_type: null,
        donor: null,
      },
      isCountryUser: false,
      isDonorUser: true,
      changeApprovedUserRole: false,
      donorFilters: ['unicef'],
    }
  },
  async fetch({ store, params }) {
    await store.dispatch('system/loadStaticData')
  },
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
      user: 'user/getUser',
      unicefOrganisation: 'system/getUnicefOrganisation',
      unicefDonor: 'system/getUnicefDonor',
    }),

    userTypeRequested() {
      return (
        this.profile &&
        this.profile.account_type !== 'I' &&
        !this.profile.account_type_approved
      )
    },
    isDonorRequired() {
      return (
        this.innerProfile &&
        this.innerProfile.account_type &&
        ['D', 'DA', 'SDA'].includes(this.innerProfile.account_type)
      )
    },
    rules() {
      return {
        name: [
          {
            required: true,
            message: this.$gettext('This field is required'),
            trigger: 'change',
          },
          { validator: this.validatorGenerator('name') },
        ],
        language: [
          {
            required: true,
            message: this.$gettext('This field is required'),
            trigger: 'change',
          },
          { validator: this.validatorGenerator('language') },
        ],
        country: [
          {
            required: true,
            message: this.$gettext('This field is required'),
            trigger: 'change',
          },
          { validator: this.validatorGenerator('country') },
        ],
      }
    },
  },

  watch: {
    profile: {
      immediate: true,
      handler(profile) {
        this.innerProfile = {
          ...profile,
          organisation: this.unicefOrganisation.id,
          donor: this.unicefDonor.id,
        }
      },
    },
  },

  methods: {
    ...mapActions({
      updateUserProfile: 'user/updateUserProfile',
    }),

    dismissChanges() {
      this.innerProfile = {
        ...this.profile,
        organisation: this.unicefOrganisation.id,
        donor: this.unicefDonor.id,
      }
      this.$router.go(-1)
    },

    submit() {
      this.deleteFormAPIErrors()
      this.changeApprovedUserRole = false
      this.$refs.editProfileForm.validate(async (valid) => {
        if (valid) {
          try {
            const isFirstSave = !this.profile.country
            await this.updateUserProfile(this.innerProfile)
            window.scrollTo(0, 0)
            this.$message({
              message: this.$gettext('Profile succesfully updated'),
              type: 'success',
              showClose: true,
            })
            if (isFirstSave) {
              this.routeToDashboard(this.innerProfile.language)
            } else {
              this.changeLocale(this.innerProfile.language)
            }
          } catch (err) {
            console.log('ERR:', err)
            this.setFormAPIErrors(err)
            this.$refs.editProfileForm.validate(() => {})
            this.$message({
              message: this.$gettext('Profile update error'),
              type: 'error',
              showClose: true,
            })
          }
        }
      })
    },
    changeLocale(locale) {
      if (locale !== this.$i18n.locale) {
        const name = this.$route.name.split('___')[0]
        const path = this.localePath({ ...this.$route, name }, locale)
        this.$router.replace(path)
      }
    },
    routeToDashboard(locale) {
      const path = this.localePath(
        { name: 'organisation-inventory-list', params: this.$route.params },
        locale
      )
      this.$router.push(path)
    },
    changingUserRole() {
      this.changeApprovedUserRole = true
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.EditProfile {
  margin-bottom: 80px;

  .ProfileCard {
    width: @cardSizeMedium;
    margin: 0 auto;

    .UserForm {
      padding: 40px 80px;

      .CountrySelector {
        width: 100%;
      }
    }

    .UserRole {
      padding: 40px 80px;
      border-left: 1px solid @colorGrayLight;
      // background-color: #FFFBDC;

      h5 {
        margin: 0 0 10px;
        font-size: @fontSizeBase;
        font-weight: 700;
        line-height: 40px;

        &.RoleRequested {
          margin: 0;

          .svg-inline--fa {
            margin-right: 6px;
            color: darken(@colorDraft, 15%);
          }

          + p {
            margin: 0;
            color: @colorTextSecondary;
            font-size: @fontSizeSmall;
            line-height: 18px;
          }
        }

        &.RoleAccepted {
          font-weight: 400;

          .svg-inline--fa {
            margin-right: 6px;
            color: #67c23a;
          }
        }
      }

      .Separator {
        .SeparatorStyleHorizontal();
        margin: 30px 0;
      }

      .el-checkbox {
        &.is-bordered {
          position: relative;
          width: 100%;
          height: auto;
          padding: 15px;
          transition: @transitionAll;

          &:hover {
            .IconRole {
              filter: grayscale(0);
              opacity: 1;
            }
          }

          &:hover,
          &.is-checked {
            border-color: @colorBrandPrimary;
            background-color: @colorBrandBlueLight;

            .IconRole {
              filter: grayscale(0);
              opacity: 1;
            }
          }
        }
      }

      .el-radio-group {
        margin: 10px 0 0;
        padding: 0 30px;

        + .el-form {
          margin-top: 10px;
        }
      }

      .IconRole {
        position: absolute;
        top: 50%;
        right: 15px;
        transform: translateY(-50%);
        display: inline-block;
        width: 36px;
        height: 24px;
        background-position: right center;
        background-size: contain;
        background-repeat: no-repeat;
        filter: grayscale(1);
        opacity: 0.6;
        transition: @transitionAll;

        &.IconGovernmentUser {
          top: 46%;
          background-image: url('~static/icon-role-government.svg');
        }

        &.IconInvestorUser {
          background-image: url('~static/icon-role-investor.svg');
        }
      }

      .UserArchTypeText {
        margin: 15px 0 0;
        font-size: @fontSizeSmall;
        line-height: 18px;
        color: @colorTextSecondary;
      }

      .UserTypeTextList {
        margin-bottom: 10px;

        li {
          margin-bottom: 5px;
          font-size: @fontSizeSmall - 1;
          line-height: 16px;
          color: @colorTextSecondary;
        }
      }

      .DonorSelectorWrapper {
        width: 100%;
        margin-top: 20px;

        .el-select {
          min-width: 75%;
          max-width: 100%;
        }
      }

      .UserRoleDescription {
        position: relative;
        width: 100%;
        border: 1px solid @colorGray;

        .ClickThrough {
          pointer-events: none;
        }

        .el-row {
          .el-col {
            padding: 10px 10px 15px;

            &:nth-child(1) {
              width: auto;
            }

            &:nth-child(2) {
              width: 100%;
            }
          }
        }

        .el-button {
          position: absolute;
          top: 15px;
          right: 20px;
        }

        .IconRole {
          position: relative;
          top: 3px;
          right: auto;
          transform: none;
          filter: grayscale(0);
          opacity: 1;
          width: 32px;
          height: 48px;
          margin-left: 10px;
        }

        h5 {
          margin: 0;
          line-height: 24px;

          + span {
            font-size: @fontSizeBase - 1;
            color: @colorTextSecondary;
          }
        }

        .MyPrivileges {
          background-color: @colorGrayLightest;
          padding: 20px 20px 15px;

          > span {
            font-size: @fontSizeSmall;
          }

          ul {
            margin: 10px 30px;
            padding: 0;

            li {
              margin-bottom: 5px;
              font-size: @fontSizeSmall;
            }
          }
        }
      }
    }
  }
}
</style>
