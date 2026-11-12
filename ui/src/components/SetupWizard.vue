<!--
  Copyright (C) 2026 Genius Dynamics
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <NsWizard
    size="default"
    :visible="visible"
    :cancelLabel="$t('wizard.cancel')"
    :previousLabel="$t('wizard.previous')"
    :nextLabel="nextLabel"
    :isLastStep="step === 'done'"
    :isPreviousShown="!['welcome', 'done'].includes(step)"
    :isPreviousDisabled="loading.configureModule"
    :isCancelShown="step !== 'done'"
    :isCancelDisabled="loading.configureModule"
    :isNextLoading="loading.configureModule"
    :isNextDisabled="isLoadingData"
    @modal-hidden="close"
    @cancel="close"
    @previousStep="previousStep"
    @nextStep="nextStep"
  >
    <template slot="title">{{ $t("wizard.title") }}</template>
    <template slot="content">
      <cv-form @submit.prevent="nextStep">
        <p v-if="stepNumber" class="step-counter">
          {{
            $t("wizard.step_of", {
              step: stepNumber,
              total: numberedSteps.length,
            })
          }}
          - {{ $t("wizard.step_" + step) }}
        </p>
        <NsInlineNotification
          v-if="error.load"
          kind="error"
          :title="$t('error.cannot_retrieve_configuration')"
          :description="error.load"
          :showCloseButton="false"
        />
        <cv-skeleton-text
          v-if="isLoadingData"
          :paragraph="true"
          :line-count="6"
        />

        <!-- welcome -->
        <template v-else-if="step === 'welcome'">
          <h4 class="mg-bottom">{{ $t("wizard.welcome_title") }}</h4>
          <p class="mg-bottom">{{ $t("wizard.welcome_description") }}</p>
          <cv-radio-group
            v-if="!isInitialized"
            :legend="$t('wizard.setup_mode')"
            vertical
            class="mg-bottom"
          >
            <cv-radio-button
              :label="$t('wizard.setup_mode_new')"
              value="new"
              v-model="setupMode"
            />
            <ul class="choice-details">
              <li>{{ $t("wizard.setup_mode_new_description") }}</li>
            </ul>
            <cv-radio-button
              :label="$t('wizard.setup_mode_join')"
              value="join"
              v-model="setupMode"
              :disabled="!haCandidateOptions.length"
            />
            <ul class="choice-details">
              <li>{{ $t("wizard.setup_mode_join_description") }}</li>
              <li v-if="!haCandidateOptions.length">
                {{ $t("settings.ha_no_candidates_description") }}
              </li>
            </ul>
          </cv-radio-group>
          <ol class="welcome-list mg-bottom">
            <li v-for="s in numberedSteps" :key="s">
              {{ $t("wizard.step_" + s) }}
            </li>
          </ol>
          <NsInlineNotification
            kind="info"
            :title="$t('wizard.advanced_title')"
            :description="$t('wizard.advanced_description')"
            :actionLabel="$t('wizard.go_to_settings')"
            @action="goToSettings"
            :showCloseButton="false"
          />
        </template>

        <!-- web access -->
        <template v-else-if="step === 'web'">
          <p class="mg-bottom">{{ $t("wizard.web_description") }}</p>
          <NsTextInput
            :label="$t('settings.host')"
            :helper-text="$t('wizard.host_helper')"
            placeholder="vault.example.org"
            v-model.trim="host"
            :invalid-message="error.host"
            class="mg-bottom"
            ref="host"
          />
          <NsToggle
            value="letsEncrypt"
            :label="$t('settings.lets_encrypt')"
            v-model="isLetsEncryptEnabled"
            class="mg-bottom"
          >
            <template slot="tooltip">{{
              $t("wizard.lets_encrypt_helper")
            }}</template>
            <template slot="text-left">{{ $t("settings.disabled") }}</template>
            <template slot="text-right">{{ $t("settings.enabled") }}</template>
          </NsToggle>
          <NsToggle
            value="httpToHttps"
            :label="$t('settings.http_to_https')"
            v-model="isHttpToHttpsEnabled"
          >
            <template slot="text-left">{{ $t("settings.disabled") }}</template>
            <template slot="text-right">{{ $t("settings.enabled") }}</template>
          </NsToggle>
        </template>

        <!-- join an existing OpenBao (high availability) -->
        <template v-else-if="step === 'join'">
          <p class="mg-bottom">{{ $t("wizard.join_description") }}</p>
          <NsComboBox
            v-model="haJoin"
            :options="haCandidateOptions"
            :title="$t('settings.ha_join')"
            :label="$t('settings.ha_join_placeholder')"
            :invalid-message="error.ha_join"
            :auto-filter="true"
            :auto-highlight="true"
            class="mg-bottom"
            ref="ha_join"
          />
          <NsInlineNotification
            v-if="selectedHaCandidate"
            kind="info"
            :title="$t('settings.ha_join_seal_title')"
            :description="
              $t('settings.ha_join_seal_' + selectedHaCandidate.unseal_mode)
            "
            :showCloseButton="false"
          />
          <template
            v-if="
              selectedHaCandidate &&
              selectedHaCandidate.unseal_mode === 'transit' &&
              savedConfig &&
              !savedConfig.transit_token_present
            "
          >
            <p class="mg-bottom">{{ $t("wizard.join_transit_token") }}</p>
            <NsCodeSnippet
              :copyTooltip="$t('settings.copy_to_clipboard')"
              :copy-feedback="$t('settings.copied_to_clipboard')"
              :feedback-aria-label="$t('settings.copied_to_clipboard')"
              hideExpandButton
              class="mg-bottom"
              >{{ transitTokenCommand }}</NsCodeSnippet
            >
          </template>
          <NsInlineNotification
            kind="warning"
            :title="$t('wizard.join_quorum_title')"
            :description="$t('wizard.join_quorum_description')"
            :showCloseButton="false"
          />
          <NsInlineNotification
            v-if="error.ha_role"
            kind="error"
            :title="error.ha_role"
            :showCloseButton="false"
          />
        </template>

        <!-- unseal mode -->
        <template v-else-if="step === 'unseal'">
          <p class="mg-bottom">{{ $t("wizard.unseal_description") }}</p>
          <NsInlineNotification
            v-if="isInitialized"
            kind="info"
            :title="$t('settings.unseal_mode_locked')"
            :showCloseButton="false"
          />
          <cv-radio-group vertical class="mg-bottom">
            <cv-radio-button
              :label="$t('settings.unseal_mode_manual')"
              value="manual"
              v-model="unsealMode"
              :disabled="isInitialized"
            />
            <ul class="choice-details">
              <li>{{ $t("wizard.manual_pro") }}</li>
              <li>{{ $t("wizard.manual_con") }}</li>
              <li>{{ $t("wizard.manual_when") }}</li>
            </ul>
            <cv-radio-button
              :label="$t('settings.unseal_mode_auto')"
              value="auto"
              v-model="unsealMode"
              :disabled="isInitialized"
            />
            <ul class="choice-details">
              <li>{{ $t("wizard.auto_pro") }}</li>
              <li>{{ $t("wizard.auto_con") }}</li>
              <li>{{ $t("wizard.auto_when") }}</li>
            </ul>
            <template
              v-if="savedConfig && savedConfig.unseal_mode === 'transit'"
            >
              <cv-radio-button
                :label="$t('settings.unseal_mode_transit')"
                value="transit"
                v-model="unsealMode"
                :disabled="isInitialized"
              />
              <ul class="choice-details">
                <li>{{ $t("wizard.transit_configured") }}</li>
              </ul>
            </template>
          </cv-radio-group>
          <NsInlineNotification
            v-if="error.unseal_mode"
            kind="error"
            :title="error.unseal_mode"
            :showCloseButton="false"
          />
        </template>

        <!-- directory login -->
        <template v-else-if="step === 'directory'">
          <p class="mg-bottom">{{ $t("wizard.directory_description") }}</p>
          <NsInlineNotification
            v-if="!hasUserDomains"
            kind="info"
            :title="$t('wizard.no_user_domains_title')"
            :description="$t('wizard.no_user_domains_description')"
            :actionLabel="$t('wizard.go_to_domains')"
            @action="goToDomainsAndUsers"
            :showCloseButton="false"
          />
          <template v-else>
            <NsToggle
              value="directoryEnabled"
              :label="$t('wizard.enable_directory_login')"
              v-model="isDirectoryEnabled"
              class="mg-bottom"
            >
              <template slot="text-left">{{
                $t("settings.disabled")
              }}</template>
              <template slot="text-right">{{
                $t("settings.enabled")
              }}</template>
            </NsToggle>
            <template v-if="isDirectoryEnabled">
              <NsComboBox
                v-model="userDomain"
                :options="domainOptions"
                :title="$t('settings.user_domain')"
                :label="$t('settings.user_domain_placeholder')"
                :invalid-message="error.user_domain"
                class="mg-bottom"
                ref="user_domain"
                @change="onUserDomainChange"
              />
              <NsComboBox
                v-if="userDomain"
                v-model="ldapAdminGroup"
                :options="adminGroupOptions"
                :title="$t('settings.ldap_admin_group')"
                :label="$t('settings.ldap_admin_group_placeholder')"
                :helper-text="$t('settings.ldap_admin_group_helper')"
                :invalid-message="error.ldap_admin_group"
                :disabled="loading.listDomainGroups"
                :acceptUserInput="true"
                :userInputLabel="$t('settings.group_user_input')"
                class="mg-bottom"
                ref="ldap_admin_group"
              />
              <template v-if="userDomain && canAutoInitialize">
                <NsCheckbox
                  value="autoInitialize"
                  v-model="isAutoInitializeEnabled"
                  :label="$t('settings.auto_initialize')"
                />
                <div v-if="isAutoInitializeEnabled" class="kits">
                  <p class="kits-title">{{ $t("wizard.kits_title") }}</p>
                  <NsCheckbox
                    v-for="kit in starterKitList"
                    :key="kit"
                    :value="kit"
                    v-model="starterKits"
                    :label="$t('settings.kit_' + kit)"
                  />
                </div>
                <NsInlineNotification
                  v-if="isAutoInitializeEnabled"
                  kind="warning"
                  :title="$t('settings.auto_initialize_warning_title')"
                  :description="
                    $t('settings.auto_initialize_warning_description')
                  "
                  :showCloseButton="false"
                />
              </template>
              <NsInlineNotification
                v-else-if="userDomain"
                kind="info"
                :title="$t('wizard.directory_later_title')"
                :description="
                  unsealMode === 'manual' && !isInitialized
                    ? $t('wizard.directory_later_manual')
                    : $t('wizard.directory_later_initialized')
                "
                :showCloseButton="false"
              />
            </template>
          </template>
        </template>

        <!-- notifications -->
        <template v-else-if="step === 'notifications'">
          <p class="mg-bottom">{{ $t("wizard.notifications_description") }}</p>
          <NsInlineNotification
            v-if="savedConfig && !savedConfig.smarthost_enabled"
            kind="warning"
            :title="$t('settings.smarthost_disabled_title')"
            :description="$t('wizard.smarthost_disabled_description')"
            :actionLabel="$t('settings.configure_smarthost')"
            @action="goToSmarthostSettings"
            :showCloseButton="false"
          />
          <NsTextInput
            :label="$t('settings.notify_recipients')"
            :helper-text="$t('settings.notify_recipients_helper')"
            placeholder="security@example.org"
            v-model="notifyRecipients"
            :invalid-message="error.notify_recipients"
            class="mg-bottom"
            ref="notify_recipients"
          />
          <NsButton
            v-if="savedConfig && savedConfig.smarthost_enabled"
            kind="tertiary"
            size="field"
            type="button"
            :icon="Email20"
            :loading="loading.sendTestEmail"
            :disabled="loading.sendTestEmail || !recipientList.length"
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
          />
        </template>

        <!-- review -->
        <template v-else-if="step === 'review'">
          <p class="mg-bottom">{{ $t("wizard.review_description") }}</p>
          <cv-structured-list class="review-list">
            <template slot="items">
              <cv-structured-list-item
                v-for="item in reviewItems"
                :key="item.label"
              >
                <cv-structured-list-data class="review-label">{{
                  item.label
                }}</cv-structured-list-data>
                <cv-structured-list-data>{{
                  item.value
                }}</cv-structured-list-data>
              </cv-structured-list-item>
            </template>
          </cv-structured-list>
          <NsInlineNotification
            v-if="isRestartRequired"
            kind="warning"
            :title="$t('settings.restart_warning_title')"
            :description="$t('settings.restart_warning_description')"
            :showCloseButton="false"
          />
          <NsInlineNotification
            v-if="error.configureModule"
            kind="error"
            :title="$t('action.configure-module')"
            :description="error.configureModule"
            :showCloseButton="false"
          />
        </template>

        <!-- done: next steps -->
        <template v-else-if="step === 'done'">
          <h4 class="mg-bottom">{{ $t("wizard.done_title") }}</h4>

          <!-- joined an existing OpenBao -->
          <template v-if="outcome === 'joined'">
            <p class="mg-bottom">
              {{
                selectedHaCandidate &&
                selectedHaCandidate.unseal_mode === "transit"
                  ? $t("wizard.done_joined_transit")
                  : $t("wizard.done_joined_manual")
              }}
            </p>
            <NsButton
              kind="primary"
              :icon="Launch20"
              class="mg-bottom"
              type="button"
              @click="openUrl(uiUrl)"
              >{{ $t("status.open_openbao") }}</NsButton
            >
          </template>

          <!-- C: self-initialization with directory login -->
          <template v-else-if="outcome === 'self_initialized'">
            <p class="mg-bottom">{{ $t("wizard.done_self_init") }}</p>
            <NsButton
              kind="primary"
              :icon="Launch20"
              class="mg-bottom"
              type="button"
              @click="openUrl(ldapLoginUrl)"
              >{{ $t("status.ldap_login") }}</NsButton
            >
            <p class="mg-bottom">{{ $t("wizard.done_recovery_keys") }}</p>
            <NsCodeSnippet
              :copyTooltip="$t('settings.copy_to_clipboard')"
              :copy-feedback="$t('settings.copied_to_clipboard')"
              :feedback-aria-label="$t('settings.copied_to_clipboard')"
              hideExpandButton
              class="mg-bottom"
              >{{ recoveryKeysCommand }}</NsCodeSnippet
            >
          </template>

          <!-- A, B: the administrator initializes OpenBao -->
          <template v-else-if="outcome === 'initialize'">
            <p class="mg-bottom">{{ $t("wizard.done_initialize") }}</p>
            <h6 class="mg-bottom-small">{{ $t("wizard.init_cli_title") }}</h6>
            <p class="mg-bottom-small">
              {{
                unsealMode === "manual"
                  ? $t("wizard.init_cli_description_manual")
                  : $t("wizard.init_cli_description_auto")
              }}
            </p>
            <NsCodeSnippet
              :copyTooltip="$t('settings.copy_to_clipboard')"
              :copy-feedback="$t('settings.copied_to_clipboard')"
              :feedback-aria-label="$t('settings.copied_to_clipboard')"
              hideExpandButton
              class="mg-bottom"
              >{{ initCommand }}</NsCodeSnippet
            >
            <h6 class="mg-bottom-small">{{ $t("wizard.init_ui_title") }}</h6>
            <NsInlineNotification
              kind="warning"
              :title="$t('wizard.init_ui_warning_title')"
              :description="$t('wizard.init_ui_warning_description')"
              :showCloseButton="false"
            />
            <ol class="next-steps mg-bottom">
              <li>{{ $t("wizard.init_step_open") }}</li>
              <li>
                {{
                  unsealMode === "manual"
                    ? $t("wizard.init_step_shares_manual")
                    : $t("wizard.init_step_shares_auto")
                }}
              </li>
              <li>
                <strong>{{ $t("wizard.init_step_save") }}</strong>
              </li>
              <li v-if="unsealMode === 'manual'">
                {{ $t("wizard.init_step_unseal") }}
              </li>
              <li>{{ $t("wizard.init_step_login") }}</li>
              <li v-if="userDomain">{{ $t("wizard.init_step_ldap") }}</li>
              <li>{{ $t("wizard.init_step_revoke") }}</li>
            </ol>
            <NsCodeSnippet
              v-if="userDomain"
              :copyTooltip="$t('settings.copy_to_clipboard')"
              :copy-feedback="$t('settings.copied_to_clipboard')"
              :feedback-aria-label="$t('settings.copied_to_clipboard')"
              hideExpandButton
              class="mg-bottom"
              >{{ applyConfigCommand }}</NsCodeSnippet
            >
            <NsButton
              kind="primary"
              :icon="Launch20"
              class="mg-bottom"
              type="button"
              @click="openUrl(uiUrl)"
              >{{ $t("status.open_openbao") }}</NsButton
            >
            <NsInlineNotification
              v-if="unsealMode === 'manual'"
              kind="info"
              :title="$t('wizard.manual_reminder_title')"
              :description="$t('wizard.manual_reminder_description')"
              :showCloseButton="false"
            />
          </template>

          <!-- D: already initialized -->
          <template v-else>
            <p class="mg-bottom">{{ $t("wizard.done_initialized") }}</p>
            <template v-if="userDomain">
              <p class="mg-bottom">{{ $t("wizard.done_setup_ldap") }}</p>
              <NsCodeSnippet
                :copyTooltip="$t('settings.copy_to_clipboard')"
                :copy-feedback="$t('settings.copied_to_clipboard')"
                :feedback-aria-label="$t('settings.copied_to_clipboard')"
                hideExpandButton
                class="mg-bottom"
                >{{ applyConfigCommand }}</NsCodeSnippet
              >
            </template>
            <NsButton
              kind="primary"
              :icon="Launch20"
              class="mg-bottom"
              type="button"
              @click="openUrl(uiUrl)"
              >{{ $t("status.open_openbao") }}</NsButton
            >
          </template>
        </template>
      </cv-form>
    </template>
  </NsWizard>
</template>

<script>
import to from "await-to-js";
import { mapState } from "vuex";
import { UtilService, TaskService, IconService } from "@nethserver/ns8-ui-lib";
import OpenbaoConfig from "@/mixins/openbaoConfig";

const STEPS = {
  new: [
    "welcome",
    "web",
    "unseal",
    "directory",
    "notifications",
    "review",
    "done",
  ],
  join: ["welcome", "web", "join", "notifications", "review", "done"],
};

export default {
  name: "SetupWizard",
  mixins: [OpenbaoConfig, UtilService, TaskService, IconService],
  props: {
    visible: { type: Boolean, default: false },
  },
  data() {
    return {
      step: "welcome",
      setupMode: "new",
      haJoin: "",
      savedConfig: null,
      openbaoStatus: null,
      host: "",
      isLetsEncryptEnabled: true,
      isHttpToHttpsEnabled: true,
      unsealMode: "manual",
      isDirectoryEnabled: false,
      userDomain: "",
      ldapAdminGroup: "",
      domainGroups: [],
      isAutoInitializeEnabled: true,
      notifyRecipients: "",
      testEmailResult: null,
      starterKits: ["kv"],
      starterKitList: ["kv", "pki", "approle"],
      outcome: "",
      loading: {
        getConfiguration: false,
        getOpenbaoStatus: false,
        configureModule: false,
        listDomainGroups: false,
        sendTestEmail: false,
      },
      error: {
        load: "",
        configureModule: "",
        host: "",
        unseal_mode: "",
        user_domain: "",
        ldap_admin_group: "",
        auto_initialize: "",
        notify_recipients: "",
        ha_role: "",
        ha_join: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core"]),
    steps() {
      return STEPS[this.setupMode] || STEPS.new;
    },
    numberedSteps() {
      return this.steps.filter((s) => !["welcome", "done"].includes(s));
    },
    initCommand() {
      return `runagent -m ${this.instanceName} openbao-init`;
    },
    transitTokenCommand() {
      return `runagent -m ${this.instanceName} openbao-transit-token`;
    },
    stepNumber() {
      return this.numberedSteps.indexOf(this.step) + 1;
    },
    isLoadingData() {
      return this.loading.getConfiguration || this.loading.getOpenbaoStatus;
    },
    isInitialized() {
      return !!(this.openbaoStatus && this.openbaoStatus.initialized);
    },
    canAutoInitialize() {
      return (
        ["auto", "transit"].includes(this.unsealMode) && !this.isInitialized
      );
    },
    domainOptions() {
      // "none" is offered by the toggle in the wizard
      return this.userDomainOptions.filter((o) => o.value);
    },
    nextLabel() {
      if (this.step === "welcome") {
        return this.$t("wizard.start");
      } else if (this.step === "review") {
        return this.$t("wizard.apply");
      } else if (this.step === "done") {
        return this.$t("wizard.finish");
      }
      return this.$t("wizard.next");
    },
    uiUrl() {
      return `https://${this.host}/ui/`;
    },
    ldapLoginUrl() {
      return this.uiUrl + "vault/auth?with=ldap%2F";
    },
    recoveryKeysCommand() {
      return (
        `export BAO_ADDR=https://${this.host}\n` +
        "bao login -method=ldap username=<your user>\n" +
        "bao operator rotate-keys -init -target=recovery \\\n" +
        "    -key-shares=5 -key-threshold=3"
      );
    },
    willSelfInitialize() {
      return (
        this.isDirectoryEnabled &&
        !!this.userDomain &&
        this.canAutoInitialize &&
        this.isAutoInitializeEnabled
      );
    },
    isRestartRequired() {
      const saved = this.savedConfig;
      return !!(
        saved &&
        saved.host &&
        (saved.host !== this.host || saved.unseal_mode !== this.unsealMode)
      );
    },
    reviewItems() {
      const yes = this.$t("settings.enabled");
      const no = this.$t("settings.disabled");
      if (this.setupMode === "join") {
        return [
          { label: this.$t("settings.host"), value: this.host },
          {
            label: this.$t("settings.ha_join"),
            value: this.selectedHaCandidate
              ? `${this.selectedHaCandidate.module_id} (${this.selectedHaCandidate.node})`
              : this.haJoin,
          },
          {
            label: this.$t("settings.unseal_mode"),
            value: this.selectedHaCandidate
              ? this.$t(
                  "settings.unseal_mode_" + this.selectedHaCandidate.unseal_mode
                )
              : "",
          },
          {
            label: this.$t("settings.notify_recipients"),
            value: this.recipientList.length
              ? this.recipientList.join(", ")
              : no,
          },
        ];
      }
      const items = [
        { label: this.$t("settings.host"), value: this.host },
        {
          label: this.$t("settings.lets_encrypt"),
          value: this.isLetsEncryptEnabled ? yes : no,
        },
        {
          label: this.$t("settings.http_to_https"),
          value: this.isHttpToHttpsEnabled ? yes : no,
        },
        {
          label: this.$t("settings.unseal_mode"),
          value: this.$t("settings.unseal_mode_" + this.unsealMode),
        },
        {
          label: this.$t("wizard.step_directory"),
          value:
            this.isDirectoryEnabled && this.userDomain
              ? `${this.userDomain} - ${this.ldapAdminGroup}`
              : no,
        },
      ];
      if (
        this.isDirectoryEnabled &&
        this.userDomain &&
        this.canAutoInitialize
      ) {
        items.push({
          label: this.$t("wizard.review_auto_initialize"),
          value: this.isAutoInitializeEnabled ? yes : no,
        });
        if (this.isAutoInitializeEnabled) {
          items.push({
            label: this.$t("settings.section_starter_kits"),
            value: this.starterKits.length
              ? this.starterKits
                  .map((k) => this.$t("settings.kit_" + k))
                  .join(", ")
              : no,
          });
        }
      }
      items.push({
        label: this.$t("settings.notify_recipients"),
        value: this.recipientList.length ? this.recipientList.join(", ") : no,
      });
      return items;
    },
  },
  watch: {
    visible(isVisible) {
      if (isVisible) {
        this.open();
      }
    },
  },
  methods: {
    open() {
      this.step = "welcome";
      this.setupMode = "new";
      this.outcome = "";
      this.testEmailResult = null;
      this.clearErrors(this);
      this.error.load = "";
      this.getConfiguration();
      this.getOpenbaoStatus();
    },
    close() {
      if (this.loading.configureModule) {
        return;
      }
      this.$emit("hide");
    },
    goToSettings() {
      this.$emit("hide");
      this.goToAppPage(this.instanceName, "settings");
    },
    openUrl(url) {
      window.open(url, "_blank", "noopener");
    },
    onUserDomainChange() {
      this.ldapAdminGroup = "";
      this.domainGroups = [];
      if (this.userDomain) {
        this.listDomainGroups();
      }
    },
    runTask(action, onCompleted, onFailed, data) {
      const eventId = this.getUuid();
      this.core.$root.$once(`${action}-completed-${eventId}`, onCompleted);
      this.core.$root.$once(`${action}-aborted-${eventId}`, onFailed);
      return to(
        this.createModuleTaskForApp(this.instanceName, {
          action,
          data,
          extra: {
            title: this.$t("action." + action),
            isNotificationHidden: true,
            eventId,
          },
        })
      );
    },
    async getConfiguration() {
      this.loading.getConfiguration = true;
      const res = await this.runTask(
        "get-configuration",
        (taskContext, taskResult) => {
          const config = taskResult.output;
          this.savedConfig = config;
          // Prefill with the current values, or with recommended defaults
          // for a new instance
          this.host = config.host;
          this.isLetsEncryptEnabled = config.host ? config.lets_encrypt : true;
          this.isHttpToHttpsEnabled = config.host ? config.http2https : true;
          this.unsealMode = config.unseal_mode;
          // NsComboBox resolves a new value against its current options:
          // set the values after the options are rendered
          this.$nextTick(() => {
            this.userDomain = config.user_domain;
            this.ldapAdminGroup = config.ldap_admin_group;
            if (this.userDomain) {
              this.listDomainGroups();
            }
          });
          this.isDirectoryEnabled = !!config.user_domain;
          this.isAutoInitializeEnabled = config.host
            ? config.auto_initialize
            : true;
          this.notifyRecipients = config.notify_recipients.join(", ");
          this.starterKits = [...config.starter_kits];
          if (config.ha_role === "member") {
            this.setupMode = "join";
          }
          this.$nextTick(() => {
            this.haJoin = config.ha_join;
          });
          this.loading.getConfiguration = false;
        },
        () => {
          this.error.load = this.$t("error.generic_error");
          this.loading.getConfiguration = false;
        }
      );
      if (res[0]) {
        this.error.load = this.getErrorMessage(res[0]);
        this.loading.getConfiguration = false;
      }
    },
    async getOpenbaoStatus() {
      this.loading.getOpenbaoStatus = true;
      const res = await this.runTask(
        "get-openbao-status",
        (taskContext, taskResult) => {
          this.openbaoStatus = taskResult.output;
          this.loading.getOpenbaoStatus = false;
        },
        () => {
          this.loading.getOpenbaoStatus = false;
        }
      );
      if (res[0]) {
        this.loading.getOpenbaoStatus = false;
      }
    },
    validateStep() {
      this.clearErrors(this);
      if (this.step === "web") {
        if (!this.host) {
          this.error.host = this.$t("common.required");
        } else if (!this.isHostValid(this.host)) {
          this.error.host = this.$t("settings.host_format");
        }
        if (this.error.host) {
          this.focusElement("host");
          return false;
        }
      } else if (this.step === "directory" && this.isDirectoryEnabled) {
        if (!this.userDomain) {
          this.error.user_domain = this.$t("settings.user_domain_placeholder");
          this.focusElement("user_domain");
          return false;
        }
        if (!this.ldapAdminGroup) {
          this.error.ldap_admin_group = this.$t(
            "settings.ldap_admin_group_required"
          );
          this.focusElement("ldap_admin_group");
          return false;
        }
      } else if (this.step === "join") {
        if (!this.haJoin) {
          this.error.ha_join = this.$t("settings.ha_join_required");
          this.focusElement("ha_join");
          return false;
        }
      } else if (this.step === "notifications") {
        const invalid = this.invalidRecipient();
        if (invalid) {
          this.error.notify_recipients = this.$t("settings.invalid_email", {
            address: invalid,
          });
          this.focusElement("notify_recipients");
          return false;
        }
      }
      return true;
    },
    nextStep() {
      if (this.isLoadingData || this.loading.configureModule) {
        return;
      }
      if (this.step === "done") {
        this.$emit("configured");
        this.$emit("hide");
        return;
      }
      if (!this.validateStep()) {
        return;
      }
      if (this.step === "review") {
        this.configureModule();
        return;
      }
      this.step = this.steps[this.steps.indexOf(this.step) + 1];
    },
    previousStep() {
      const index = this.steps.indexOf(this.step);
      if (index > 0) {
        this.step = this.steps[index - 1];
      }
    },
    async configureModule() {
      this.error.configureModule = "";
      this.loading.configureModule = true;
      const action = "configure-module";
      const eventId = this.getUuid();
      const directory = this.isDirectoryEnabled && !!this.userDomain;
      const join = this.setupMode === "join";
      const selfInitialize = !join && this.willSelfInitialize;

      this.core.$root.$once(`${action}-completed-${eventId}`, () => {
        this.loading.configureModule = false;
        if (join) {
          this.outcome = "joined";
        } else if (selfInitialize) {
          this.outcome = "self_initialized";
        } else if (!this.isInitialized) {
          this.outcome = "initialize";
        } else {
          this.outcome = "initialized";
        }
        this.step = "done";
      });
      this.core.$root.$once(
        `${action}-validation-failed-${eventId}`,
        this.configureModuleValidationFailed
      );
      this.core.$root.$once(`${action}-aborted-${eventId}`, () => {
        this.loading.configureModule = false;
        this.error.configureModule = this.$t("error.generic_error");
      });

      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action,
          data: join
            ? {
                // The member takes the seal and the directory login of
                // the cluster it joins
                host: this.host,
                lets_encrypt: this.isLetsEncryptEnabled,
                http2https: this.isHttpToHttpsEnabled,
                ha_role: "member",
                ha_join: this.haJoin,
                auto_initialize: false,
                notify_recipients: this.recipientList,
              }
            : {
                host: this.host,
                lets_encrypt: this.isLetsEncryptEnabled,
                http2https: this.isHttpToHttpsEnabled,
                unseal_mode: this.unsealMode,
                user_domain: directory ? this.userDomain : "",
                ldap_admin_group: directory ? this.ldapAdminGroup : "",
                auto_initialize: selfInitialize,
                notify_recipients: this.recipientList,
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
      if (res[0]) {
        this.loading.configureModule = false;
        this.error.configureModule = this.getErrorMessage(res[0]);
      }
    },
    configureModuleValidationFailed(validationErrors) {
      this.loading.configureModule = false;
      // Go back to the step of the first invalid field
      const fieldSteps = {
        host: "web",
        lets_encrypt: "web",
        http2https: "web",
        unseal_mode: "unseal",
        user_domain: "directory",
        ldap_admin_group: "directory",
        auto_initialize: "directory",
        ha_role: "join",
        ha_join: "join",
      };
      let targetStep = "";
      for (const validationError of validationErrors) {
        let param = validationError.parameter;
        if (param.startsWith("notify_recipients")) {
          param = "notify_recipients";
          this.error[param] = this.$t("settings.invalid_email", {
            address: validationError.value,
          });
        } else if (param in this.error) {
          this.error[param] = this.$t("settings." + validationError.error);
        }
        if (!targetStep) {
          targetStep = fieldSteps[param] || "notifications";
        }
      }
      if (targetStep) {
        this.step = targetStep;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";

.mg-bottom {
  margin-bottom: $spacing-06;
}

.step-counter {
  margin-bottom: $spacing-05;
  color: $text-02;
}

.welcome-list,
.next-steps {
  list-style: decimal;
  padding-left: $spacing-06;
}

.welcome-list li,
.next-steps li {
  margin-bottom: $spacing-03;
}

.choice-details {
  list-style: disc;
  margin: 0 0 $spacing-05 $spacing-09;
  color: $text-02;
}

.choice-details li {
  margin-bottom: $spacing-02;
}

.kits {
  margin: $spacing-05 0 $spacing-05 $spacing-07;
}

.kits-title {
  margin-bottom: $spacing-03;
  color: $text-02;
}

.review-list {
  margin-bottom: $spacing-06;
}

.review-label {
  font-weight: 600;
  width: 40%;
}

.mg-bottom-small {
  margin-bottom: $spacing-03;
}
</style>
