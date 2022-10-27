<template>
  <div>
    <h2>{{ $t("dashboard.title") }}</h2>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <!-- warning -->
    <div class="alert alert-warning" v-if="uiLoaded && !firewallInstalled">
      <span class="pficon pficon-warning-triangle-o"></span>
      {{ $t("dashboard.firewall_not_installed") }}
    </div>

    <div v-if="uiLoaded">
      <div v-if="firewallInstalled">
        <div class="page-description">
          <span v-html="$t('dashboard.description')"></span>
        </div>
      </div>
    </div>

    <div v-if="!exported">
      <div class="fw-exporting">{{ $t("dashboard.exporting") }}</div>
      <div v-if="!exported" class="spinner spinner-lg"></div>
    </div>

    <div v-if="exported">
      <h3>{{ $t("dashboard.exported") }}</h3>
      <ul>
        <li v-for="item in done">
          {{ $t("dashboard." + item) }}
        </li>
      </ul>
    </div>

    <div v-if="exported">
      <h3>{{ $t("dashboard.skipped") }}</h3>
      <ul>
        <li v-for="(elements, key) in skipped">
          <legend class="fields-section-header-pf" aria-expanded="true">
            <span
              :class="[
                'fa fa-angle-right field-section-toggle-pf',
                show_skipped[key] ? 'fa-angle-down' : '',
              ]"
            ></span>
            <a class="field-section-toggle-pf" @click="toggleSkipped(key)"
              >{{ $t("dashboard.skipped_" + key) }} ({{
                skipped[key].length
              }})</a
            >
          </legend>
          <div v-show="show_skipped[key]">
            <ul>
              <li v-for="item in skipped[key]">
                {{ formatSkipped(key, item) }}
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  mounted() {
    this.getConfig();
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      exported: false,
      firewallInstalled: false,
      done: [],
      skipped: [],
      show_skipped: {},
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error);
      this.errorMessage = errorMessage;
    },
    closeErrorMessage() {
      this.errorMessage = null;
    },
    getConfig() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-firewall-migration/dashboard/read"],
        { action: "status" },
        null,
        function (success) {
          success = JSON.parse(success);
          ctx.firewallInstalled = success.firewallInstalled;
          ctx.uiLoaded = true;
          ctx.exportConfig();
        },
        function (error) {
          ctx.showErrorMessage(
            ctx.$i18n.t("dashboard.error_reading_status"),
            error
          );
        }
      );
    },
    exportConfig() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-firewall-migration/dashboard/read"],
        { action: "export" },
        null,
        function (success) {
          success = JSON.parse(success);
          ctx.exported = success.exported;
          ctx.done = success.done;
          ctx.uiLoaded = true;
          ctx.skipped = success.skipped;

          for (const s in ctx.skipped) {
            ctx.show_skipped[s] = false;
          }
        },
        function (error) {
          ctx.showErrorMessage(ctx.$i18n.t("dashboard.error_exporting"), error);
        }
      );
    },
    configurationValidationSuccess(configValidate) {
      this.uiLoaded = false;
      nethserver.notifications.success = this.$i18n.t(
        "dashboard.configuration_update_successful"
      );
      nethserver.notifications.error = this.$i18n.t(
        "settings.configuration_update_failed"
      );

      var ctx = this;
    },
    toggleSkipped(section) {
      this.show_skipped[section] = !this.show_skipped[section];
      this.$forceUpdate();
    },
    formatSkipped(key, item) {
      switch (key) {
        case "network":
          if (item["type"] == "alias") {
            return "Alias: " + item["key"];
          } else if (item["type"] == "bond") {
            // bridge over bond
            return (
              this.$i18n.t("dashboard.bridge") +
              " " +
              item["bridge"] +
              " " +
              this.$i18n.t("dashboard.over_bond") +
              " " +
              item["key"]
            );
          } else {
            return item;
          }
        case "rules":
          if (item["Action"].startsWith("class;")) {
            return (
              this.$i18n.t("dashboard.qos") +
              " - " +
              this.$i18n.t("dashboard.source") +
              ": " +
              item["Src"] +
              " " +
              this.$i18n.t("dashboard.destination") +
              ": " +
              item["Dst"] +
              " " +
              this.$i18n.t("dashboard.class") +
              ": " +
              item["Action"].replace("class;", "")
            );
          } else if (item["Service"].startsWith("ndpi;")) {
            return (
              this.$i18n.t("dashboard.dpi") +
              " - " +
              this.$i18n.t("dashboard.source") +
              ": " +
              item["Src"] +
              " " +
              this.$i18n.t("dashboard.destination") +
              ": " +
              item["Dst"] +
              " " +
              this.$i18n.t("dashboard.service") +
              ": " +
              item["Service"].replace("ndpi;", "")
            );
          } else {
            return itme;
          }
        default:
          return item;
      }
    },
  },
};
</script>

<style scoped>
.page-description {
  margin-bottom: 30px;
}
.fw-exporting {
  margin-top: 30px;
  font-size: 120%;
}
</style>
