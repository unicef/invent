<template>
  <div class="LandingInitiativesTable">
    <el-table :data="tableData" :highlight-current-row="false">
      <el-table-column v-for="column in columns" :label="column" :prop="column" :key="column">
        <template slot-scope="scope">
          <!-- <draggable :list="tableData[0][column]"> -->
          <nuxt-link
            :to="
              localePath({
                name: 'organisation-initiatives-id-published',
                params: { ...$route.params, id: card.id },
              })
            "
            v-for="card in scope.row[column]"
            :key="card.name"
            :class="card.stale ? 'link-card stale' : 'link-card'"
          >
            <div class="list-group-card">
              <div class="icon-div">
                <i class="el-icon-time"></i>
              </div>
              <div class="list-group-card-data">
                <p class="initiative-office">{{ card.unicefOffice }}</p>
                <p class="initiative-name">{{ card.name }}</p>
                <p class="initiative-date">{{ `${$gettext('Since')} ${card.lastUpdated}` }}</p>
              </div>
            </div>
          </nuxt-link>
          <!-- </draggable> -->
        </template>
      </el-table-column>
    </el-table>
    <!-- <div class="LandingInitiativesTable">
      <el-row>
        <el-col v-for="column in columns" :key="column" class="initiatives-phase-col">
          <draggable class="list-group" :list="tableData[column]" group="people">
            <div class="header">
              {{ column }}
            </div>
            <div class="list-group-card" v-for="(element, index) in tableData[column]" :key="element.name">
              <div class="">
                <i class="el-icon-time"></i>
              </div>
              <p>{{ element.name }}</p>
              <p>{{ element.lastUpdated }}</p>
            </div>
          </draggable>
        </el-col>
      </el-row>
    </div> -->
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable,
  },
  data() {
    return {
      columns: ['col1', 'col2', 'col3', 'col4', 'col5', 'col6'],
      tableData: [
        {
          col1: [
            {
              name: 'test initiative af a dfalsdjaf qwerq tqtfaiopuiop afapoiuqwer ergc',
              lastUpdated: '01/01/2022',
              unicefOffice: 'Jakarda',
              id: 3310,
              stale: true,
            },
            {
              name: 'test initiative2 af a dfalsdjaf qwerq tqtfaiopuiop afapoiuqwer ergc',
              lastUpdated: '01/01/2022',
              unicefOffice: 'Jakarda2',
              id: 3310,
              stale: false,
            },
          ],
          col2: [
            {
              name: 'test initiative1 col2  af a dfalsdjaf qwerq tqtfaiopuiop afapoiuqwer ergc',
              lastUpdated: '01/01/2022',
              unicefOffice: 'Jakarda2',
              id: 3310,
              stale: true,
            },
          ],
          col3: [],
          col4: [],
          col5: [],
          col6: [],
        },
      ],
    }
  },
}
</script>

<!-- <style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';

.LandingInitiativesTable {
  padding: 10px 0;
  .el-row {
    background-color: #aedcf7;
    border: solid 2px @colorBrandPrimary;

    .header {
      background-color: @colorBrandPrimaryLight;
      margin: 0;
      padding: 8px 6px;
    }

    .initiatives-phase-col {
      max-width: 240px;
      border-right: dashed 2px @colorBrandPrimary;
      height: inherit;

      .list-group-card {
        border: solid 1px gray;
        border-radius: 2px;
        width: 200px;
        border-top-color: blue;
        border-top-width: 6px;
        background-color: rgb(219, 217, 215);
        margin: 4px;
      }
    }
  }
}
</style> -->

<style lang="less">
@import '~assets/style/variables.less';
@import '~assets/style/mixins.less';
.LandingInitiativesTable {
  margin: 10px 0;

  .el-table--enable-row-hover .el-table__body tr:hover > td {
    background-color: unset;
  }

  .el-table {
    border: solid @colorBrandPrimary 2px;
    max-height: 600px;
    overflow-y: auto;
    overflow-x: auto;

    td {
      border-left: dashed @colorBrandPrimary 2px;
    }
    td:first-child {
      border-left: none;
    }
  }
  .el-table__row {
    background-color: #f5fafc;

    > td {
      vertical-align: top;
    }
  }

  th {
    background-color: @colorBrandPrimary;
    > .cell {
      font-size: @fontSizeSmall;
      color: @colorWhite;
      font-weight: bold;
      letter-spacing: 0;
      line-height: 29px;
      white-space: nowrap;
    }

    &.is-leaf {
      border-bottom-color: @colorWhite;
    }
  }

  .link-card {
    text-decoration: none;
    margin: auto;

    .list-group-card {
      border: solid 1px #d0dadf;
      box-shadow: 0px 2px 1px 0px rgba(194, 204, 210, 1);
      margin: 18px 0;
      border-top-color: @colorBrandPrimary;
      border-top-width: 5px;
      border-radius: 2px;
      background-color: #ffffff;

      .list-group-card-data {
        padding: 4px;
      }
      .icon-div {
        width: inherit;
        z-index: 10;
        position: fixed;

        .el-icon-time {
          display: none;
        }
      }

      .initiative-name {
        padding: 0;
        margin: 0;
        display: -webkit-box;
        max-width: inherit;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      .initiative-date {
        padding: 0;
        margin: 0;

        color: #909496;
      }

      .initiative-office {
        padding: 0;
        margin: 0;

        color: #22ace2;
      }
    }
    &.stale {
      .list-group-card {
        border-top-color: #fe8900;
        .icon-div {
          .el-icon-time {
            display: block;
            font-size: 20px;
            background-color: #fe8900;
            border-radius: 0 0 2px 2px;
            box-shadow: 0px 1px 1px 0px rgba(194, 204, 210, 1);
            padding: 2px;
            color: white;
            position: relative;
            top: -2px;
            left: 150px;
          }
        }
        .initiative-office {
          color: #fe8900;
        }
        .initiative-date {
          color: #fe8900;
        }
      }
    }
  }
}
</style>
