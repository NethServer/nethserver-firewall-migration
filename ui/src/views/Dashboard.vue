<template>
  <div>
    <h2>{{ $t("dashboard.title") }}</h2>

    <div
      class="modal"
      id="downloadModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
      data-keyboard="false"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">
              {{ $t("dashboard.download_usb_image") }}
            </h4>
          </div>

          <div class="fw-migration" v-if="migrating">
            <div class="fw-migration">
              {{ $t("dashboard.preparing_image") }}
              <div v-show="!hideSpinner" class="spinner spinner-sm"></div>
            </div>
          </div>
          <div class="fw-migration" v-if="migrating">
            <pre>{{ output }}</pre>
          </div>
          <form
            v-if="!migrating"
            class="form-horizontal"
            v-on:submit.prevent=""
          ></form>
        </div>
      </div>
    </div>

    <div
      class="modal"
      id="migrateModal"
      tabindex="-1"
      role="dialog"
      data-backdrop="static"
      data-keyboard="false"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">{{ $t("dashboard.in_place_migrate") }}</h4>
          </div>

          <div class="fw-migration" v-if="migrating">
            <div class="fw-migration">
              {{ $t("dashboard.migration_in_progress") }}
              <a :href="nextLink">{{ nextLink }}</a>
              <div v-show="!hideSpinner" class="spinner spinner-sm"></div>
            </div>
          </div>
          <div class="fw-migration" v-if="migrating">
            <pre>{{ output }}</pre>
          </div>
          <form
            v-if="!migrating"
            class="form-horizontal"
            v-on:submit.prevent=""
          >
            <div class="modal-body">
              <div class="alert alert-warning">
                <span class="pficon pficon-warning-triangle-o"></span>
                {{ $t("dashboard.not_reversible") }}
              </div>
              <div class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                  >{{ $t("dashboard.select_device") }}</label
                >
                <div class="col-sm-9 control-div" for="textInput-modal-markup">
                  <select
                    title="-"
                    v-model="disk"
                    class="combobox form-control"
                  >
                    <option v-for="(d, dk) in disks" v-bind:key="dk" :value="d">
                      {{ d.name }} {{ d.model ? "(" + d.model + ")" : "" }} |
                      {{ d.size | byteFormat }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-default"
                type="button"
                data-dismiss="modal"
              >
                {{ $t("cancel") }}
              </button>
              <button
                class="btn btn-danger btn-large"
                type="submit"
                :disabled="!disk"
                @click="migrate()"
              >
                {{ $t("dashboard.migrate") }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <!-- warning -->
    <div class="alert alert-warning" v-if="uiLoaded && !firewallInstalled">
      <span class="pficon pficon-warning-triangle-o"></span>
      {{ $t("dashboard.firewall_not_installed") }}
    </div>

    <div v-if="uiLoaded">
      <div v-if="firewallInstalled">
        <div class="page-description">
          <span>{{ $t("dashboard.description") }}</span>
        </div>
      </div>
    </div>

    <div v-if="!exported">
      <div class="fw-exporting">{{ $t("dashboard.exporting") }}</div>
      <div v-if="!exported" class="spinner spinner-lg"></div>
    </div>

    <div v-if="exported">
      <hr/>
      <p class="p-description">{{$t("dashboard.export_help")}}</p>
      <div class="form-group download-exported row">
        <label class="col-sm-2 control-label" for="textInput-modal-markup">{{
          $t("dashboard.download_exported")
        }}</label>
        <div class="col-sm-2 control-div" for="textInput-modal-markup">
          <a
            id="download-export-button"
            class="btn btn-default"
            ref="downloadButton"
            @click="
              downloadFile(
                '/var/lib/nethserver/firewall-migration/export.tar.gz'
              )
            "
            >{{ $t("download") }}</a
          >
        </div>
      </div>
      <hr/>
      <p class="p-description">{{$t("dashboard.usb_help")}}</p>
      <div class="form-group download-exported row">
        <label class="col-sm-2 control-label" for="textInput-modal-markup">{{
          $t("dashboard.download_usb_image")
        }}</label>
        <div class="col-sm-2 control-div" for="textInput-modal-markup">
          <a
            id="download-export-button"
            class="btn btn-default"
            @click="openDownloadModal()"
            >{{ $t("download") }}</a
          >
        </div>
      </div>
      <hr/>
      <p class="p-description">{{$t("dashboard.migrate_help")}}</p>
      <div class="form-group download-exported row">
        <label class="col-sm-2 control-label" for="textInput-modal-markup">{{
          $t("dashboard.in_place_migrate")
        }}</label>
        <div class="col-sm-2 control-div" for="textInput-modal-markup">
          <a
            id="migrate-export-button"
            class="btn btn-primary"
            @click="openMigrateModal()"
            >{{ $t("dashboard.migrate") }}</a
          >
        </div>
      </div>
      <div class="row"></div>
    </div>

    <hr v-if="exported"/>
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
      disk: "",
      disks: [],
      migrating: false,
      output: "",
      nextLink: "https://" + window.location.host.split(":")[0],
      hideSpinner: false,
      imageReady: false,
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
          ctx.disks = success.disks;

          for (const s in ctx.skipped) {
            ctx.show_skipped[s] = false;
          }
        },
        function (error) {
          ctx.showErrorMessage(ctx.$i18n.t("dashboard.error_exporting"), error);
        }
      );
    },
    prepareImageDownload() {
      var ctx = this;
      nethserver.execRaw(
        ["nethserver-firewall-migration/dashboard/execute"],
        {},
        function (stream) {
          ctx.migrating = true;
          ctx.output = ctx.output + stream;
        },
        function (success) {
          ctx.migrating = false;
          ctx.output = "";
          ctx.imageReady = true;
          ctx.downloadFile(
            "/usr/share/nethserver-firewall-migration-builder/nethsecurity-custom.img.gz"
          );
          $("#downloadModal").modal("hide");
        },
        function (error) {
          console.error("Can't download image");
        }
      );
    },
    setImageDownload() {
      var ctx = this;

      nethserver.exec(
        ["nethserver-firewall-migration/dashboard/read"],
        {
          action: "download-image",
        },
        null,
        function (success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          var blob = "data:application/octet-stream;base64," + success.data;
          var encodedUri = encodeURI(blob);
          $("#download-image-button")
            .attr("download", success.filename)
            .attr("href", encodedUri);
        },
        function (error, data) {
          console.error(error, data);
        }
      );
    },
    toggleSkipped(section) {
      this.show_skipped[section] = !this.show_skipped[section];
      this.$forceUpdate();
    },
    formatTarget(target) {
      if (target.includes(";")) {
        return target.split(";")[1];
      } else {
        return target;
      }
    },
    formatSkipped(key, item) {
      switch (key) {
        case "static":
          return this.$i18n.t("dashboard." + item);
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
          var line = "";
          if (item["Action"].startsWith("class;")) {
            line =
              this.$i18n.t("dashboard.qos") +
              " - " +
              this.$i18n.t("dashboard.source") +
              ": " +
              this.formatTarget(item["Src"]) +
              " " +
              this.$i18n.t("dashboard.destination") +
              ": " +
              this.formatTarget(item["Dst"]) +
              " " +
              this.$i18n.t("dashboard.class") +
              ": " +
              item["Action"].replace("class;", "");
          } else if (item["Service"].startsWith("ndpi;")) {
            line =
              this.$i18n.t("dashboard.dpi") +
              " - " +
              this.$i18n.t("dashboard.source") +
              ": " +
              this.formatTarget(item["Src"]) +
              " " +
              this.$i18n.t("dashboard.destination") +
              ": " +
              this.formatTarget(item["Dst"]) +
              " " +
              this.$i18n.t("dashboard.service") +
              ": " +
              item["Service"].replace("ndpi;", "");
          }
          if (line) {
            line =
              line +
              " " +
              (item["Description"] ? " - " + item["Description"] : "");
            return line;
          } else {
            return item;
          }
        case "wan":
          line =
              this.$i18n.t("dashboard.divert") +
              " - " +
              this.$i18n.t("dashboard.source") +
              ": " +
              this.formatTarget(item["Src"]) +
              " " +
              this.$i18n.t("dashboard.destination") +
              ": " +
              this.formatTarget(item["Dst"]) +
              " " +
              this.$i18n.t("dashboard.provider") +
              ": " +
              item["Action"].replace("provider;", "");
          return line;
        default:
          return item;
      }
    },
    openMigrateModal() {
      $("#migrateModal").modal("show");
    },
    openDownloadModal() {
      $("#downloadModal").modal("show");
      this.prepareImageDownload();
    },
    migrate() {
      var ctx = this;
      // hide spinner after 2 minutes
      setTimeout(() => {
        ctx.hideSpinner = true;
      }, 1000 * 120);
      nethserver.execRaw(
        ["nethserver-firewall-migration/dashboard/execute"],
        { device: "/dev/" + ctx.disk.name },
        function (stream) {
          ctx.migrating = true;
          ctx.output = ctx.output + stream;
        },
        function (success) {
          //this will never be executed
        },
        function (error) {
          //this will never be executed
        }
      );
    },
    downloadFile(path) {
      const basename = path.replace(/.*\//, "");
      const query = window.btoa(
        JSON.stringify({
          payload: "fsread1",
          binary: "raw",
          path: path,
          superuser: true,
          max_read_size: 150 * 1024 * 1024,
          external: {
            "content-disposition": 'attachment; filename="' + basename + '"',
            "content-type": "application/x-xz, application/octet-stream",
          },
        })
      );
      const prefix = new URL(
        cockpit.transport.uri("channel/" + cockpit.transport.csrf_token)
      ).pathname;
      const url = prefix + "?" + query;
      return new Promise((resolve, reject) => {
        // We download via a hidden iframe to get better control over the error cases
        const iframe = document.createElement("iframe");
        iframe.setAttribute("src", url);
        iframe.setAttribute("hidden", "hidden");
        iframe.addEventListener("load", () => {
          const title = iframe.contentDocument.title;
          if (title) {
            reject(title);
          } else {
            resolve();
          }
        });
        document.body.appendChild(iframe);
      });
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
.download-exported {
  margin-bottom: 30px;
  font-size: 110%;
}
.fw-migration {
  padding: 5px;
}

.p-description {
  max-width: 1024px;
}
</style>
