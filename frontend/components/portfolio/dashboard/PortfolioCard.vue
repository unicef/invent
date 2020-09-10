<template>
  <article :class="`portfolio-card ${item.status}`">
    <div class="wrapper">
      <p :class="`${item.status}`">{{ item.status }}</p>
      <span :class="`icon-circle icon-tiip-${item.icon}`">
        <template v-if="path(item.icon)">
          <span class="path1" /><span class="path2" />
        </template>
      </span>
      <p class="name">
        {{ item.name }} <span>({{ item.total }})</span>
      </p>
    </div>
    <div class="details">
      <div class="wrapper">
        <div class="icon-wrapper">
          <span :class="`icon-bg icon-tiip-${item.icon}`">
            <template v-if="path(item.icon)">
              <span class="path1" /><span class="path2" />
            </template>
          </span>
        </div>
        <p :class="`${item.status}`">{{ item.status }}</p>
        <p class="name">
          {{ item.name }} <span>({{ item.total }})</span>
        </p>
        <div class="links">
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-portfolio-management-id',
                params: { id: item.id }
              })
            "
          >
            <translate>Manage</translate>
          </nuxt-link>
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-portfolio-management-edit-id',
                params: { id: item.id }
              })
            "
          >
            <translate>Edit info</translate>
          </nuxt-link>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  components: {},
  methods: {
    path(icon) {
      return icon === "breast_feeding" || icon === "mother_and_baby";
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";
.portfolio-card {
  width: 400px;
  height: 240px;
  margin-bottom: 16px;
  overflow: hidden;
  position: relative;
  margin-right: 20px;
  transition: all 0.25s;
  &:nth-child(3n + 0) {
    margin-right: 0px;
  }
  .wrapper {
    display: flex;
    flex-direction: column;
  }
  .icon-circle {
    margin-top: calc(25px - 10px);
    margin-bottom: 20px;
    border-radius: 50px;
    font-size: 52px;
    padding: 12px;
    align-self: center;
    border: 2px dotted @colorBrandPrimary;
  }

  .icon-wrapper {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1;
    width: 100%;
    height: 100%;
    .icon-bg {
      opacity: 0.1;
      font-size: 150px;
    }
  }
  .active,
  .draft,
  .archived {
    margin: 10px;
    padding: 0px 10px;
    border-radius: 3px;
    font-size: 10px;
    letter-spacing: 0;
    line-height: 24px;
    text-align: center;
    text-transform: uppercase;
    align-self: flex-end;
  }
  .active {
    background-color: #e2f4fc;
  }
  .draft {
    background-color: #ffd765;
    color: @colorBrandGrayDark;
  }
  .archived {
    background-color: #c4c4c4;
    color: @colorWhite;
  }
  .name {
    font-size: 18px;
    letter-spacing: 0;
    line-height: 24px;
    font-weight: 700;
    text-transform: uppercase;
    align-self: center;
    margin: 0;
    padding: 0 60px;
    text-align: center;
    span {
      font-weight: 100;
    }
  }
  .details {
    width: 400px;
    height: 240px;
    background-color: @colorWhite;
    position: absolute;
    top: 240px;
    transition: all 0.3s;
    .name,
    .links {
      z-index: 2;
    }
    .name {
      font-size: 22px;
      padding: 0 20px;
      line-height: 28px;
      margin-top: 50px;
      margin-bottom: 32px;
    }
    .links {
      width: 242px;
      align-self: center;
      display: flex;
      justify-content: space-between;
      a:first-child {
        background-color: @colorBrandPrimary;
        color: @colorWhite;
      }
      a {
        height: 22px;
        width: 92px;
        padding: 10px;
        background-color: #c6eafa;
        font-size: 16px;
        font-weight: bold;
        letter-spacing: 0;
        line-height: 20px;
        text-align: center;
        text-decoration: none;
      }
    }
  }
  &.active {
    background-color: #c6eafa;
    color: @colorBrandPrimary;
  }
  &.draft {
    background-color: #ffeebd;
    color: @colorBrandPrimary;
  }
  &.archived {
    background-color: #e6e6e6;
    color: @colorBrandGrayDark;
    .icon-circle {
      &:before {
        color: @colorBrandGrayDark;
      }
      border-color: @colorBrandGrayDark;
    }
    .icon-bg {
      &:before {
        color: @colorBrandGrayDark;
      }
    }
    .details {
      a:first-child {
        background-color: @colorBrandGrayDark;
        color: @colorWhite;
      }
      a {
        color: @colorBrandGrayDark;
        background-color: #eae6e1;
      }
    }
  }
  &:hover {
    box-shadow: 5px 5px 20px 0 rgba(0, 0, 0, 0.12);
    .details {
      top: 0;
    }
  }
}
</style>
