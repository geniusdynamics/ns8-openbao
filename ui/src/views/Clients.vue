<!--
  Copyright (C) 2026 Genius Dynamics
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("clients.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <p class="page-description">{{ $t("clients.description") }}</p>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.listClients">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.list-clients')"
          :description="error.listClients"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <cv-tile light>
          <cv-skeleton-text
            v-if="loading.listClients && !info"
            :paragraph="true"
            :line-count="5"
          />
          <template v-else-if="info">
            <!-- feature state -->
            <NsInlineNotification
              v-if="!info.client_provisioning"
              kind="info"
              :title="$t('clients.disabled_title')"
              :description="$t('clients.disabled_description')"
              :actionLabel="$t('clients.go_to_settings')"
              @action="goToAppPage(instanceName, 'settings')"
              :showCloseButton="false"
            />
            <template v-else-if="info.provisioner !== 'valid'">
              <NsInlineNotification
                kind="warning"
                :title="
                  $t('clients.provisioner_' + info.provisioner + '_title')
                "
                :description="$t('clients.provisioner_missing_description')"
                :showCloseButton="false"
              />
              <NsCodeSnippet
                :copyTooltip="$t('settings.copy_to_clipboard')"
                :copy-feedback="$t('settings.copied_to_clipboard')"
                :feedback-aria-label="$t('settings.copied_to_clipboard')"
                hideExpandButton
                class="mg-bottom"
                >{{ provisionerCommand }}</NsCodeSnippet
              >
            </template>
            <NsInlineNotification
              v-if="
                !info.client_provisioning &&
                info.provisioner === 'revoke_pending'
              "
              kind="warning"
              :title="$t('clients.provisioner_revoke_pending_title')"
              :description="
                $t('clients.provisioner_revoke_pending_description')
              "
              :showCloseButton="false"
            />
            <div class="toolbar">
              <NsButton
                kind="secondary"
                :icon="Add20"
                :disabled="!info.client_provisioning || loading.setClientAccess"
                @click="openApprove(null)"
                >{{ $t("clients.approve_module") }}</NsButton
              >
            </div>
            <NsDataTable
              :allRows="info.clients"
              :columns="columnLabels"
              :rawColumns="columns"
              :sortable="true"
              :pageSizes="[10, 25, 50]"
              :isLoading="loading.listClients"
              :skeletonRows="3"
              :overflow-menu="true"
              :noSearchResultsLabel="$t('clients.no_clients')"
              :noSearchResultsDescription="$t('clients.no_clients_description')"
              :itemsPerPageLabel="$t('pagination.items_per_page')"
              :rangeOfTotalItemsLabel="$t('pagination.range_of_total_items')"
              :ofTotalPagesLabel="$t('pagination.of_total_pages')"
              :backwardText="$t('pagination.previous_page')"
              :forwardText="$t('pagination.next_page')"
              :pageNumberLabel="$t('pagination.page_number')"
              @updatePage="tablePage = $event"
            >
              <template slot="empty-state">
                <NsEmptyState :title="$t('clients.no_clients')">
                  <template #description>
                    {{ $t("clients.no_clients_description") }}
                  </template>
                </NsEmptyState>
              </template>
              <template slot="data">
                <cv-data-table-row
                  v-for="row in tablePage"
                  :key="row.module_id"
                  :value="row.module_id"
                >
                  <cv-data-table-cell>
                    <span class="module-id">{{ row.module_id }}</span>
                    <span v-if="!row.installed" class="muted">
                      {{ $t("clients.not_installed") }}</span
                    >
                  </cv-data-table-cell>
                  <cv-data-table-cell>
                    <cv-tag
                      :kind="statusKind(row.status)"
                      :label="$t('clients.status_' + row.status)"
                      size="sm"
                    />
                  </cv-data-table-cell>
                  <cv-data-table-cell>
                    <span v-if="row.database_engine">{{
                      $t("clients.granted")
                    }}</span>
                    <span v-else-if="row.database_engine_requested">{{
                      $t("clients.requested")
                    }}</span>
                    <span v-else class="muted">-</span>
                  </cv-data-table-cell>
                  <cv-data-table-cell>
                    <span>{{ row.groups.join(", ") || "-" }}</span>
                    <span v-if="row.groups_requested.length" class="muted">
                      {{
                        $t("clients.groups_requested_list", {
                          groups: row.groups_requested.join(", "),
                        })
                      }}</span
                    >
                  </cv-data-table-cell>
                  <cv-data-table-cell>{{ row.tokens }}</cv-data-table-cell>
                  <cv-data-table-cell class="table-overflow-menu-cell">
                    <cv-overflow-menu
                      flip-menu
                      class="table-overflow-menu"
                      :data-test-id="row.module_id + '-menu'"
                    >
                      <cv-overflow-menu-item
                        v-if="row.installed && info.client_provisioning"
                        @click="openApprove(row)"
                        >{{
                          row.status === "approved"
                            ? $t("clients.change_access")
                            : $t("clients.approve")
                        }}</cv-overflow-menu-item
                      >
                      <cv-overflow-menu-item danger @click="openRevoke(row)">{{
                        row.status === "pending"
                          ? $t("clients.reject")
                          : $t("clients.revoke")
                      }}</cv-overflow-menu-item>
                    </cv-overflow-menu>
                  </cv-data-table-cell>
                </cv-data-table-row>
              </template>
            </NsDataTable>
            <NsInlineNotification
              v-if="error.setClientAccess"
              kind="error"
              :title="$t('action.set-client-access')"
              :description="error.setClientAccess"
              :showCloseButton="false"
            />
            <NsInlineNotification
              v-if="cleanupPending"
              kind="warning"
              :title="$t('clients.cleanup_pending_title')"
              :description="$t('clients.cleanup_pending_description')"
              :showCloseButton="false"
            />
            <!-- audit trail -->
            <cv-accordion v-if="info.audit.length" class="mg-top">
              <cv-accordion-item>
                <template slot="title">{{ $t("clients.audit") }}</template>
                <template slot="content">
                  <cv-structured-list>
                    <template slot="headings">
                      <cv-structured-list-heading>{{
                        $t("clients.audit_time")
                      }}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{
                        $t("clients.audit_event")
                      }}</cv-structured-list-heading>
                      <cv-structured-list-heading>{{
                        $t("clients.module")
                      }}</cv-structured-list-heading>
                    </template>
                    <template slot="items">
                      <cv-structured-list-item
                        v-for="(entry, index) in info.audit.slice(0, 20)"
                        :key="index"
                      >
                        <cv-structured-list-data>{{
                          new Date(entry.time * 1000).toLocaleString()
                        }}</cv-structured-list-data>
                        <cv-structured-list-data>{{
                          $t("clients.event_" + entry.event)
                        }}</cv-structured-list-data>
                        <cv-structured-list-data>{{
                          entry.module_id || "-"
                        }}</cv-structured-list-data>
                      </cv-structured-list-item>
                    </template>
                  </cv-structured-list>
                </template>
              </cv-accordion-item>
            </cv-accordion>
          </template>
        </cv-tile>
      </cv-column>
    </cv-row>

    <!-- approve or change access -->
    <NsModal
      size="default"
      :visible="approve.visible"
      :primaryButtonDisabled="loading.setClientAccess"
      :isLoading="loading.setClientAccess"
      @modal-hidden="approve.visible = false"
      @primary-click="submitApprove"
    >
      <template slot="title">{{ $t("clients.approve_title") }}</template>
      <template slot="content">
        <cv-form @submit.prevent="submitApprove">
          <NsComboBox
            v-if="!approve.fixed"
            v-model="approve.moduleId"
            :title="$t('clients.module')"
            :label="$t('clients.choose_module')"
            :options="moduleOptions"
            :invalid-message="error.module_id"
            :acceptUserInput="false"
            class="mg-bottom"
            ref="module_id"
          />
          <p v-else class="mg-bottom">
            {{
              $t("clients.approve_module_text", { module: approve.moduleId })
            }}
          </p>
          <p class="section-description">
            {{ $t("clients.approve_scope", { prefix: kvPrefix }) }}
          </p>
          <NsCheckbox
            value="databaseEngine"
            v-model="approve.databaseEngine"
            :label="$t('clients.database_engine', { mount: dbMount })"
            class="mg-bottom"
          />
          <NsTextInput
            v-model.trim="approve.groups"
            :label="$t('clients.groups')"
            :helper-text="$t('clients.groups_helper')"
            :invalid-message="error.groups"
            placeholder="kumomta-cluster"
            class="mg-bottom"
            ref="groups"
          />
          <NsInlineNotification
            v-if="approve.requested"
            kind="info"
            :title="$t('clients.request_title')"
            :description="approve.requested"
            :showCloseButton="false"
          />
          <NsInlineNotification
            kind="warning"
            :title="$t('clients.approve_warning_title')"
            :description="$t('clients.approve_warning_description')"
            :showCloseButton="false"
          />
        </cv-form>
      </template>
      <template slot="secondary-button">{{ $t("common.cancel") }}</template>
      <template slot="primary-button">{{ $t("clients.approve") }}</template>
    </NsModal>

    <!-- revoke -->
    <NsModal
      size="default"
      kind="danger"
      :visible="revoke.visible"
      :primaryButtonDisabled="loading.setClientAccess"
      :isLoading="loading.setClientAccess"
      @modal-hidden="revoke.visible = false"
      @primary-click="submitRevoke"
    >
      <template slot="title">{{
        $t("clients.revoke_title", { module: revoke.moduleId })
      }}</template>
      <template slot="content">
        <p class="mg-bottom">{{ $t("clients.revoke_description") }}</p>
        <NsCheckbox
          value="deleteData"
          v-model="revoke.deleteData"
          :label="$t('clients.delete_data')"
        />
        <NsInlineNotification
          v-if="revoke.deleteData"
          kind="warning"
          :title="$t('clients.delete_data_warning_title')"
          :description="
            $t('clients.delete_data_warning_description', {
              prefix: 'ns8-kv/modules/' + revoke.moduleId,
              mount: 'ns8-db-' + revoke.moduleId,
            })
          "
          :showCloseButton="false"
        />
      </template>
      <template slot="secondary-button">{{ $t("common.cancel") }}</template>
      <template slot="primary-button">{{ $t("clients.revoke") }}</template>
    </NsModal>
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

const GROUP_RE = /^[a-z][a-z0-9-]{0,62}[a-z]$/;

export default {
  name: "Clients",
  mixins: [
    TaskService,
    IconService,
    UtilService,
    QueryParamService,
    PageTitleService,
  ],
  pageTitle() {
    return this.$t("clients.title") + " - " + this.appName;
  },
  data() {
    return {
      q: {
        page: "clients",
      },
      urlCheckInterval: null,
      info: null,
      tablePage: [],
      columns: ["module_id", "status", "database_engine", "groups", "tokens"],
      cleanupPending: false,
      approve: {
        visible: false,
        fixed: false,
        moduleId: "",
        databaseEngine: false,
        groups: "",
        requested: "",
      },
      revoke: {
        visible: false,
        moduleId: "",
        deleteData: false,
      },
      loading: {
        listClients: false,
        setClientAccess: false,
      },
      error: {
        listClients: "",
        setClientAccess: "",
        module_id: "",
        groups: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core", "appName"]),
    columnLabels() {
      return this.columns.map((c) => this.$t("clients.column_" + c));
    },
    moduleOptions() {
      return ((this.info && this.info.modules) || []).map((m) => ({
        name: m,
        label: m,
        value: m,
      }));
    },
    groupList() {
      return this.approve.groups
        .split(/[\s,;]+/)
        .map((g) => g.trim())
        .filter((g) => g);
    },
    kvPrefix() {
      return "ns8-kv/modules/" + (this.approve.moduleId || "<module>");
    },
    dbMount() {
      return "ns8-db-" + (this.approve.moduleId || "<module>");
    },
    provisionerCommand() {
      return `runagent -m ${this.instanceName} openbao-client-provisioner create`;
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
    this.listClients();
  },
  methods: {
    statusKind(status) {
      return (
        {
          approved: "green",
          pending: "blue",
          stale: "red",
          cleanup_pending: "gray",
        }[status] || "gray"
      );
    },
    async listClients() {
      this.loading.listClients = true;
      this.error.listClients = "";
      const taskAction = "list-clients";
      const eventId = this.getUuid();
      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.error.listClients = this.$t("error.generic_error");
        this.loading.listClients = false;
      });
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        (taskContext, taskResult) => {
          this.info = taskResult.output;
          this.loading.listClients = false;
        }
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
      if (res[0]) {
        this.error.listClients = this.getErrorMessage(res[0]);
        this.loading.listClients = false;
      }
    },
    openApprove(row) {
      this.clearErrors(this);
      this.approve.fixed = !!row;
      this.approve.moduleId = row ? row.module_id : "";
      this.approve.databaseEngine = row
        ? row.database_engine || row.database_engine_requested
        : false;
      const groups = row
        ? [...new Set([...row.groups, ...row.groups_requested])]
        : [];
      this.approve.groups = groups.join(", ");
      const requested = [];
      if (row && row.database_engine_requested) {
        requested.push(this.$t("clients.requested_database"));
      }
      if (row && row.groups_requested.length) {
        requested.push(
          this.$t("clients.requested_groups", {
            groups: row.groups_requested.join(", "),
          })
        );
      }
      this.approve.requested = requested.join(" ");
      this.approve.visible = true;
    },
    openRevoke(row) {
      this.error.setClientAccess = "";
      this.revoke.moduleId = row.module_id;
      this.revoke.deleteData = false;
      this.revoke.visible = true;
    },
    submitApprove() {
      this.clearErrors(this);
      if (!this.approve.moduleId) {
        this.error.module_id = this.$t("common.required");
        this.focusElement("module_id");
        return;
      }
      const invalid = this.groupList.find((g) => !GROUP_RE.test(g));
      if (invalid) {
        this.error.groups = this.$t("clients.invalid_group_id", {
          group: invalid,
        });
        this.focusElement("groups");
        return;
      }
      this.setClientAccess({
        module_id: this.approve.moduleId,
        allowed: true,
        database_engine: this.approve.databaseEngine,
        groups: this.groupList,
      });
    },
    submitRevoke() {
      this.setClientAccess({
        module_id: this.revoke.moduleId,
        allowed: false,
        delete_data: this.revoke.deleteData,
      });
    },
    async setClientAccess(data) {
      this.loading.setClientAccess = true;
      this.error.setClientAccess = "";
      const taskAction = "set-client-access";
      const eventId = this.getUuid();
      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.error.setClientAccess = this.$t("error.generic_error");
        this.loading.setClientAccess = false;
        this.approve.visible = false;
        this.revoke.visible = false;
      });
      this.core.$root.$once(
        `${taskAction}-validation-failed-${eventId}`,
        (validationErrors) => {
          this.loading.setClientAccess = false;
          for (const e of validationErrors) {
            const message = this.$t("clients." + e.error, {
              group: e.value,
            });
            if (e.parameter in this.error && this.approve.visible) {
              this.error[e.parameter] = message;
            } else {
              this.error.setClientAccess = message;
              this.approve.visible = false;
              this.revoke.visible = false;
            }
          }
        }
      );
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        (taskContext, taskResult) => {
          this.loading.setClientAccess = false;
          this.approve.visible = false;
          this.revoke.visible = false;
          this.cleanupPending = taskResult.output.cleanup === "pending";
          this.listClients();
        }
      );
      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data,
          extra: {
            title: data.allowed
              ? this.$t("clients.approving", { module: data.module_id })
              : this.$t("clients.revoking", { module: data.module_id }),
            eventId,
          },
        })
      );
      if (res[0]) {
        this.error.setClientAccess = this.getErrorMessage(res[0]);
        this.loading.setClientAccess = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";

.page-description {
  max-width: 48rem;
  margin-bottom: $spacing-06;
}

.mg-bottom {
  margin-bottom: $spacing-06;
}

.mg-top {
  margin-top: $spacing-07;
}

.toolbar {
  margin-bottom: $spacing-05;
}

.section-description {
  margin-bottom: $spacing-05;
  color: $text-02;
}

.module-id {
  font-weight: 600;
  margin-right: $spacing-03;
}

.muted {
  color: $text-02;
}
</style>
