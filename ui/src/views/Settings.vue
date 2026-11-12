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
            <cv-text-area
              :label="$t('settings.ip_allowlist')"
              :helper-text="$t('settings.ip_allowlist_helper')"
              placeholder="192.168.1.0/24"
              v-model="ipAllowlistText"
              :invalid-message="error.ip_allowlist"
              :disabled="isFormDisabled"
              :rows="3"
              class="mg-bottom maxwidth"
              ref="ip_allowlist"
            />
            <NsInlineNotification
              v-if="ipAllowlist.length"
              kind="warning"
              :title="$t('settings.ip_allowlist_warning_title')"
              :description="$t('settings.ip_allowlist_warning_description')"
              :showCloseButton="false"
              class="maxwidth"
            />
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
              <div class="maxwidth mg-bottom" ref="ldap_group_policies">
                <p class="field-label">
                  {{ $t("settings.group_policies") }}
                </p>
                <p class="section-description">
                  {{ $t("settings.group_policies_description") }}
                </p>
                <div
                  v-for="(row, index) in groupPolicies"
                  :key="row.key"
                  class="mapping-row"
                >
                  <NsComboBox
                    v-model="row.group"
                    :options="groupOptions"
                    :title="index === 0 ? $t('settings.group') : ''"
                    :label="$t('settings.ldap_admin_group_placeholder')"
                    :acceptUserInput="true"
                    :userInputLabel="$t('settings.group_user_input')"
                    :disabled="isFormDisabled"
                    class="mapping-field"
                  />
                  <NsComboBox
                    v-model="row.policy"
                    :options="policyOptions"
                    :title="index === 0 ? $t('settings.policy') : ''"
                    :label="$t('settings.policy_placeholder')"
                    :acceptUserInput="true"
                    :userInputLabel="$t('settings.policy_user_input')"
                    :disabled="isFormDisabled"
                    class="mapping-field"
                  />
                  <cv-icon-button
                    kind="ghost"
                    size="field"
                    type="button"
                    :icon="TrashCan20"
                    :label="$t('settings.remove_group_policy')"
                    tip-position="left"
                    :disabled="isFormDisabled"
                    class="mapping-remove"
                    @click="removeGroupPolicy(index)"
                  />
                </div>
                <NsButton
                  kind="ghost"
                  size="field"
                  type="button"
                  :icon="Add20"
                  :disabled="isFormDisabled"
                  @click="addGroupPolicy"
                  >{{ $t("settings.add_group_policy") }}</NsButton
                >
                <NsInlineNotification
                  v-if="error.ldap_group_policies"
                  kind="error"
                  :title="error.ldap_group_policies"
                  :showCloseButton="false"
                />
              </div>
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
              <NsInlineNotification
                v-if="error.auto_initialize"
                kind="error"
                :title="error.auto_initialize"
                :showCloseButton="false"
                class="maxwidth"
              />
            </template>
            <!-- starter kits -->
            <h4 class="section-title">
              {{ $t("settings.section_starter_kits") }}
            </h4>
            <p class="section-description">
              {{ $t("settings.starter_kits_description") }}
            </p>
            <div
              v-for="kit in starterKitList"
              :key="kit"
              class="kit-item maxwidth"
            >
              <NsCheckbox
                :value="kit"
                v-model="starterKits"
                :label="$t('settings.kit_' + kit)"
                :disabled="isFormDisabled"
              />
              <p class="kit-description">
                {{ $t("settings.kit_" + kit + "_description") }}
              </p>
            </div>
            <div v-if="!canAutoInitialize" class="maxwidth mg-bottom">
              <p class="section-description">
                {{ $t("settings.apply_config_description") }}
              </p>
              <NsCodeSnippet
                :copyTooltip="$t('settings.copy_to_clipboard')"
                :copy-feedback="$t('settings.copied_to_clipboard')"
                :feedback-aria-label="$t('settings.copied_to_clipboard')"
                hideExpandButton
                >{{ applyConfigCommand }}</NsCodeSnippet
              >
            </div>
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
              :invalid-message="error.notify_recipients"
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
import OpenbaoConfig from "@/mixins/openbaoConfig";

export default {
  name: "Settings",
  mixins: [
    OpenbaoConfig,
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
      ipAllowlistText: "",
      groupPolicies: [],
      groupPolicyKey: 0,
      starterKits: ["kv"],
      starterKitList: ["kv", "pki", "approle"],
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
        ip_allowlist: "",
        ldap_group_policies: "",
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
    ipAllowlist() {
      return this.ipAllowlistText
        .split(/[\s,;]+/)
        .map((n) => n.trim())
        .filter((n) => n);
    },
    groupOptions() {
      return this.domainGroups.map((g) => ({ name: g, label: g, value: g }));
    },
    policyOptions() {
      const names =
        (this.savedConfig && this.savedConfig.builtin_policies) || [];
      return names.map((p) => ({
        name: p,
        label: p,
        value: p,
        description: this.$t("settings.policy_" + p.replace(/-/g, "_")),
      }));
    },
    completeGroupPolicies() {
      return this.groupPolicies
        .filter((row) => row.group && row.policy)
        .map((row) => ({ group: row.group.trim(), policy: row.policy.trim() }));
    },
    canAutoInitialize() {
      // self-initialization needs an auto-unseal mechanism and an
      // uninitialized server
      return (
        this.unsealMode === "auto" &&
        !(this.openbaoStatus && this.openbaoStatus.initialized)
      );
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
      // NsComboBox resolves a new value against its current options: set
      // the values after the options computed from savedConfig are rendered
      this.$nextTick(() => {
        this.userDomain = config.user_domain;
        this.ldapAdminGroup = config.ldap_admin_group;
        if (this.userDomain) {
          this.listDomainGroups();
        }
      });
      this.isAutoInitializeEnabled = config.auto_initialize;
      this.notifyRecipients = config.notify_recipients.join(", ");
      this.ipAllowlistText = config.ip_allowlist.join("\n");
      this.starterKits = [...config.starter_kits];
      this.groupPolicies = config.ldap_group_policies.map((m) => ({
        key: this.groupPolicyKey++,
        group: m.group,
        policy: m.policy,
      }));
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
    addGroupPolicy() {
      this.groupPolicies.push({
        key: this.groupPolicyKey++,
        group: "",
        policy: "",
      });
    },
    removeGroupPolicy(index) {
      this.groupPolicies.splice(index, 1);
    },
    onUserDomainChange() {
      this.ldapAdminGroup = "";
      this.domainGroups = [];
      if (this.userDomain) {
        this.listDomainGroups();
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
      const incomplete = this.groupPolicies.some(
        (row) => !!row.group !== !!row.policy
      );
      if (this.userDomain && incomplete) {
        this.error.ldap_group_policies = this.$t(
          "settings.group_policy_incomplete"
        );
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

        if (param.startsWith("ldap_group_policies")) {
          this.error.ldap_group_policies = this.$t(
            "settings." + validationError.error,
            { group: validationError.value }
          );
          continue;
        }
        if (param.startsWith("ip_allowlist")) {
          this.error.ip_allowlist = this.$t(
            "settings." + validationError.error,
            {
              network: validationError.value,
            }
          );
          continue;
        }
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
            ip_allowlist: this.ipAllowlist,
            ldap_group_policies: this.userDomain
              ? this.completeGroupPolicies
              : [],
            starter_kits: this.starterKits,
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

.field-label {
  font-size: 0.75rem;
  color: $text-02;
  margin-bottom: $spacing-03;
}

.mapping-row {
  display: flex;
  align-items: flex-end;
  gap: $spacing-03;
  margin-bottom: $spacing-03;
}

.mapping-field {
  flex: 1;
  min-width: 0;
}

.mapping-remove {
  flex: none;
}

.kit-item {
  margin-bottom: $spacing-03;
}

.kit-description {
  margin: 0 0 $spacing-03 $spacing-07;
  color: $text-02;
}

.radio-description {
  max-width: 38rem;
  margin: 0 0 $spacing-05 $spacing-07;
  color: $text-02;
}
</style>
