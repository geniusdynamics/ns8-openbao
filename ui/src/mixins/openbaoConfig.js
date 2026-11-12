//
// Copyright (C) 2026 Genius Dynamics
// SPDX-License-Identifier: GPL-3.0-or-later
//

// Helpers shared by the Settings page and the setup wizard. The component
// must define the data fields savedConfig, userDomain, ldapAdminGroup,
// domainGroups, notifyRecipients, testEmailResult, error.notify_recipients,
// loading.listDomainGroups and loading.sendTestEmail, and use the
// TaskService and UtilService mixins.

import to from "await-to-js";

export default {
  computed: {
    userDomainOptions() {
      const domains = (this.savedConfig && this.savedConfig.user_domains) || [];
      const options = [
        { name: "", label: this.$t("settings.user_domain_none"), value: "" },
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
    hasUserDomains() {
      return !!(
        this.savedConfig &&
        this.savedConfig.user_domains &&
        this.savedConfig.user_domains.length
      );
    },
    adminGroupOptions() {
      const options = this.domainGroups.map((group) => ({
        name: group,
        label: group,
        value: group,
      }));
      // keep the current value selectable even if it is not listed
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
    recipientList() {
      return this.notifyRecipients
        .split(/[,;\s]+/)
        .map((r) => r.trim())
        .filter((r) => r);
    },
    setupLdapCommand() {
      return `runagent -m ${this.instanceName} openbao-setup-ldap`;
    },
  },
  methods: {
    isEmailValid(address) {
      return /^[^@\s,]+@[^@\s,]+\.[^@\s,]+$/.test(address);
    },
    invalidRecipient() {
      return this.recipientList.find((r) => !this.isEmailValid(r)) || "";
    },
    isHostValid(host) {
      return /^(?=.{1,253}$)([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z0-9-]{2,63}$/.test(
        host
      );
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
        this.error.notify_recipients = this.$t(
          "settings.notify_recipients_required"
        );
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
    goToSmarthostSettings() {
      this.core.$router.push("/settings/smarthost");
    },
    goToDomainsAndUsers() {
      this.core.$router.push("/domains");
    },
  },
};
