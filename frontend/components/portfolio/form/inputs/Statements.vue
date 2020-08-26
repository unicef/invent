<template>
  <div
    v-model="innerValue"
    v-bind="{ ...$props, ...$attrs }"
    v-on="{ ...$listeners }"
    class="statements"
  >
    <div v-for="(item, i) in $attrs.value" :key="i" class="statement">
      <div class="close" @click="handleRemoveStatement(i)">
        <fa icon="times" />
      </div>
      <custom-required-form-item :error="errors.first('statementName')" row>
        <template slot="label">
          <translate key="portfolio-statement-name">
            Name
          </translate>
        </template>
        <character-count-input
          v-model="item.name"
          data-as-name="statement Name"
          data-vv-name="statementName"
        />
      </custom-required-form-item>

      <custom-required-form-item
        :error="errors.first('statementDescription')"
        row
      >
        <template slot="label">
          <translate key="portfolio-statementDescription">
            Description
          </translate>
        </template>

        <character-count-input
          v-model="item.description"
          data-vv-name="statementDescription"
          data-vv-as="Description"
          type="textarea"
        />
      </custom-required-form-item>
    </div>
    <p @click="handleAddStatement" class="add">
      <fa icon="plus" /><translate>Add new statement</translate>
    </p>
  </div>
</template>

<script>
import { mapState } from "vuex";
import VeeValidationMixin from "@/components/mixins/VeeValidationMixin";
import PortfolioFieldsetMixin from "@/components/mixins/PortfolioFieldsetMixin";

export default {
  mixins: [VeeValidationMixin, PortfolioFieldsetMixin],
  model: {
    prop: "value",
    event: "change"
  },
  computed: {
    innerValue: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("change", value);
      }
    }
  },
  methods: {
    handleAddStatement() {
      this.innerValue = [...this.$attrs.value, { name: "", description: "" }];
    },
    handleRemoveStatement(idx) {
      const outputArray = [];
      for (let i = 0; i < this.$attrs.value.length; i++) {
        if (idx !== i) {
          outputArray.push(this.$attrs.value[i]);
        }
      }
      this.innerValue = outputArray;
    }
  }
};
</script>

<style lang="less" scoped>
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.statements {
  position: relative;
  .add {
    height: 18px;
    width: 170px;
    color: @colorBrandPrimary;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0;
    line-height: 18px;
    cursor: pointer;
    svg {
      margin-right: 10px;
    }
  }
  .statement {
    position: relative;
    box-sizing: border-box;
    height: 229px;
    width: 100%;
    border: 1px solid #eae6e1;
    background-color: #f5f3ef;
    margin-bottom: 24px;
    .close {
      position: absolute;
      top: -10px;
      right: -10px;
      height: 24px;
      width: 24px;
      background-color: @colorWhite;
      color: @colorDanger;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.18);
      -webkit-border-radius: 20px;
      -moz-border-radius: 20px;
      border-radius: 20px;
      cursor: pointer;
      svg {
        margin: 5px 7px;
      }
    }
  }
}
</style>
