<!--
  Copyright (C) 2023 Nethesis S.r.l.
  Copyright (C) 2026 Genius Dynamics
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("settings.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.getConfiguration">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.get-configuration')"
          :description="error.getConfiguration"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <cv-tile light>
          <cv-form @submit.prevent="configureModule">
            <NsTextInput
              :label="$t('settings.host')"
              :helper-text="$t('settings.host_helper')"
              placeholder="vault.example.org"
              v-model.trim="host"
              class="mg-bottom"
              :invalid-message="$t(error.host)"
              :disabled="isFormDisabled"
              ref="host"
            />
            <NsToggle
              value="letsEncrypt"
              :label="$t('settings.lets_encrypt')"
              v-model="isLetsEncryptEnabled"
              :disabled="isFormDisabled"
              class="mg-bottom"
            >
              <template slot="text-left">{{
                $t("settings.disabled")
              }}</template>
              <template slot="text-right">{{
                $t("settings.enabled")
              }}</template>
            </NsToggle>
            <NsToggle
              value="httpToHttps"
              :label="$t('settings.http_to_https')"
              v-model="isHttpToHttpsEnabled"
              :disabled="isFormDisabled"
              class="mg-bottom"
            >
              <template slot="text-left">{{
                $t("settings.disabled")
              }}</template>
              <template slot="text-right">{{
                $t("settings.enabled")
              }}</template>
            </NsToggle>
            <cv-radio-group
              :legend="$t('settings.unseal_mode')"
              vertical
              class="mg-bottom"
              ref="unseal_mode"
            >
              <cv-radio-button
                :label="$t('settings.unseal_mode_manual')"
                value="manual"
                v-model="unsealMode"
                :disabled="isFormDisabled || isUnsealModeLocked"
              />
              <p class="radio-description">
                {{ $t("settings.unseal_mode_manual_description") }}
              </p>
              <cv-radio-button
                :label="$t('settings.unseal_mode_auto')"
                value="auto"
                v-model="unsealMode"
                :disabled="isFormDisabled || isUnsealModeLocked"
              />
              <p class="radio-description">
                {{ $t("settings.unseal_mode_auto_description") }}
              </p>
            </cv-radio-group>
            <NsInlineNotification
              v-if="isUnsealModeLocked"
              kind="info"
              :title="$t('settings.unseal_mode_locked')"
              :showCloseButton="false"
              class="maxwidth"
            />
            <NsInlineNotification
              v-if="error.unseal_mode"
              kind="error"
              :title="error.unseal_mode"
              :showCloseButton="false"
              class="maxwidth"
            />
            <!-- advanced options -->
            <cv-accordion ref="accordion" class="maxwidth mg-bottom">
              <cv-accordion-item :open="isAdvancedOpen">
                <template slot="title">{{ $t("settings.advanced") }}</template>
                <template slot="content">
                  <cv-select
                    :label="$t('settings.log_level')"
                    v-model="logLevel"
                    :disabled="isFormDisabled"
                    class="mg-bottom"
                    ref="log_level"
                  >
                    <cv-select-option
                      v-for="level in logLevels"
                      :key="level"
                      :value="level"
                      >{{ $t("settings.log_level_" + level) }}</cv-select-option
                    >
                  </cv-select>
                  <NsToggle
                    value="auditLog"
                    :label="$t('settings.audit_log')"
                    v-model="isAuditLogEnabled"
                    :disabled="isFormDisabled"
                  >
                    <template slot="tooltip">{{
                      $t("settings.audit_log_helper")
                    }}</template>
                    <template slot="text-left">{{
                      $t("settings.disabled")
                    }}</template>
                    <template slot="text-right">{{
                      $t("settings.enabled")
                    }}</template>
                  </NsToggle>
                </template>
              </cv-accordion-item>
            </cv-accordion>
            <NsInlineNotification
              v-if="isRestartRequired"
              kind="warning"
              :title="$t('settings.restart_warning_title')"
              :description="$t('settings.restart_warning_description')"
              :showCloseButton="false"
              class="maxwidth"
            />
            <NsInlineNotification
              v-if="error.configureModule"
              kind="error"
              :title="$t('action.configure-module')"
              :description="error.configureModule"
              :showCloseButton="false"
              class="maxwidth"
            />
            <NsButton
              kind="primary"
              :icon="Save20"
              :loading="loading.configureModule"
              :disabled="isFormDisabled"
              >{{ $t("settings.save") }}</NsButton
            >
          </cv-form>
        </cv-tile>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script>
import to from "await-to-js";
import { mapState } from "vuex";
import {
  QueryParamService,
  UtilService,
  TaskService,
  IconService,
  PageTitleService,
} from "@nethserver/ns8-ui-lib";

export default {
  name: "Settings",
  mixins: [
    TaskService,
    IconService,
    UtilService,
    QueryParamService,
    PageTitleService,
  ],
  pageTitle() {
    return this.$t("settings.title") + " - " + this.appName;
  },
  data() {
    return {
      q: {
        page: "settings",
      },
      urlCheckInterval: null,
      logLevels: ["trace", "debug", "info", "warn", "error"],
      host: "",
      isLetsEncryptEnabled: false,
      isHttpToHttpsEnabled: true,
      unsealMode: "manual",
      logLevel: "info",
      isAuditLogEnabled: false,
      isAdvancedOpen: false,
      savedConfig: null,
      openbaoStatus: null,
      loading: {
        getConfiguration: false,
        getOpenbaoStatus: false,
        configureModule: false,
      },
      error: {
        getConfiguration: "",
        configureModule: "",
        host: "",
        lets_encrypt: "",
        http2https: "",
        unseal_mode: "",
        log_level: "",
        audit_log: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core", "appName"]),
    isFormDisabled() {
      return (
        this.loading.getConfiguration ||
        this.loading.getOpenbaoStatus ||
        this.loading.configureModule
      );
    },
    isUnsealModeLocked() {
      // The seal type is stored by OpenBao at initialization time
      return !!(this.openbaoStatus && this.openbaoStatus.initialized);
    },
    isRestartRequired() {
      if (!this.savedConfig || !this.savedConfig.host) {
        return false;
      }
      return (
        this.host !== this.savedConfig.host ||
        this.unsealMode !== this.savedConfig.unseal_mode
      );
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.watchQueryData(vm);
      vm.urlCheckInterval = vm.initUrlBindingForApp(vm, vm.q.page);
    });
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.urlCheckInterval);
    next();
  },
  created() {
    this.getConfiguration();
    this.getOpenbaoStatus();
  },
  methods: {
    async getConfiguration() {
      this.loading.getConfiguration = true;
      this.error.getConfiguration = "";
      const taskAction = "get-configuration";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.getConfigurationAborted
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.getConfigurationCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.getConfiguration = this.getErrorMessage(err);
        this.loading.getConfiguration = false;
        return;
      }
    },
    getConfigurationAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.getConfiguration = this.$t("error.generic_error");
      this.loading.getConfiguration = false;
    },
    getConfigurationCompleted(taskContext, taskResult) {
      const config = taskResult.output;
      this.savedConfig = config;
      this.host = config.host;
      this.isLetsEncryptEnabled = config.lets_encrypt;
      // new instances default to HTTPS redirection
      this.isHttpToHttpsEnabled = config.host ? config.http2https : true;
      this.unsealMode = config.unseal_mode;
      this.logLevel = config.log_level;
      this.isAuditLogEnabled = config.audit_log;
      this.loading.getConfiguration = false;
      this.focusElement("host");
    },
    async getOpenbaoStatus() {
      this.loading.getOpenbaoStatus = true;
      const taskAction = "get-openbao-status";
      const eventId = this.getUuid();

      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.getOpenbaoStatusAborted
      );
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.getOpenbaoStatusCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        // not blocking: the backend validates the unseal mode anyway
        console.error(`error creating task ${taskAction}`, err);
        this.loading.getOpenbaoStatus = false;
      }
    },
    getOpenbaoStatusAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.loading.getOpenbaoStatus = false;
    },
    getOpenbaoStatusCompleted(taskContext, taskResult) {
      this.openbaoStatus = taskResult.output;
      this.loading.getOpenbaoStatus = false;
    },
    validateConfigureModule() {
      this.clearErrors(this);

      let isValidationOk = true;
      if (!this.host) {
        this.error.host = "common.required";

        if (isValidationOk) {
          this.focusElement("host");
        }
        isValidationOk = false;
      }
      return isValidationOk;
    },
    configureModuleValidationFailed(validationErrors) {
      this.loading.configureModule = false;
      let focusAlreadySet = false;

      for (const validationError of validationErrors) {
        const param = validationError.parameter;

        if (param === "(root)") {
          continue;
        }
        // set i18n error message
        this.error[param] = this.$t("settings." + validationError.error);

        if (["log_level", "audit_log"].includes(param)) {
          this.isAdvancedOpen = true;
        }

        if (!focusAlreadySet) {
          this.focusElement(param);
          focusAlreadySet = true;
        }
      }
    },
    async configureModule() {
      const isValidationOk = this.validateConfigureModule();
      if (!isValidationOk) {
        return;
      }

      this.loading.configureModule = true;
      const taskAction = "configure-module";
      const eventId = this.getUuid();

      // register to task error
      this.core.$root.$once(
        `${taskAction}-aborted-${eventId}`,
        this.configureModuleAborted
      );

      // register to task validation
      this.core.$root.$once(
        `${taskAction}-validation-failed-${eventId}`,
        this.configureModuleValidationFailed
      );

      // register to task completion
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        this.configureModuleCompleted
      );

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: {
            host: this.host,
            lets_encrypt: this.isLetsEncryptEnabled,
            http2https: this.isHttpToHttpsEnabled,
            unseal_mode: this.unsealMode,
            log_level: this.logLevel,
            audit_log: this.isAuditLogEnabled,
          },
          extra: {
            title: this.$t("settings.configure_instance", {
              instance: this.instanceName,
            }),
            description: this.$t("settings.configuring"),
            eventId,
          },
        })
      );
      const err = res[0];

      if (err) {
        console.error(`error creating task ${taskAction}`, err);
        this.error.configureModule = this.getErrorMessage(err);
        this.loading.configureModule = false;
        return;
      }
    },
    configureModuleAborted(taskResult, taskContext) {
      console.error(`${taskContext.action} aborted`, taskResult);
      this.error.configureModule = this.$t("error.generic_error");
      this.loading.configureModule = false;
    },
    configureModuleCompleted() {
      this.loading.configureModule = false;

      // reload configuration and server state
      this.getConfiguration();
      this.getOpenbaoStatus();
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";

.mg-bottom {
  margin-bottom: $spacing-06;
}

.maxwidth {
  max-width: 38rem;
}

.radio-description {
  max-width: 38rem;
  margin: 0 0 $spacing-05 $spacing-07;
  color: $text-02;
}
</style>
