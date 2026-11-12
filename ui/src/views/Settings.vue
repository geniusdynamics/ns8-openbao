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
            <!-- web access -->
            <h4 class="section-title">{{ $t("settings.section_web") }}</h4>
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
            <!-- unseal -->
            <h4 class="section-title">{{ $t("settings.section_unseal") }}</h4>
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
            <!-- directory login -->
            <h4 class="section-title">
              {{ $t("settings.section_directory") }}
            </h4>
            <p class="section-description">
              {{ $t("settings.directory_description") }}
            </p>
            <NsComboBox
              v-model="userDomain"
              :options="userDomainOptions"
              :title="$t('settings.user_domain')"
              :label="$t('settings.user_domain_placeholder')"
              :invalid-message="$t(error.user_domain)"
              :disabled="isFormDisabled"
              :auto-filter="true"
              :auto-highlight="true"
              class="mg-bottom maxwidth"
              ref="user_domain"
              @change="onUserDomainChange"
            />
            <template v-if="userDomain">
              <NsComboBox
                v-model="ldapAdminGroup"
                :options="adminGroupOptions"
                :title="$t('settings.ldap_admin_group')"
                :label="$t('settings.ldap_admin_group_placeholder')"
                :helper-text="$t('settings.ldap_admin_group_helper')"
                :invalid-message="$t(error.ldap_admin_group)"
                :disabled="isFormDisabled || loading.listDomainGroups"
                :acceptUserInput="true"
                :userInputLabel="$t('settings.group_user_input')"
                class="mg-bottom maxwidth"
                ref="ldap_admin_group"
              />
              <template v-if="canAutoInitialize">
                <NsCheckbox
                  value="autoInitialize"
                  v-model="isAutoInitializeEnabled"
                  :label="$t('settings.auto_initialize')"
                  :disabled="isFormDisabled"
                  ref="auto_initialize"
                />
                <NsInlineNotification
                  v-if="isAutoInitializeEnabled"
                  kind="warning"
                  :title="$t('settings.auto_initialize_warning_title')"
                  :description="
                    $t('settings.auto_initialize_warning_description')
                  "
                  :showCloseButton="false"
                  class="maxwidth"
                />
              </template>
              <div v-else class="maxwidth mg-bottom">
                <p class="section-description">
                  {{ $t("settings.setup_ldap_description") }}
                </p>
                <NsCodeSnippet
                  :copyTooltip="$t('settings.copy_to_clipboard')"
                  :copy-feedback="$t('settings.copied_to_clipboard')"
                  :feedback-aria-label="$t('settings.copied_to_clipboard')"
                  hideExpandButton
                  >{{ setupLdapCommand }}</NsCodeSnippet
                >
              </div>
              <NsInlineNotification
                v-if="error.auto_initialize"
                kind="error"
                :title="error.auto_initialize"
                :showCloseButton="false"
                class="maxwidth"
              />
            </template>
            <!-- notifications -->
            <h4 class="section-title">
              {{ $t("settings.section_notifications") }}
            </h4>
            <p class="section-description">
              {{ $t("settings.notifications_description") }}
            </p>
            <NsInlineNotification
              v-if="savedConfig && !savedConfig.smarthost_enabled"
              kind="warning"
              :title="$t('settings.smarthost_disabled_title')"
              :description="$t('settings.smarthost_disabled_description')"
              :actionLabel="$t('settings.configure_smarthost')"
              @action="goToSmarthostSettings"
              :showCloseButton="false"
              class="maxwidth"
            />
            <NsTextInput
              :label="$t('settings.notify_recipients')"
              :helper-text="$t('settings.notify_recipients_helper')"
              placeholder="security@example.org, admin@example.org"
              v-model="notifyRecipients"
              :invalid-message="$t(error.notify_recipients)"
              :disabled="isFormDisabled"
              class="mg-bottom maxwidth"
              ref="notify_recipients"
            />
            <NsButton
              kind="tertiary"
              size="field"
              type="button"
              :icon="Email20"
              :loading="loading.sendTestEmail"
              :disabled="isFormDisabled || loading.sendTestEmail"
              class="mg-bottom"
              @click="sendTestEmail"
              >{{ $t("settings.send_test_email") }}</NsButton
            >
            <NsInlineNotification
              v-if="testEmailResult"
              :kind="testEmailResult.kind"
              :title="testEmailResult.title"
              :description="testEmailResult.description"
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
      userDomain: "",
      ldapAdminGroup: "",
      isAutoInitializeEnabled: false,
      domainGroups: [],
      notifyRecipients: "",
      testEmailResult: null,
      isAdvancedOpen: false,
      savedConfig: null,
      openbaoStatus: null,
      loading: {
        getConfiguration: false,
        getOpenbaoStatus: false,
        configureModule: false,
        listDomainGroups: false,
        sendTestEmail: false,
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
        user_domain: "",
        ldap_admin_group: "",
        auto_initialize: "",
        notify_recipients: "",
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
    userDomainOptions() {
      const domains = (this.savedConfig && this.savedConfig.user_domains) || [];
      const options = [
        {
          name: "",
          label: this.$t("settings.user_domain_none"),
          value: "",
        },
      ];
      for (const domain of domains) {
        options.push({
          name: domain.name,
          label:
            domain.name +
            " (" +
            this.$t("settings.schema_" + (domain.schema || "unknown")) +
            ")",
          value: domain.name,
        });
      }
      return options;
    },
    adminGroupOptions() {
      const options = this.domainGroups.map((group) => ({
        name: group,
        label: group,
        value: group,
      }));
      // keep the saved value selectable even if it is not listed
      if (
        this.ldapAdminGroup &&
        !this.domainGroups.includes(this.ldapAdminGroup)
      ) {
        options.unshift({
          name: this.ldapAdminGroup,
          label: this.ldapAdminGroup,
          value: this.ldapAdminGroup,
        });
      }
      return options;
    },
    canAutoInitialize() {
      // self-initialization needs an auto-unseal mechanism and an
      // uninitialized server
      return (
        this.unsealMode === "auto" &&
        !(this.openbaoStatus && this.openbaoStatus.initialized)
      );
    },
    setupLdapCommand() {
      return `runagent -m ${this.instanceName} openbao-setup-ldap`;
    },
    recipientList() {
      return this.notifyRecipients
        .split(/[,;\s]+/)
        .map((r) => r.trim())
        .filter((r) => r);
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
      this.userDomain = config.user_domain;
      this.ldapAdminGroup = config.ldap_admin_group;
      this.isAutoInitializeEnabled = config.auto_initialize;
      this.notifyRecipients = config.notify_recipients.join(", ");
      if (this.userDomain) {
        this.listDomainGroups();
      }
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
    onUserDomainChange() {
      this.ldapAdminGroup = "";
      this.domainGroups = [];
      if (this.userDomain) {
        this.listDomainGroups();
      }
    },
    async listDomainGroups() {
      this.loading.listDomainGroups = true;
      const taskAction = "list-domain-groups";
      const eventId = this.getUuid();
      const domain = this.userDomain;

      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.loading.listDomainGroups = false;
      });
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        (taskContext, taskResult) => {
          // ignore stale results if the domain changed meanwhile
          if (domain === this.userDomain) {
            this.domainGroups = taskResult.output.groups
              .map((g) => g.group)
              .sort();
          }
          this.loading.listDomainGroups = false;
        }
      );

      const res = await to(
        this.createClusterTaskForApp({
          action: taskAction,
          data: { domain },
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      if (res[0]) {
        // not blocking: the group name can be typed
        console.error(`error creating task ${taskAction}`, res[0]);
        this.loading.listDomainGroups = false;
      }
    },
    goToSmarthostSettings() {
      this.core.$router.push("/settings/smarthost");
    },
    isEmailValid(address) {
      return /^[^@\s,]+@[^@\s,]+\.[^@\s,]+$/.test(address);
    },
    validateRecipients() {
      const invalid = this.recipientList.filter((r) => !this.isEmailValid(r));
      if (invalid.length) {
        this.error.notify_recipients = this.$t("settings.invalid_email", {
          address: invalid[0],
        });
        this.focusElement("notify_recipients");
        return false;
      }
      return true;
    },
    async sendTestEmail() {
      this.testEmailResult = null;
      this.error.notify_recipients = "";
      if (!this.recipientList.length) {
        this.error.notify_recipients = "settings.notify_recipients_required";
        this.focusElement("notify_recipients");
        return;
      }
      if (!this.validateRecipients()) {
        return;
      }
      this.loading.sendTestEmail = true;
      const taskAction = "send-test-email";
      const eventId = this.getUuid();

      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        (taskContext, taskResult) => {
          this.loading.sendTestEmail = false;
          this.testEmailResult = {
            kind: "success",
            title: this.$t("settings.test_email_sent"),
            description: taskResult.output.recipients.join(", "),
          };
        }
      );
      this.core.$root.$once(
        `${taskAction}-validation-failed-${eventId}`,
        (validationErrors) => {
          this.loading.sendTestEmail = false;
          this.testEmailResult = {
            kind: "error",
            title: this.$t("settings.test_email_failed"),
            description: this.$t("settings." + validationErrors[0].error),
          };
        }
      );
      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.loading.sendTestEmail = false;
        this.testEmailResult = {
          kind: "error",
          title: this.$t("settings.test_email_failed"),
          description: this.$t("settings.test_email_failed_description"),
        };
      });

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: { recipients: this.recipientList },
          extra: {
            title: this.$t("action." + taskAction),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
      if (res[0]) {
        console.error(`error creating task ${taskAction}`, res[0]);
        this.loading.sendTestEmail = false;
        this.testEmailResult = {
          kind: "error",
          title: this.$t("settings.test_email_failed"),
          description: this.getErrorMessage(res[0]),
        };
      }
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
      if (this.userDomain && !this.ldapAdminGroup) {
        this.error.ldap_admin_group = "common.required";

        if (isValidationOk) {
          this.focusElement("ldap_admin_group");
        }
        isValidationOk = false;
      }
      if (isValidationOk && !this.validateRecipients()) {
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

        if (param.startsWith("notify_recipients")) {
          this.error.notify_recipients = this.$t("settings.invalid_email", {
            address: validationError.value,
          });
          continue;
        }

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
            user_domain: this.userDomain,
            ldap_admin_group: this.userDomain ? this.ldapAdminGroup : "",
            auto_initialize:
              !!this.userDomain &&
              this.canAutoInitialize &&
              this.isAutoInitializeEnabled,
            notify_recipients: this.recipientList,
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

.section-title {
  margin-top: $spacing-07;
  margin-bottom: $spacing-05;
}

.section-title:first-child {
  margin-top: 0;
}

.section-description {
  max-width: 38rem;
  margin-bottom: $spacing-05;
  color: $text-02;
}

.radio-description {
  max-width: 38rem;
  margin: 0 0 $spacing-05 $spacing-07;
  color: $text-02;
}
</style>
