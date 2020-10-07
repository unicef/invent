<template>
  <div class="vue-django-feedback">
    <vue-django-feedback
      v-if="token"
      :name="name"
      :name-label="$gettext('Name') | translate"
      :email-label="$gettext('Email') | translate"
      :subject-label="$gettext('Subject') | translate"
      :message-label="$gettext('Message') | translate"
      :email="email"
      :csrf-token="token"
    >
      <span slot="header-text">
        <translate> Ask our experts </translate>
      </span>
      <span slot="success-header">
        <translate>Thank you</translate>
      </span>
      <span slot="success-message">
        <translate>
          Your message has been successfully sent! We will be back to you soon!
        </translate>
      </span>
      <span slot="error-header">
        <translate> Sorry </translate>
      </span>
      <span slot="error-message">
        <translate>
          There was a problem processing your ticket, please try again
        </translate>
      </span>
      <span slot="hint-text">
        <translate>
          Click here if you are experiencing any issues or have suggestion for
          improving the website
        </translate>
      </span>
    </vue-django-feedback>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import VueDjangoFeedback from './feedback/RawDjangoFeedback.vue'

export default {
  components: { VueDjangoFeedback },
  $_veeValidate: {
    validator: 'new',
  },
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
      token: 'user/getToken',
    }),
    name() {
      if (this.profile) {
        return this.profile.name
      }
      return null
    },
    email() {
      if (this.profile) {
        return this.profile.email
      }
      return null
    },
  },
}
</script>

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
@import './feedback/variables.less';
@import './feedback/main.less';

.vue-django-feedback {
  .vue-django-feedback {
    z-index: 5000;
    font-family: 'Univers', Arial, sans-serif;
    color: @colorTextPrimary;
  }

  .feedback-button {
    background-color: @colorBrandPrimary;

    .icon.icon-opened {
      > span {
        font-weight: 700 !important;
      }
    }
  }

  .pop-up-container {
    .header {
      background-color: @colorBrandPrimary;

      .icon.icon-opened {
        > span {
          font-weight: 700 !important;
        }
      }

      h2 {
        font-weight: 700;
        letter-spacing: -0.5px;
      }
    }

    .message-container {
      h4 {
        color: @colorPublished;

        &.error {
          color: @colorDanger;
        }
      }

      p {
        color: @colorTextSecondary;
      }
    }

    .pop-up-controls {
      border-color: @colorGrayLight;
      border-radius: 0;

      .error-info {
        font-weight: 700;
        color: @colorDanger;

        .icon.icon-danger span {
          font-weight: 700;
        }
      }

      .actions {
        button {
          color: @colorBrandPrimary;
          font-weight: 700;
          text-transform: none;

          &:hover {
            color: @colorBrandPrimaryLight;
          }

          &:disabled {
            color: @colorTextMuted;
          }
        }
      }
    }

    .input-container {
      label {
        color: @colorTextPrimary;
        font-weight: 700;
      }

      input,
      textarea {
        color: @colorTextPrimary;
        border-color: @colorTextMuted;
        border-radius: 0;

        &:hover,
        &:focus {
          border-color: @colorGray;
        }

        &.error {
          border-color: @colorDanger;
        }
      }

      .feedback {
        color: @colorTextMuted;

        .errors {
          color: @colorDanger;
        }
      }
    }

    .user-block {
      .user {
        .name {
          font-weight: 700;
        }

        .email {
          color: @colorTextSecondary;
        }
      }
    }
  }
}
</style>
