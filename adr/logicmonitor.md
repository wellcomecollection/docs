# Uptime monitoring with LogicMonitor

Last updated: 12/11/25

---

We use LogicMonitor as the shared Wellcome solution for monitoring the uptime of Wellcome Collection services. This replaces the previous updown.io checks and aligns us with the wider Wellcome infrastructure tooling.

## Infrastructure

Terraform configuration for LogicMonitor lives in the [`wellcome-devops` repository](https://github.com/wellcometrust/wellcome-devops/tree/main/infrastructure/monitoring_logicmonitor). Changes to collectors, websites, or alerting should be made through this code so we keep declarative configuration and peer review in place.

Deploying updates requires a `.tfvars` file that contains account-specific secrets. A lead engineer can provide the current version of this file when changes are needed.

## Monitoring UI

The LogicMonitor portal lists the active website monitors at <https://wellcome.logicmonitor.com/santaba/uiv4/websites>. All Wellcome staff accounts have read-only access to this portal.

If you need to make changes through the LogicMonitor UI (for example, to pause a website monitor temporarily), raise a ServiceNow request to grant write access to your `c_` (cloud) account.

## Guidance

- Prefer making changes through Terraform rather than the UI so that configuration remains version-controlled.
- When introducing a new public endpoint, add an associated LogicMonitor website check and include alert routing that matches our incident response processes.
- Review existing monitors at least quarterly to ensure they still represent real user journeys and applications that we support.
