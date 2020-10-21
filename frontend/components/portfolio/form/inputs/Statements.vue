<template>
  <div class="statements">
    <div v-for="(item, i) in statements" :key="i" class="statement">
      <div class="close" @click="handleRemoveStatement(i)">
        <fa icon="times" />
      </div>
      <custom-required-form-item row>
        <template slot="label">
          <translate key="portfolio-statement-name"> Name </translate>
        </template>
        <el-input
          :value="item.name"
          placeholder="Max. 80 characters"
          @input="handleInput($event, 'name', i)"
        />
      </custom-required-form-item>

      <custom-required-form-item row>
        <template slot="label">
          <translate key="portfolio-statement-description">
            Description
          </translate>
        </template>
        <el-input
          :value="item.description"
          type="textarea"
          placeholder="Max. 1000 characters"
          rows="3"
          @input="handleInput($event, 'description', i)"
        />
      </custom-required-form-item>
    </div>
    <p class="add" @click="handleAddStatement">
      <fa icon="plus" /><translate>Add new statement</translate>
    </p>
  </div>
</template>

<script>
import cloneDeep from 'lodash/cloneDeep'
import { mapState, mapMutations } from 'vuex'

export default {
  computed: {
    ...mapState({
      statements: (state) => state.portfolio.problemStatements,
    }),
  },

  methods: {
    ...mapMutations({
      setStatements: 'portfolio/SET_STATEMENTS',
    }),
    handleAddStatement() {
      this.setStatements([...this.statements, { name: '', description: '' }])
    },
    handleRemoveStatement(idx) {
      const outputArray = []
      for (let i = 0; i < this.statements.length; i++) {
        if (idx !== i) {
          outputArray.push(this.statements[i])
        }
      }
      this.setStatements(outputArray)
    },
    handleInput(val, key, idx) {
      const resultArr = cloneDeep(this.statements)
      resultArr[idx][key] = val
      this.setStatements(resultArr)
    },
  },
}
</script>

<style lang="less" scoped>
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

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
    padding: 30px 60px 20px 30px;
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
