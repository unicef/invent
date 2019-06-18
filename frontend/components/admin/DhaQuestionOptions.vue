<template>
  <div class="ListOfOptions">
    <h6><translate>List of selectable options:</translate></h6>
    <p v-if="!options.length">
      <translate>No options added yet</translate>
    </p>
    <ul>
      <li
        v-for="(option, index) in options"
        :key="index"
      >
        <fa icon="check-circle" />
        <span class="Option">
          {{ option }}
        </span>
        <el-button
          v-if="!disabled"
          :disabled="disabled"
          type="text"
          size="mini"
          class="DeleteButton IconLeft RemoveOption"
          @click="removeOption(index)"
        >
          <fa icon="times" />
        </el-button>
      </li>
    </ul>
    <el-tooltip
      :disabled="!disabled"
      :content="$gettext('Unable to add or remove options on saved questions') | translate"
      placement="top"
    >
      <el-row
        type="flex"
        align="middle"
      >
        <el-col :span="16">
          <el-input
            ref="input"
            v-model="inputField"
            :disabled="disabled"
            :placeholder="$gettext('Add a new option here') | translate"
            type="text"
            @keyup.enter.native="addOption"
          />
        </el-col>
        <el-col :span="8">
          <el-button
            :disabled="!inputField || disabled"
            type="text"
            class="IconLeft AddOption"
            @click="addOption"
          >
            <fa icon="plus" /> <translate>Add</translate>
          </el-button>
        </el-col>
      </el-row>
    </el-tooltip>
  </div>
</template>

<script>

export default {

  props: {
    options: {
      type: Array,
      default: () => []
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      inputField: ''
    };
  },
  methods: {
    removeOption (index) {
      this.options.splice(index, 1);
    },
    addOption () {
      this.options.push(this.inputField);
      this.inputField = '';
      this.$refs.input.focus();
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

  .ListOfOptions {
    margin-bottom: 10px;

    h6 {
      font-size: @fontSizeBase;
      margin: 30px 0 10px;

      + p {
        font-size: @fontSizeBase;
        color: @colorGray;
        margin: 20px 0;
      }
    }

    .AddOption {
      margin-left: 20px;
    }

    .RemoveOption {
      padding: 0;
    }

    .Option {
      margin: 0 10px 0 5px;
    }

    ul {
      list-style-type: none;
      display: block;
      margin: 20px 0;
      padding: 0 15px;

      li {
        display: flex;
        align-items: center;
        margin: 0 0 10px;
        font-size: @fontSizeBase;
      }

      .svg-inline--fa {
        width: 14px;
        height: 14px;
        padding: 1px;
      }
    }
  }

</style>
