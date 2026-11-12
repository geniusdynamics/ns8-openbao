<!--
  Copyright (C) 2026 Genius Dynamics
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("plugins.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <p class="page-description">{{ $t("plugins.description") }}</p>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.listPlugins">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.list-plugins')"
          :description="error.listPlugins"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <cv-tile light>
          <cv-skeleton-text
            v-if="loading.listPlugins && !plugins.length"
            :paragraph="true"
            :line-count="8"
          />
          <template v-else>
            <div v-for="group in groups" :key="group.type" class="plugin-group">
              <h4 class="section-title">
                {{ $t("plugins.group_" + group.type) }}
              </h4>
              <div
                v-for="plugin in group.plugins"
                :key="plugin.id"
                class="plugin-row"
              >
                <div class="plugin-header">
                  <div class="plugin-text">
                    <div class="plugin-name">
                      {{ $t("plugins.name_" + plugin.id.replace(/-/g, "_")) }}
                      <cv-tag
                        :kind="tagKind(plugin)"
                        :label="tagLabel(plugin)"
                        size="sm"
                      />
                      <span class="plugin-version">{{ plugin.version }}</span>
                    </div>
                    <p class="plugin-description">
                      {{ $t("plugins.desc_" + plugin.id.replace(/-/g, "_")) }}
                    </p>
                  </div>
                  <NsToggle
                    v-if="!plugin.bundled"
                    :value="plugin.id"
                    hideLabel
                    :label="$t('plugins.name_' + plugin.id.replace(/-/g, '_'))"
                    v-model="toggles[plugin.id]"
                    :disabled="loading.configurePlugins"
                  >
                    <template slot="text-left">{{
                      $t("settings.disabled")
                    }}</template>
                    <template slot="text-right">{{
                      $t("settings.enabled")
                    }}</template>
                  </NsToggle>
                </div>
                <NsInlineNotification
                  v-if="plugin.installed && !isSelected(plugin)"
                  kind="warning"
                  :title="$t('plugins.remove_warning_title')"
                  :description="$t('plugins.remove_warning_description')"
                  :showCloseButton="false"
                />
                <cv-accordion v-if="plugin.installed && !plugin.bundled">
                  <cv-accordion-item>
                    <template slot="title">{{
                      $t("plugins.how_to_use")
                    }}</template>
                    <template slot="content">
                      <p class="step">{{ $t("plugins.step_enable") }}</p>
                      <NsCodeSnippet
                        :copyTooltip="$t('settings.copy_to_clipboard')"
                        :copy-feedback="$t('settings.copied_to_clipboard')"
                        :feedback-aria-label="
                          $t('settings.copied_to_clipboard')
                        "
                        hideExpandButton
                        class="mg-bottom"
                        >{{ plugin.enable_command }}</NsCodeSnippet
                      >
                      <p class="step">{{ $t("plugins.step_configure") }}</p>
                      <NsCodeSnippet
                        :copyTooltip="$t('settings.copy_to_clipboard')"
                        :copy-feedback="$t('settings.copied_to_clipboard')"
                        :feedback-aria-label="
                          $t('settings.copied_to_clipboard')
                        "
                        class="mg-bottom"
                        >{{ plugin.setup_commands.join("\n") }}</NsCodeSnippet
                      >
                      <cv-link :href="plugin.docs_url" target="_blank">
                        {{ $t("plugins.documentation") }}
                      </cv-link>
                    </template>
                  </cv-accordion-item>
                </cv-accordion>
              </div>
            </div>
            <NsInlineNotification
              v-if="isChanged"
              kind="info"
              :title="$t('plugins.restart_title')"
              :description="$t('plugins.restart_description')"
              :showCloseButton="false"
            />
            <NsInlineNotification
              v-if="error.configurePlugins"
              kind="error"
              :title="$t('action.configure-plugins')"
              :description="error.configurePlugins"
              :showCloseButton="false"
            />
            <NsButton
              kind="primary"
              :icon="Save20"
              :loading="loading.configurePlugins"
              :disabled="!isChanged || loading.configurePlugins"
              @click="configurePlugins"
              >{{ $t("plugins.apply") }}</NsButton
            >
          </template>
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

const GROUPS = ["auth", "secret", "database"];

export default {
  name: "Plugins",
  mixins: [
    TaskService,
    IconService,
    UtilService,
    QueryParamService,
    PageTitleService,
  ],
  pageTitle() {
    return this.$t("plugins.title") + " - " + this.appName;
  },
  data() {
    return {
      q: {
        page: "plugins",
      },
      urlCheckInterval: null,
      plugins: [],
      toggles: {},
      loading: {
        listPlugins: false,
        configurePlugins: false,
      },
      error: {
        listPlugins: "",
        configurePlugins: "",
      },
    };
  },
  computed: {
    ...mapState(["instanceName", "core", "appName"]),
    groups() {
      return GROUPS.map((type) => ({
        type,
        plugins: this.plugins.filter((p) => p.type === type),
      })).filter((g) => g.plugins.length);
    },
    selected() {
      return this.plugins
        .filter((p) => !p.bundled && this.toggles[p.id])
        .map((p) => p.id);
    },
    savedSelection() {
      return this.plugins
        .filter((p) => !p.bundled && p.enabled)
        .map((p) => p.id)
        .sort();
    },
    isChanged() {
      return (
        JSON.stringify([...this.selected].sort()) !==
        JSON.stringify(this.savedSelection)
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
    this.listPlugins();
  },
  methods: {
    isSelected(plugin) {
      return plugin.bundled || !!this.toggles[plugin.id];
    },
    tagKind(plugin) {
      if (plugin.bundled) {
        return "blue";
      }
      if (plugin.installed) {
        return plugin.installed_version === plugin.version ? "green" : "teal";
      }
      return "gray";
    },
    tagLabel(plugin) {
      if (plugin.bundled) {
        return this.$t("plugins.state_bundled");
      }
      if (plugin.installed) {
        return plugin.installed_version === plugin.version
          ? this.$t("plugins.state_installed")
          : this.$t("plugins.state_update", {
              version: plugin.installed_version,
            });
      }
      return plugin.enabled
        ? this.$t("plugins.state_pending")
        : this.$t("plugins.state_available");
    },
    async listPlugins() {
      this.loading.listPlugins = true;
      this.error.listPlugins = "";
      const taskAction = "list-plugins";
      const eventId = this.getUuid();
      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.error.listPlugins = this.$t("error.generic_error");
        this.loading.listPlugins = false;
      });
      this.core.$root.$once(
        `${taskAction}-completed-${eventId}`,
        (taskContext, taskResult) => {
          const plugins = taskResult.output.plugins;
          // a new object, so every key is reactive before rendering
          this.toggles = Object.fromEntries(
            plugins.map((p) => [p.id, p.bundled || p.enabled])
          );
          this.plugins = plugins;
          this.loading.listPlugins = false;
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
        console.error(`error creating task ${taskAction}`, res[0]);
        this.error.listPlugins = this.getErrorMessage(res[0]);
        this.loading.listPlugins = false;
      }
    },
    async configurePlugins() {
      this.loading.configurePlugins = true;
      this.error.configurePlugins = "";
      const taskAction = "configure-plugins";
      const eventId = this.getUuid();
      this.core.$root.$once(`${taskAction}-aborted-${eventId}`, () => {
        this.error.configurePlugins = this.$t("error.generic_error");
        this.loading.configurePlugins = false;
      });
      this.core.$root.$once(
        `${taskAction}-validation-failed-${eventId}`,
        (validationErrors) => {
          this.loading.configurePlugins = false;
          const failed = validationErrors.map((e) => e.value).join(", ");
          this.error.configurePlugins = this.$t(
            "plugins.plugin_download_failed",
            { plugins: failed }
          );
        }
      );
      this.core.$root.$once(`${taskAction}-completed-${eventId}`, () => {
        this.loading.configurePlugins = false;
        this.listPlugins();
      });
      const res = await to(
        this.createModuleTaskForApp(this.instanceName, {
          action: taskAction,
          data: { plugins: this.selected },
          extra: {
            title: this.$t("plugins.configure_title", {
              instance: this.instanceName,
            }),
            description: this.$t("plugins.configuring"),
            eventId,
          },
        })
      );
      if (res[0]) {
        console.error(`error creating task ${taskAction}`, res[0]);
        this.error.configurePlugins = this.getErrorMessage(res[0]);
        this.loading.configurePlugins = false;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";

.page-description {
  margin-bottom: $spacing-06;
  max-width: 60rem;
}

.section-title {
  margin-top: $spacing-07;
  margin-bottom: $spacing-05;
}

.plugin-group:first-child .section-title {
  margin-top: 0;
}

.plugin-row {
  padding: $spacing-05 0;
  border-bottom: 1px solid $ui-03;
}

.plugin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: $spacing-05;
}

.plugin-name {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: $spacing-03;
  flex-wrap: wrap;
}

.plugin-version {
  font-weight: 400;
  color: $text-02;
}

.plugin-description {
  color: $text-02;
  margin-top: $spacing-02;
}

.step {
  margin-bottom: $spacing-03;
}

.mg-bottom {
  margin-bottom: $spacing-05;
}

.bx--btn {
  margin-top: $spacing-06;
}
</style>
