<template>
  <div class="CountryAdmin">
    <div class="PageTitle">
      <h2>
        <translate :parameters="{ name: donor.name }">
          Investor admin for {name}
        </translate>
      </h2>
    </div>

    <collapsible-card
      :title="$gettext('Investor information') | translate"
      class="CountryInformation"
    >
      <el-form
        ref="countryInfo"
        :rules="rules"
        :model="{ logo, cover }"
        label-width="220px"
        label-position="left"
        @submit.native.prevent
      >
        <el-form-item
          v-if="userProfile.is_superuser"
          :label="$gettext('Choose investor') | translate"
        >
          <donor-select :value="donorId" @change="setDonorId" />
        </el-form-item>

        <el-form-item :label="$gettext('Logo')" prop="logo">
          <file-upload
            :disabled="notSDA"
            :auto-upload="false"
            :files.sync="logo"
            :limit="1"
          />
        </el-form-item>

        <el-form-item :label="$gettext('Cover image') | translate" prop="cover">
          <file-upload :disabled="notSDA" :files.sync="cover" :limit="1" />
        </el-form-item>

        <el-form-item :label="$gettext('Cover text') | translate">
          <el-input
            v-model="coverText"
            :disabled="notSDA"
            type="textarea"
            rows="5"
          />
        </el-form-item>

        <el-form-item :label="$gettext('Footer title') | translate">
          <el-input v-model="footerTitle" :disabled="notSDA" type="text" />
        </el-form-item>

        <el-form-item :label="$gettext('Footer text') | translate">
          <el-input v-model="footerText" :disabled="notSDA" type="text" />
        </el-form-item>

        <el-form-item
          :label="$gettext('Partner logos') | translate"
          prop="partnerLogos"
        >
          <file-upload
            :disabled="notSDA"
            :files.sync="partnerLogos"
            :limit="10"
          />
        </el-form-item>
      </el-form>
    </collapsible-card>

    <collapsible-card
      :title="$gettext('User management') | translate"
      class="UserManagement"
    >
      <el-row type="flex">
        <el-col class="AdminPersonaChooser">
          <div
            :class="['Persona', { active: selectedPersona === 'D' }]"
            @click="selectPersona('D')"
          >
            <div class="PersonaName">
              <translate>Viewers</translate>
            </div>
            <div class="RequestCount">
              <translate
                :parameters="{ num: userSelection.length - users.length }"
              >
                {num} new request(s)
              </translate>
            </div>
          </div>
          <!-- <div
            :class="['Persona', { 'active': selectedPersona === 'DA'}]"
            @click="selectPersona('DA')"
          >
            <div class="PersonaName">
              <translate>Investor Admins</translate>
            </div>
            <div class="RequestCount">
              <translate :parameters="{num: adminSelection.length - admins.length}">
                {num} new request(s)
              </translate>
            </div>
          </div> -->
          <div
            :class="['Persona', { active: selectedPersona === 'SDA' }]"
            @click="selectPersona('SDA')"
          >
            <div class="PersonaName">
              <translate>System Admins</translate>
            </div>
            <div class="RequestCount">
              <translate
                :parameters="{
                  num: superadminSelection.length - superAdmins.length
                }"
              >
                {num} new request(s)
              </translate>
            </div>
          </div>
        </el-col>

        <el-col class="UserTransfers">
          <div v-if="selectedPersona === 'D'" class="PersonaPrivileges">
            <el-collapse accordion>
              <el-collapse-item>
                <template slot="title">
                  <fa icon="info-circle" />
                  <translate>Privileges for Investor Users</translate>
                </template>
                <div>
                  <ul>
                    <li>
                      <translate key="d-list-item-1">
                        Can read/export responses to private investor questions
                      </translate>
                    </li>
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
          <el-transfer
            v-if="selectedPersona === 'D'"
            v-model="users"
            :titles="transferTitles"
            :data="userSelection"
            :filter-placeholder="
              $gettext('Type to filter users...') | translate
            "
            filterable
          />

          <div v-if="selectedPersona === 'DA'" class="PersonaPrivileges">
            <el-collapse accordion>
              <el-collapse-item>
                <template slot="title">
                  <fa icon="info-circle" />
                  <translate>Privileges for Investor Admins</translate>
                </template>
                <div>
                  <ul>
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
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
          <el-transfer
            v-if="selectedPersona === 'DA'"
            v-model="admins"
            :titles="transferTitles"
            :data="adminSelection"
            :filter-placeholder="
              $gettext('Type to filter users...') | translate
            "
            filterable
          />

          <div v-if="selectedPersona === 'SDA'" class="PersonaPrivileges">
            <el-collapse accordion>
              <el-collapse-item>
                <template slot="title">
                  <fa icon="info-circle" />
                  <translate>Privileges for Investor System Admins</translate>
                </template>
                <div>
                  <ul>
                    <li>
                      <translate key="sda-list-item-1">
                        Can read/export responses to private investor-specific
                        questions
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
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
          <el-transfer
            v-if="selectedPersona === 'SDA'"
            v-model="superAdmins"
            :titles="transferTitles"
            :data="superadminSelection"
            :filter-placeholder="
              $gettext('Type to filter users...') | translate
            "
            filterable
          />
        </el-col>
      </el-row>
    </collapsible-card>

    <collapsible-card
      :title="$gettext('Investor specific questionaire') | translate"
      class="Questionnaire"
    >
      <dha-questionaire ref="customQuestions" />
    </collapsible-card>

    <div class="AdminActionBarBottom">
      <el-row type="flex" justify="space-between">
        <el-button type="text" class="CancelButton IconLeft">
          <fa icon="reply" />
          <translate>Dismiss changes</translate>
        </el-button>
        <el-button type="primary" size="medium" @click="save">
          <translate>Save changes</translate>
        </el-button>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import CollapsibleCard from "../project/CollapsibleCard";
import DhaQuestionaire from "../admin/DhaQuestionaire";
import FileUpload from "../common/FileUpload";
import DonorSelect from "../common/DonorSelect";
import { mapGettersActions } from "../../utilities/form";

export default {
  name: "CountryAdministrator",

  components: {
    CollapsibleCard,
    DhaQuestionaire,
    FileUpload,
    DonorSelect
  },

  data() {
    return {
      selectedPersona: "D",
      logoError: "",
      coverError: "",
      flagForKeepingPartnerLogosError: false,
      partnerLogosError: "",
      rules: {
        logo: [
          {
            validator: (rule, value, callback) => {
              if (this.logoError) {
                callback(new Error(this.logoError));
              } else {
                callback();
              }
            }
          }
        ],
        cover: [
          {
            validator: (rule, value, callback) => {
              if (this.coverError) {
                callback(new Error(this.coverError));
              } else {
                callback();
              }
            }
          }
        ],
        partnerLogos: [
          {
            validator: (rule, value, callback) => {
              if (this.partnerLogosError) {
                callback(new Error(this.partnerLogosError));
              } else {
                callback();
              }
            }
          }
        ]
      }
    };
  },

  computed: {
    ...mapGettersActions({
      coverText: ["admin/donor", "getCoverText", "setCoverText"],
      footerTitle: ["admin/donor", "getFooterTitle", "setFooterTitle"],
      footerText: ["admin/donor", "getFooterText", "setFooterText"]
    }),

    ...mapGetters({
      donor: "admin/donor/getData",
      userSelection: "admin/donor/getUserSelection",
      adminSelection: "admin/donor/getAdminSelection",
      superadminSelection: "admin/donor/getSuperadminSelection",
      userProfile: "user/getProfile"
    }),

    notSDA() {
      return (
        this.userProfile.account_type === "DA" && !this.userProfile.is_superuser
      );
    },

    logo: {
      get() {
        if (typeof this.donor.logo === "string") {
          return [
            {
              url: this.donor.logo,
              name: ("" + this.donor.logo).split("/").pop()
            }
          ];
        } else if (!this.donor.logo) {
          return [];
        } else {
          return [this.donor.logo];
        }
      },
      set([value]) {
        this.setDataField({ field: "logo", data: value });
      }
    },

    cover: {
      get() {
        if (typeof this.donor.cover === "string") {
          return [
            {
              url: this.donor.cover,
              name: ("" + this.donor.cover).split("/").pop()
            }
          ];
        } else if (!this.donor.cover) {
          return [];
        } else {
          return [this.donor.cover];
        }
      },
      set([value]) {
        this.setDataField({ field: "cover", data: value });
      }
    },

    partnerLogos: {
      get() {
        return this.donor.partner_logos.map(rawLogo => {
          if (rawLogo.raw || rawLogo.uid) {
            return rawLogo;
          } else if (rawLogo.image) {
            return {
              url: rawLogo.image,
              name: ("" + rawLogo.image).split("/").pop(),
              id: rawLogo.id
            };
          }
        });
      },
      set(value) {
        this.setDataField({ field: "partner_logos", data: value });
      }
    },

    users: {
      get() {
        return this.donor.users || [];
      },
      set(value) {
        this.setDataField({ field: "users", data: value });
      }
    },

    admins: {
      get() {
        return this.donor.admins || [];
      },
      set(value) {
        this.setDataField({ field: "admins", data: value });
      }
    },

    superAdmins: {
      get() {
        return this.donor.super_admins || [];
      },
      set(value) {
        this.setDataField({ field: "super_admins", data: value });
      }
    },

    donorId: {
      get() {
        return this.donor.id || this.userProfile.donor;
      },
      async set(value) {
        this.setId(value);
        await this.fetchData();
      }
    },
    transferTitles() {
      return [this.$gettext("New requests"), this.$gettext("Approved")];
    }
  },

  watch: {
    logo(newArr, oldArr) {
      // Handles error message placing for wrong image formats
      if (!newArr.length) {
        return;
      }

      const filteredArray = [
        ...this.logo.filter(image => {
          return (
            !image.raw ||
            (image.raw && image.raw.name.endsWith(".jpg")) ||
            (image.raw && image.raw.name.endsWith(".jpeg")) ||
            (image.raw && image.raw.name.endsWith(".png"))
          );
        })
      ];

      if (newArr.length !== filteredArray.length) {
        this.logo = filteredArray;
        this.logoError =
          "Wrong image format, you can only upload .jpg and .png files";
      } else {
        this.logoError = "";
      }
      this.$refs.countryInfo.validate(() => {});
    },

    cover(newArr, oldArr) {
      // Handles error message placing for wrong image formats
      if (!newArr.length) {
        return;
      }

      const filteredArray = [
        ...this.cover.filter(image => {
          return (
            !image.raw ||
            (image.raw && image.raw.name.endsWith(".jpg")) ||
            (image.raw && image.raw.name.endsWith(".jpeg")) ||
            (image.raw && image.raw.name.endsWith(".png"))
          );
        })
      ];

      if (newArr.length !== filteredArray.length) {
        this.cover = filteredArray;
        this.coverError =
          "Wrong image format, you can only upload .jpg and .png files";
      } else {
        this.coverError = "";
      }
      this.$refs.countryInfo.validate(() => {});
    },

    partnerLogos(newArr, oldArr) {
      // Handles error message placing for wrong image formats
      const filteredArray = [
        ...this.partnerLogos.filter(image => {
          return (
            !image.raw ||
            (image.raw && image.raw.name.endsWith(".jpg")) ||
            (image.raw && image.raw.name.endsWith(".jpeg")) ||
            (image.raw && image.raw.name.endsWith(".png"))
          );
        })
      ];

      if (newArr.length !== filteredArray.length) {
        this.partnerLogos = filteredArray;
        this.partnerLogosError =
          "Wrong image format, you can only upload .jpg and .png files";
        this.flagForKeepingPartnerLogosError = true;
      } else if (this.flagForKeepingPartnerLogosError) {
        this.flagForKeepingPartnerLogosError = false;
        return;
      } else {
        this.partnerLogosError = "";
      }
      this.$refs.countryInfo.validate(() => {});
    }
  },

  methods: {
    ...mapActions({
      setDataField: "admin/donor/setDataField",
      saveChanges: "admin/donor/saveChanges",
      setId: "admin/donor/setId",
      fetchData: "admin/donor/fetchData"
    }),

    selectPersona(selected) {
      this.selectedPersona = selected;
    },

    setDonorId(value) {
      this.donorId = value;
    },
    save() {
      if (this.$refs.customQuestions.allSaved) {
        this.saveChanges();
      } else {
        this.$alert("Your questionnaire is not completely saved", "Warning", {
          confirmButtonText: "Ok"
        });
      }
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.CountryAdmin {
  margin-bottom: 60px;

  .CollapsibleCard {
    width: @cardSizeMedium;
    margin: 0 auto 20px;
  }

  .CountryInformation {
    .ContentContainer {
      padding: 40px;
    }

    .el-checkbox {
      line-height: 40px;
    }

    .DonorSelector {
      width: 50%;
    }
  }

  .UserManagement {
    .ContentContainer {
      padding: 0;
    }

    .AdminPersonaChooser {
      width: 200px;
      border-right: 2px solid @colorGrayLighter;

      .Persona {
        position: relative;
        display: block;
        padding: 16px 20px;
        border-bottom: 1px solid @colorGrayLighter;
        cursor: pointer;
        transition: @transitionAll;

        .PersonaName {
          color: @colorTextSecondary;
          font-size: @fontSizeBase;
          line-height: 16px;
          margin-bottom: 8px;
        }

        .RequestCount {
          color: @colorTextMuted;
          font-size: @fontSizeSmall;
        }

        .svg-inline--fa {
          position: absolute;
          top: 50%;
          right: 12px;
          transform: translateY(-50%);
          height: 14px;
          opacity: 0;
          transition: @transitionAll;
        }

        &:hover {
          background-color: @colorGrayLightest;

          .PersonaName {
            color: @colorTextPrimary;
          }

          .RequestCount {
            color: @colorGray;
          }

          .svg-inline--fa {
            opacity: 0.5;
          }
        }

        &.active {
          background-color: mix(@colorWhite, @colorBrandPrimary, 90%);
          border-color: mix(@colorWhite, @colorBrandPrimary, 70%);

          .PersonaName {
            font-weight: 700;
            color: @colorBrandPrimary;
          }

          .RequestCount {
            color: @colorTextSecondary;
          }

          .svg-inline--fa {
            color: @colorBrandPrimary;
            opacity: 1;
          }
        }
      }
    }

    .UserTransfers {
      padding: 20px 40px;

      .PersonaPrivileges {
        margin: 0 0 20px;

        ul {
          margin: 0;
          padding: 0 0 0 40px;

          li {
            font-size: @fontSizeSmall;
            line-height: 18px;
            color: @colorTextSecondary;
          }
        }
      }

      .el-transfer {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        margin: 0 0 20px;
      }

      .el-transfer-panel {
        width: 100%;

        .el-transfer-panel__body {
          min-height: 250px;
          max-height: 40vh;
          overflow-y: auto;
        }

        // &:first-child {
        //   .el-transfer-panel__header {
        //     background-color: lighten(@colorDraft, 33%);
        //   }
        // }
        //
        // &:last-child {
        //   .el-transfer-panel__header {
        //     background-color: lighten(@colorPublished, 52%);
        //   }
        // }
      }

      // .el-transfer-buttons {}
    }
  }

  .Questionnaire {
    .ContentContainer {
      padding: 20px;
    }
  }

  .AdminActionBarBottom {
    box-sizing: border-box;
    min-width: @cardSizeMedium;
    max-width: @cardSizeMedium;
    margin: 40px auto;
    padding: 40px 0;
    border-top: 1px solid @colorGrayLight;
  }
}

[dir="rtl"] {
  .CountryAdmin {
    .UserManagement {
      .AdminPersonaChooser {
        border-left: 2px solid @colorGrayLighter;
        border-right: none;

        .Persona {
          .svg-inline--fa {
            left: 12px;
            right: auto;
            transform: translateY(-50%) rotate(180deg);
          }
        }
      }

      .UserTransfers {
        .PersonaPrivileges {
          .el-collapse .el-collapse-item__header .svg-inline--fa {
            margin-left: 6px;
            margin-right: 0;
          }
          ul {
            padding-left: 0;
            padding-right: 40px;
          }
        }
      }
    }
  }
}
</style>
