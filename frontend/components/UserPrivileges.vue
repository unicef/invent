<template>
  <ul class="UserTypeTextList">
    <template v-if="type === 'G'">
      <li>
        <translate key="g-item-list-1">
          Can read/export responses to private Government questions
        </translate>
      </li>
      <li>
        <translate key="g-item-list-2">
          Can view when a project is approved/declined
        </translate>
      </li>
    </template>
    <template v-if="type === 'CA'">
      <li>
        <translate key="ca-list-item-1">
          Can update Government map data
        </translate>
      </li>
      <li>
        <translate key="ca-list-item-2">
          Can create and delete Government-specific questions
        </translate>
      </li>
      <li>
        <translate key="ca-list-item-3">
          Can select which questions are private and public
        </translate>
      </li>
      <li>
        <translate key="ca-list-item-4">
          Can read/export responses to private Government questions
        </translate>
      </li>
      <li>
        <translate key="ca-list-item-5">
          Can approve users to join the Government page
        </translate>
      </li>
      <li>
        <translate key="ca-list-item-6">
          Can approve initiatives if the iniciative approval feature is active
        </translate>
      </li>
    </template>
    <template v-if="type === 'SCA'">
      <li>
        <translate key="sca-list-item-1">
          Can update Government map data
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-2">
          Can create and delete Government-specific questions
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-3">
          Can select which questions are private and public
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-4">
          Can read/export responses to private Government questions
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-5">
          Can approve users to join the Government page
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-6">
          Can approve initiatives if the initiative approval feature is active
        </translate>
      </li>
      <li>
        <translate key="sca-list-item-7">
          Can customize and update Government home page
        </translate>
      </li>
    </template>
    <template v-if="type === 'D'">
      <li>
        <translate key="d-list-item-1">
          Can read/export responses to private investor questions
        </translate>
      </li>
    </template>
    <template v-if="type === 'DA'">
      <li>
        <translate key="da-list-item-1">
          Can read/export responses to private investor questions
        </translate>
      </li>
      <li>
        <translate key="da-list-item-2">
          Can create and delete investor-specific questions
        </translate>
      </li>
      <li>
        <translate key="da-list-item-3">
          Can select which questions are private and public
        </translate>
      </li>
      <li>
        <translate key="da-list-item-4">
          Can approve users to join the investor page
        </translate>
      </li>
    </template>
    <template v-if="type === 'SDA'">
      <li>
        <translate key="sda-list-item-1">
          Can read/export responses to private investor-specific questions
        </translate>
      </li>
      <li>
        <translate key="sda-list-item-2">
          Can create and delete investor-specific questions
        </translate>
      </li>
      <li>
        <translate key="sda-list-item-3">
          Can select which questions are private and public
        </translate>
      </li>
      <li>
        <translate key="sda-list-item-4">
          Can approve users to join the investor page
        </translate>
      </li>
      <li>
        <translate key="sda-list-item-5">
          Can customize and update investor home page
        </translate>
      </li>
    </template>
  </ul>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      default: null,
      validator: (value) => ['G', 'CA', 'SCA', 'D', 'DA', 'SDA'],
    },
  },
}
</script>

<style></style>
