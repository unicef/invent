<template>
  <el-tabs
    :value="activeTab"
    @tab-click="tabChangeHandler"
  >
    <el-tab-pane
      :label="$gettext('Sub-national') | translate"
      name="subNational"
    >
      <project-card
        v-for="p in projects"
        :key="p.id"
        :project="p"
        show-organisation
        show-arrow-on-over
      />
      <div
        v-show="projects.length === 0"
        class="HintText"
      >
        <fa
          icon="info-circle"
          size="lg"
        />
        <translate>No project to show...</translate>
      </div>
    </el-tab-pane>
    <el-tab-pane
      :label="$gettext('National') | translate"
      name="national"
    >
      <project-card
        v-for="p in projects"
        :key="p.id"
        :project="p"
        show-organisation
        show-arrow-on-over
      />
      <div
        v-show="projects.length === 0"
        class="HintText"
      >
        <fa
          icon="info-circle"
          size="lg"
        />
        <translate>No project to show...</translate>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import ProjectCard from '../ProjectCard';

export default {
  components: {
    ProjectCard
  },
  props: {
    activeTab: {
      type: String,
      required: true
    },
    projects: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    activeTab: {
      immediate: true,
      handler (value) {
        if (value) {
          this.setStripeSize();
        }
      }
    }
  },
  methods: {
    tabChangeHandler (value) {
      this.$emit('change', value);
    },
    setStripeSize () {
      this.$nextTick(() => {
        try {
          const stripe = this.$el.querySelector('.el-tabs__active-bar');
          const tabName = this.$el.querySelector('.el-tabs__item.is-active');
          const tabNameBox = tabName.getBoundingClientRect();
          const tabsContainer = this.$el.querySelector('.el-tabs__nav-scroll').getBoundingClientRect();
          const stripeLeftCorner = tabNameBox.left - tabsContainer.left;
          const paddingLeft = parseInt(getComputedStyle(tabName).paddingLeft, 10);
          const paddingRight = parseInt(getComputedStyle(tabName).paddingRight, 10);
          const padding = paddingLeft > paddingRight ? paddingLeft : paddingRight;
          const stripeWidth = tabNameBox.width - padding;
          const stripeTranslate = stripeLeftCorner === 0 ? 0 : stripeLeftCorner + paddingLeft;
          stripe.style.width = `${stripeWidth}px`;
          stripe.style.transform = `translate(${stripeTranslate}px)`;
        } catch (e) {
          console.error('Failed to calculate strip lenght', e);
        }
      });
    }
  }
};
</script>

<style>

</style>
