<template>
  <div :class="['vue-django-feedback', 'main', 'container', 'right', { opened }]">
    <button
      class="feedback-button"
      @click="togglePopUp()"
      @mouseenter="handleMouseOver(true)"
      @mouseleave="handleMouseOver(false)"
    >
      <i class="icon icon-closed">
        <span>&times;</span>
      </i>
      <i class="icon icon-opened">
        <span>?</span>
      </i>
    </button>

    <div :class="['hint-container', { open: showHintContainer }]">
      <div>
        <div>
          <slot name="hint-text">
            Click here if you are experiencing any issues or have suggestion for improving the website!
          </slot>
        </div>
      </div>
    </div>

    <div class="pop-up-container">
      <div class="header">
        <i class="icon icon-opened">
          <span>?</span>
        </i>
        <h2>
          <slot name="header-text"> Ask our experts! </slot>
        </h2>
      </div>

      <div v-show="!submitted" class="form-container">
        <div v-show="showUserBlock" class="user-block">
          <div class="avatar">
            <img v-if="!showAvatarPlaceholder" :src="avatarUrl" class="avatar-img" alt="avatar" loading="lazy" />
            <div v-show="showAvatarPlaceholder" class="avatar-placeholder">
              <i class="icon icon-avatar" />
            </div>
          </div>
          <div class="user">
            <span class="name">
              {{ name }}
            </span>
            <span class="email">
              {{ email }}
            </span>
          </div>
        </div>

        <div v-if="!showUserBlock" :class="['input-container', 'input', 'name', { danger: errors.has('name') }]">
          <label>
            {{ nameLabel }}
          </label>
          <input v-model="form.name" v-validate="{ required: true }" name="name" type="text" />
          <div class="feedback">
            <div class="errors">
              <span v-show="errors.has('name')" class="error danger">
                {{ errors.first('name') }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="!showUserBlock" :class="['input-container', 'input', 'email', { danger: errors.has('email') }]">
          <label>
            {{ emailLabel }}
          </label>
          <input v-model="form.email" v-validate="{ required: true, email: true }" name="email" type="email" />
          <div class="feedback">
            <div class="errors">
              <span v-show="errors.has('email')" class="error danger">
                {{ errors.first('email') }}
              </span>
            </div>
          </div>
        </div>

        <div :class="['input-container', 'input', 'subject', { danger: errors.has('subject') }]">
          <label>
            {{ subjectLabel }}
          </label>
          <input
            v-model="form.subject"
            v-validate="{ required: true, max: limit.subjectLimit }"
            name="subject"
            type="text"
          />
          <div class="feedback">
            <div class="errors">
              <span v-show="errors.has('subject')" class="error danger">
                {{ errors.first('subject') }}
              </span>
            </div>
            <div class="char-count">{{ form.subject.length }} / {{ limit.subjectLimit }}</div>
          </div>
        </div>

        <div :class="['input-container', 'textarea', 'message', { danger: errors.has('message') }]">
          <label>
            {{ messageLabel }}
          </label>
          <textarea
            v-model="form.message"
            v-validate="{ required: true, max: limit.messageLimit }"
            name="message"
            rows="3"
          />
          <div class="feedback">
            <div class="errors">
              <span v-show="errors.has('message')" class="error danger">
                {{ errors.first('message') }}
              </span>
            </div>
            <div class="char-count">{{ form.message.length }} / {{ limit.messageLimit }}</div>
          </div>
        </div>
      </div>

      <div v-show="!submitted" class="pop-up-controls">
        <div class="actions">
          <button :disabled="processing" @click="submit()">
            {{ submitButtonText }}
          </button>
        </div>
        <div v-show="errors.any()" class="error-info">
          <i class="icon icon-danger">
            <span>!</span>
          </i>
          {{ globalErrorWarning }}
        </div>
      </div>

      <div v-show="submitted" class="message-container">
        <h4>
          <slot name="success-header"> Thank you! </slot>
        </h4>
        <p>
          <slot name="success-message"> Your message has been successfully sent! We will be back to you soon! </slot>
        </p>
      </div>

      <div v-show="apiError" class="message-container">
        <h4 class="error">
          <slot name="error-header"> Sorry </slot>
        </h4>
        <p>
          <slot name="error-message"> There was a problem processing your ticket, please try again </slot>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VueDjangoFeedback',
  inject: ['$validator'],
  props: {
    apiUrl: {
      type: String,
      default: '/api/tickets/',
    },
    authToken: {
      type: String,
      default: null,
    },
    csrfToken: {
      type: String,
      default: null,
    },
    meta: {
      type: String,
      default: undefined,
    },
    name: {
      type: String,
      default: null,
    },
    email: {
      type: String,
      default: null,
    },
    avatarUrl: {
      type: String,
      default: null,
    },
    submitButtonText: {
      type: String,
      default: 'Submit',
    },
    globalErrorWarning: {
      type: String,
      default: 'Error!',
    },
    nameLabel: {
      type: String,
      default: 'Your name',
    },
    emailLabel: {
      type: String,
      default: 'Your email',
    },
    subjectLabel: {
      type: String,
      default: 'Subject',
    },
    messageLabel: {
      type: String,
      default: 'Message / Question',
    },
  },
  data() {
    return {
      submitted: false,
      apiError: false,
      processing: false,
      buttonHover: false,
      form: {
        name: '',
        email: '',
        subject: '',
        message: '',
      },
      limit: {
        subjectLimit: 120,
        messageLimit: 999,
      },
    }
  },
  computed: {
    storeForm() {
      return this.$store.state.user.feedbackForm
    },
    opened: {
      get() {
        return this.$store.state.user.feedbackOn
      },
      set(val) {
        this.$store.commit('user/SET_FEEDBACK', { feedbackOn: val })
      },
    },
    showUserBlock() {
      return !!(this.name && this.email)
    },
    showAvatarPlaceholder() {
      return !this.avatarUrl
    },
    parsedMeta() {
      let result = {}
      try {
        result = JSON.parse(this.meta)
      } catch (e) {
        console.warn('unable to parse the meta field', e)
      }
      return {
        ...result,
        navigator: {
          userAgent: window.navigator.userAgent,
          platform: window.navigator.platform,
          appVersion: window.navigator.appVersion,
          product: window.navigator.product,
          vendor: window.navigator.vendor,
        },
      }
    },
    showHintContainer() {
      return this.buttonHover && !this.opened
    },
  },
  watch: {
    storeForm(newData) {
      this.form.subject = newData.subject
      this.form.message = newData.message
    },
  },
  beforeCreate() {
    this.axios = axios.create()
  },
  methods: {
    togglePopUp() {
      this.opened = !this.opened
      if (!this.opened) {
        this.form.name = ''
        this.form.email = ''
        this.form.subject = ''
        this.form.message = ''
        this.submitted = false
        this.apiError = false
      }
      this.errors.clear()
    },
    async submit() {
      await this.$validator.validateAll()
      if (!this.errors.any()) {
        this.processing = true
        try {
          const data = {
            email: this.email ? this.email : this.form.email,
            subject: this.form.subject,
            text: this.form.message,
            meta: {
              ...this.parsedMeta,
              name: this.name ? this.name : this.form.name,
            },
          }
          const headers = {}
          if (this.authToken) {
            headers.Authorization = this.authToken
          }
          if (this.csrfToken) {
            headers['x-csrftoken'] = this.csrfToken
          }
          await this.axios.post(this.apiUrl, data, { headers })
          this.submitted = true
          this.apiError = false
        } catch (e) {
          this.apiError = true
          console.warn(e)
        }
        this.processing = false
      }
    },
    handleMouseOver(status) {
      this.buttonHover = status
    },
  },
}
</script>

<style lang="less" scoped>
@import './main.less';
</style>
