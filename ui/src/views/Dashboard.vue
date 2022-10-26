<template>
  <div>
    <h2>{{$t('dashboard.title')}}</h2>

  
  

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
      <!-- warning -->
    <div class="alert alert-warning" v-if="uiLoaded && !firewallInstalled">
      <span class="pficon pficon-warning-triangle-o"></span>
      {{$t('dashboard.firewall_not_installed')}}
    </div>

    <div v-if="uiLoaded && firewallInstalled">
                <div class="page-description">
          <span
            v-html="
              $t('dashboard.description')
            "
          ></span>
        </div>

        <!-- save button -->
        <div class="form-group">
          <label class="col-sm-3 control-label">
          </label>
          <div class="col-sm-4">
            <button 
              :disabled="!firewallInstalled"
              class="btn btn-primary" 
              type="submit"
            >
              {{$t('save')}}
            </button>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  mounted() {
    this.getConfig()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
    }
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error)
      this.errorMessage = errorMessage;
    },
    closeErrorMessage() {
      this.errorMessage = null;
    },
    getConfig() {
      var ctx = this;
      nethserver.exec(
        ["nethserver-firewall-migration/dashboard/read"],
        {"action": "status"},
        null,
        function(success) {
          success = JSON.parse(success);
          ctx.firewallInstalled = success.firewallInstalled;
          ctx.uiLoaded = true;
 
        },
        function(error) {
          ctx.showErrorMessage(ctx.$i18n.t("dashboard.error_reading_status"), error)
        }
      );
    },
    saveConfiguration() {
      this.saving = true
      this.errorMessage = null
    
    },
    configurationValidationSuccess(configValidate) {
      this.uiLoaded = false
      nethserver.notifications.success = this.$i18n.t("dashboard.configuration_update_successful");
      nethserver.notifications.error = this.$i18n.t("settings.configuration_update_failed");

      var ctx = this
    }
  }
};
</script>
.page-description {
  margin-bottom: 30px;
}
<style scoped>

</style>
