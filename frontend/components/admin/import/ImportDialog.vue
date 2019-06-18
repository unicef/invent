<template>
  <el-dialog
    v-if="dialogVisible"
    :visible.sync="dialogVisible"
    title="Select"
    modal
    :top="dialogStyle.top"
    :width="dialogStyle.width"
    :custom-class="dialogStyle.className"
  >
    <el-row
      type="flex"
      class="ImportDialogWrapper"
    >
      <el-col class="OriginalData">
        <h3>
          <translate>
            Original Data
          </translate>
        </h3>
        {{ dialogData.original }}
      </el-col>
      <el-col>
        <h3 v-if="dialogData.column !== 'digitalHealthInterventions'">
          <translate>
            Edit
          </translate>
        </h3>
        <organisation-select
          v-if="dialogData.column === 'organisation'"
          v-model="dialogData.value[0]"
          :auto-save="true"
        />
        <his-bucket-selector
          v-if="dialogData.column === 'his_bucket'"
          v-model="dialogData.value"
        />
        <health-system-challenges-selector
          v-if="dialogData.column === 'hsc_challenges'"
          v-model="dialogData.value"
        />
        <health-focus-areas-selector
          v-if="dialogData.column === 'health_focus_areas'"
          v-model="dialogData.value"
        />
        <template v-if="dialogData.column === 'implementing_partners'">
          <el-select
            v-model="dialogData.value"
            class="FullWidth"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="Add a partner"
          />
        </template>
        <template v-if="dialogData.column === 'platforms'">
          <platform-selector
            v-model="dialogData.value"
            :index="0"
          />
        </template>

        <template v-if="dialogData.column === 'sub_level'">
          <el-select v-model="dialogData.value[0]">
            <el-option
              v-for="item in subLevels"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </template>

        <template v-if="dialogData.column === 'digitalHealthInterventions'">
          <digital-health-interventions-filter
            child-selection
            :selected.sync="dialogData.value"
          />
        </template>

        <template v-if="dialogData.column === 'interoperability_standards'">
          <standards-selector
            v-model="dialogData.value"
          />
        </template>

        <template v-if="dialogData.column === 'licenses'">
          <license-selector
            v-model="dialogData.value"
          />
        </template>

        <div
          v-if="dialogData.column === 'custom_field'"
          ref="custom_fields"
        >
          <el-input
            v-if="dialogData.customField.type < 3"
            v-model="dialogData.value[0]"
          />

          <el-radio-group
            v-if="dialogData.customField.type === 3"
            v-model="dialogData.value[0]"
          >
            <el-radio label="yes">
              <translate>Yes</translate>
            </el-radio>
            <el-radio label="no">
              <translate>No</translate>
            </el-radio>
          </el-radio-group>

          <template v-if="dialogData.customField.type === 4 && dialogData.customField.options">
            <el-select
              v-model="dialogData.value[0]"
              :placeholder="$gettext('Select from list') | translate"
              filterable
              popper-class="CustomFieldSelectorDropdown"
              class="CustomFieldSelector"
            >
              <el-option
                v-for="(opt, index) in dialogData.customField.options"
                :key="index"
                :value="opt"
              />
            </el-select>
          </template>
          <template v-if="dialogData.customField.type === 5 && dialogData.customField.options">
            <el-select
              v-model="dialogData.value"
              :placeholder="$gettext('Select from list') | translate"
              multiple
              filterable
              popper-class="CustomFieldSelectorDropdown"
              class="CustomFieldSelector"
            >
              <el-option
                v-for="(opt, index) in dialogData.customField.options"
                :key="index"
                :value="opt"
              />
            </el-select>
          </template>
        </div>
      </el-col>
    </el-row>
    <div
      slot="footer"
    >
      <el-button @click="dialogData = null">
        <translate>
          Cancel
        </translate>
      </el-button>

      <el-button @click="save">
        <translate>
          Save
        </translate>
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import OrganisationSelect from '@/components/common/OrganisationSelect';
import PlatformSelector from '@/components/project/PlatformSelector';
import HisBucketSelector from '@/components/project/HisBucketSelector';
import HealthSystemChallengesSelector from '@/components/project/HealthSystemChallengesSelector';
import HealthFocusAreasSelector from '@/components/project/HealthFocusAreasSelector';
import DigitalHealthInterventionsFilter from '@/components/dialogs/filters/DigitalHealthInterventionsFilter';
import StandardsSelector from '@/components/project/StandardsSelector';
import LicenseSelector from '@/components/project/LicenseSelector';

export default {
  components: {
    OrganisationSelect,
    PlatformSelector,
    HisBucketSelector,
    HealthSystemChallengesSelector,
    HealthFocusAreasSelector,
    DigitalHealthInterventionsFilter,
    StandardsSelector,
    LicenseSelector
  },
  props: {
    customFieldsLib: {
      type: Object,
      required: true
    },
    imported: {
      type: Array,
      required: true
    },
    subLevels: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      dialogData: null
    };
  },
  computed: {
    dialogVisible: {
      get () {
        return !!this.dialogData;
      },
      set () {
        this.dialogData = null;
      }
    },
    dialogStyle () {
      return {
        top: this.dialogData.column === 'digitalHealthInterventions' ? '10vh' : undefined,
        width: this.dialogData.column === 'digitalHealthInterventions' ? '90vw' : '50%',
        className: ['ImportDialog', this.dialogData.column].join(' ')
      };
    }
  },
  methods: {
    openDialog (row, key, { column, value, type }) {
      const stringified = JSON.stringify(value);
      this.dialogData = {
        row,
        key,
        column,
        value: value ? JSON.parse(stringified) : null,
        original: this.imported[row].original_data[key],
        customField: this.customFieldsLib[type]
      };
    },
    save () {
      this.$emit('update', { row: this.dialogData.row, key: this.dialogData.key, value: this.dialogData.value });
      this.dialogData = null;
    }
  }
};
</script>

<style lang="less">
  @import "~assets/style/variables.less";
  @import "~assets/style/mixins.less";

 .ImportDialog {

    .OriginalData {
      max-width: 350px;
      min-width: 350px;
    }

   &.digitalHealthInterventions{
      max-width: @appWidthMaxLimit * 0.9;
      height: 80vh;
      margin-top: 0;
      margin-bottom: 0;

      .el-dialog__body {
        padding: 0;
        height: calc(80vh - (@dialogHeaderFooterHeight*2));
      }

      .ImportDialogWrapper {

        .DigitalHealthInterventionsFilter {
          .el-col-6 {
            overflow: hidden;
            height: calc(80vh - (@dialogHeaderFooterHeight * 2));
            border-right: 1px solid @colorGrayLight;

            .SelectorDialogColumn {
              .Header {
                width: calc((90vw - @filterSelectorWidth) / 4 - 1px);
                max-width: calc(((@appWidthMaxLimit * 0.9) - 350px) / 4 - 1px);
              }

              .Main {
                .Item {
                  .el-checkbox__label {
                    font-size: @fontSizeSmall;
                    line-height: 16px;
                  }
                }
              }
            }

            &:last-child {
              border: 0;

              .SelectorDialogColumn {
                .Header {
                  width: calc((90vw - @filterSelectorWidth) / 4);
                  max-width: calc(((@appWidthMaxLimit * 0.9) - 350px) / 4);
                }
              }
            }
          }
        }
      }
   }
 }

</style>
