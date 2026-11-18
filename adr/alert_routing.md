# Alert routing and severity

Last updated: 18/11/26

---

## Context

In October 2026 Wellcome's Digital & Technology (D&T) service management assessed the AWS-hosted services we run against ITIL practices. Assessment row AWS-26 asks that every alarm has a service, a severity, a named owner, a response expectation and an escalation route, and that alarms with no recipient are routed, deleted, or recorded as covered by another signal. This ADR writes down how alerts reach us, what each severity means, and the rule every alarm follows. It is tracked in [platform#6876](https://github.com/wellcomecollection/platform/issues/6876), under the remediation epic [platform#6790](https://github.com/wellcomecollection/platform/issues/6790).

It builds on two earlier decisions. The [service levels ADR](service_levels.md) sets our support hours (UK office hours, 9am to 5pm on weekdays, with no out-of-hours cover) and the availability targets for the website, account pages, catalogue API and identity API. The [change model ADR](change_model.md) covers how the fixes below reach production.

On 18 November 2026 there were 500 CloudWatch alarms across our nine AWS accounts. 282 reached a person, 148 drive autoscaling and are not meant to, and 70 reached nobody. None of them said which service it belonged to, how serious it was or who owned it, except through the alarm name.

## Where alerts go today

### CloudWatch alarms

Most alarms are created by shared Terraform modules and publish to an SNS topic. There are two routes from there to Slack:

- **Through a forwarding Lambda.** Each account has topics for Lambda errors, dead-letter queues, API Gateway 5xx responses and, in identity, Auth0 limits. Each topic triggers a small Lambda in platform-infrastructure (`<account>_lambda_errors_to_slack_alerts`, `<account>_dlq_to_slack_alerts` and similar) that adds detail, such as log lines from the failed invocation, and publishes to the `alerting-chatbot-events` topic in the platform account.
- **Straight to Amazon Q.** Alarms in the platform, experience and catalogue accounts can publish to `alerting-chatbot-events` directly. Catalogue pipeline state machines, deploy-tracker and the website CloudFront alarm work this way. The CloudFront per-behaviour alarms go through a responder Lambda that adds the failing URLs first.

Amazon Q Developer in chat applications (formerly Chatbot) subscribes to `alerting-chatbot-events` in eu-west-1 and us-east-1 and posts to **#wc-platform-alerts**. The bug nurse watches that channel each working day, as the [bug nurse page](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/bug-nurse.md) describes.

AWS Budgets notifications in each account go by email to the digital team mailbox.

### LogicMonitor

LogicMonitor runs the website and API checks listed in the service levels ADR. Its alerts reach #wc-platform-alerts, and also email and ServiceNow. Its configuration is in the `wellcome-devops` repository, as the [LogicMonitor ADR](logicmonitor.md) describes.

### Other sources

The bug nurse also handles alerts that are not CloudWatch alarms: ECS tasks failing to start (an EventBridge rule and Lambda in four accounts), the Auth0 log stream, and Kibana rules forwarded by a Lambda function URL. They post to the same channel.

## Decision

### Every alarm names its Backplane Component and a severity

Every CloudWatch alarm we create carries three tags:

- **`backplane:component`**: the name of the Backplane Component it watches, from the owning repository's `manifest.yml`. This is the tag Backplane already uses to tie AWS resources to Components
- **`github.com/project-slug`**: the owning repository, which tells Components apart when a repository has several
- **`severity`**: `high`, `medium` or `low`, as defined below

The alarm does not record its service or owner separately. The Component is the service, and Backplane gives its owner from `spec.owner` in the manifest, so an owner change in the manifest reaches every alarm without touching Terraform. That is what gives each alarm a named owner for AWS-26.

The Component and severity also go in a prefix on the alarm description, for example `[component=catalogue-api-search severity=high]`. The prefix is what appears in Slack, because CloudWatch's notification to SNS includes the description but not the tags, and Amazon Q shows the description for alarms that go to it directly.

Alarms are created through the shared modules (`terraform-aws-lambda`, `terraform-aws-sqs`, the platform-infrastructure monitoring and CloudFront modules, and catalogue-pipeline's state machine alarms), which take the Component and severity as inputs. A repository that writes its own `aws_cloudwatch_metric_alarm` sets the tags and prefix itself. Alarms created by hand in the console are not allowed; the ones that exist today are being deleted.

The forwarding Lambdas read the prefix and show severity as an emoji: `:rotating_light:` for high, `:warning:` for medium and `:information_source:` for low, with the Component name, so the bug nurse can look up its owner in Backplane. All three severities post to #wc-platform-alerts.

Alarms whose only action is an autoscaling policy are exempt. They are tagged `purpose = autoscaling` instead.

### Severity levels

We use three levels, taken from the severity values Backplane already defines. We do not use `critical` for alarms, because it would imply a faster or out-of-hours response that our support hours do not offer.

| Severity | Meaning | Response expectation |
|---|---|---|
| high | A service with an availability target, or a user journey that must work, is failing or about to fail; or there is a risk of losing data, or a security or privacy risk | During office hours, the bug nurse acknowledges it within one working hour and gets the owning team on it the same day. Outside office hours, best effort, under the exceptions in the service levels ADR |
| medium | Something is broken that users will notice if it is left for days, such as a failed pipeline run or messages in a dead-letter queue, or a non-production service that blocks the team | The bug nurse acknowledges it the same working day, and it is fixed, handed to the owning team or ticketed within two working days |
| low | No user effect expected: staging, housekeeping, capacity warnings, forecasts | Looked at in the Monday review or within the week; ticketed, tuned or removed |

Alerts that arrive outside office hours are picked up on the next working day. The Monday review of weekend alerts covers Saturday and Sunday. When an alarm keeps firing and nobody acts on it, the owning team lowers its severity, tunes it or deletes it.

### Escalation

| Step | Who | When |
|---|---|---|
| 1 | Bug nurse | Every alert. They acknowledge it with the emoji in the bug nurse page and either explain it, fix it, ticket it or hand it on |
| 2 | Owning team, the owner of the alarm's Component in Backplane | When the bug nurse cannot resolve it, and always for high severity |
| 3 | Incident lead and delivery manager, under the [incident comms and escalation playbook](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/incident-comms-and-escalation.md) | When it meets the playbook's definition of a major incident: the website, search, the catalogue API, requesting or sign-in unavailable or badly degraded for most users for 30 minutes or more, or a confirmed security or data exposure. Anyone can start the [incident response process](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/incident-response-process.md) for a smaller incident |
| 4 | Supplier, such as Digirati or Elastic | Decided by the incident lead, through the supplier routes in the playbook |

### Severity for kinds of alarm

| Kind of alarm | Severity |
|---|---|
| A service with an availability target, or a must-work journey, failing: 5xx and latency on the website, account pages, catalogue API and identity API, and IIIF image and presentation 5xx on CloudFront | high |
| Messages in a storage service dead-letter queue in production, because a bag did not finish ingest | high |
| Errors in a forwarding Lambda, because a broken forwarder silences a whole class of alerts | high |
| Lambda errors, the default in `terraform-aws-lambda`. Callers on a service with an availability target set high | medium |
| Catalogue pipeline: a failed state machine run or transformer failures. New works reach search late, but search keeps serving the existing index | medium |
| Messages in a catalogue pipeline dead-letter queue, which the team treats as information | low |
| Any alarm in staging or dev | low, in the same channel |

LogicMonitor's own levels map onto these: critical is high, error is medium and warning is low. Its routes to Slack, email and ServiceNow stay as they are. Whether the ServiceNow integration raises tickets, and who closes them, is being confirmed with D&T under [platform#6797](https://github.com/wellcomecollection/platform/issues/6797).

A high severity alarm is not automatically an incident. The bug nurse or owning team decides that from what users are seeing.

### Alarms with no recipient

An alarm that tells nobody is not allowed. Each one is routed or deleted.

For the 70 alarms that reached nobody on 18 November 2026 we will:

- **route 19**: the 5 dead-letter queue alarms on the editorial photography ingest queues go to their account's dead-letter queue forwarder, and the 14 on the catalogue pipelines go straight to Amazon Q at low severity. Messages land in the pipeline queues routinely and the team does not act on them one by one, so they are for information and are looked at in the Monday review
- **delete 51**: the 15 adapter and reindexer queue-age alarms, which we do not act on; 23 DynamoDB capacity alarms made in the console between 2018 and 2021; 8 scaling-style alarms on storage queues that have nothing to scale; 3 alarms on an unused inference queue; an alarm on a load balancer that has had no data since 2019; and a personal test alarm

We will also delete the 36 CloudWatch budget alarms, which watch a metric AWS Budgets does not publish and so cannot fire. The budgets' own notifications, at 100% and 110% of each account's monthly limit, cover the same thing. The error alarm on each forwarding Lambda will go straight to `alerting-chatbot-events`, so that a broken forwarder does not report its own failure through itself.

The shared modules will stop creating alarms with no action: `terraform-aws-sqs` will not create a queue-age alarm without an action, or a scaling alarm pair without scaling policies.

The list of every alarm and what happens to it is kept with the assessment evidence for AWS-26.
