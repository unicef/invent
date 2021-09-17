<template>
  <div class="Profile">
    <Avatar :user="user" :show-hint="false" />
    <div class="info">
      <div class="name">{{ user.name }}</div>
      <div class="email">{{ user.email }}</div>
    </div>
  </div>
</template>

<script>
import Avatar from '@/components/common/Avatar.vue'

export default {
  components: {
    Avatar,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
@import '@/assets/style/variables.less';
@import '@/assets/style/mixins.less';

.Profile {
  display: flex;
  align-items: center;
  height: 38px;
  .info {
    margin-left: 8px;
    .name {
      font-weight: bold;
      line-height: 18px;
    }
    .email {
      color: #7995a2;
      font-size: @fontSizeSmall;
      line-height: 15px;
    }
  }
}
</style>
