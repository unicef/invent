<template>
  <el-tooltip :content="contact" placement="top-start" :disabled="!showHint">
    <div
      :class="`Avatar ${noBorder}`"
      :style="`color: ${colors.text}; background-color: ${colors.background}; border: ${colors.border};`"
    >
      <img v-if="profileImage" :src="profileImage" alt="Profile image" loading="lazy" />
      <template v-else-if="profileIcon">
        <i :class="`icon ${profileIcon}`"></i>
      </template>
      <template v-else>
        {{ initial }}
      </template>
    </div>
  </el-tooltip>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
    showHint: {
      type: Boolean,
      default: true,
    },
    showInitial: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    initial() {
      let ini = '-'
      if (!this.showInitial) {
        ini = this.user?.name
      } else if (this.user?.name) {
        ini = this.user.name.charAt(0).toUpperCase()
      } else if (this.user?.email) {
        ini = this.user.email.charAt(0).toUpperCase()
      }
      return ini
    },
    contact() {
      let contact = ''
      if (this.showHint) {
        const name = this.user?.name ? this.user.name : ''
        const email = this.user?.email ? this.user.email : ''
        contact = `${name} <${email}>`
      }
      return contact
    },
    colors() {
      return this.user?.colorScheme
        ? this.user.colorScheme
        : {
            text: '#777779',
            background: '#EAE6E1',
            border: '2px solid #fff',
          }
    },
    noBorder() {
      return this.colors.border === 'none' ? 'noborder' : ''
    },
    profileImage() {
      return this.user?.picture
    },
    profileIcon() {
      return this.user?.icon
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';
.Avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  width: 30px;
  height: 30px;
  line-height: 30px;
  border-radius: 50%;
  text-align: center;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.125s ease-in-out;
  img {
    width: 100%;
  }
  &:hover {
    box-shadow: inset 0 0 0 1px #d8d1c9;
    transform: scale(1.2);
  }
  &.noborder {
    width: 34px;
    height: 34px;
    line-height: 34px;
  }
  .icon {
    &::before {
      font-size: 20px;
    }
  }
}
</style>
