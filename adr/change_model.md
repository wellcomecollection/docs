# Change model

Last updated: 13/11/26

---

## Context

In October 2026 Wellcome's Digital & Technology (D&T) service management assessed the AWS-hosted services we run against ITIL practices. It found that we control production changes through pull requests, CI and gated deploy pipelines, but that nothing written says this is our change model, which record is the change record, or who may change production outside that route. This ADR writes the model down. It answers assessment rows AWS-09, AWS-10 and AWS-11 and is tracked from [platform#6790](https://github.com/wellcomecollection/platform/issues/6790).

It covers production changes to the services the digital platform team runs in the Wellcome Collection AWS accounts: application code, infrastructure defined in Terraform, and configuration such as toggles. Workloads maintained by suppliers (Archivematica, Goobi and DLCS) are the supplier's responsibility and follow the supplier's process.

## Decision

### Change authority

Change authority for these changes sits with the digital platform team. The Head of Digital Experience and Engagement is accountable for the risk of production changes, as they are for the out-of-hours support position in the [service levels ADR](service_levels.md). The D&T change process does not apply to Collection infrastructure.

### Normal change

A normal change is any change that is not a standard or an emergency change. Most changes are normal changes and take this route:

1. A pull request against `main`, written under the headings of the [pull request template](https://github.com/wellcomecollection/.github/blob/main/PULL_REQUEST_TEMPLATE.md).
2. An approving review from at least one person other than the author. Branch protection on `main` requires one, although admins can bypass it, and CODEOWNERS sends the review to the owning team.
3. CI passes on the pull request.
4. Merging deploys to staging automatically, where the service has a staging environment.
5. A person checks staging and then approves the production deploy, either at a Buildkite block step or through a GitHub environment with required reviewers.
6. The production deploy is recorded as a GitHub Deployment to the `prod` environment.

The change record is the merged pull request together with the GitHub Deployment that shipped it.

### Test evidence, validation and rollback

The pull request template has headings for how the change was tested, how we check it once it is in production, and how to roll it back ([platform#6874](https://github.com/wellcomecollection/platform/issues/6874)). What goes under them depends on the kind of change:

- A normal change fills in each heading.
- A standard change names its catalogue entry and can point at that entry's procedure.
- An emergency change fills in the headings after the event.

The usual rollback for code is a revert pull request through the same route, as the [post code review](https://github.com/wellcomecollection/developer-handbook/blob/main/developer-handbook/github-process/post-code-review.md) page describes.

### Standard changes

A standard change is a kind of change we have agreed in advance is low risk and has a written procedure. Its pull request names the catalogue entry it falls under, and still needs an approving review from someone other than the author.

| Change | Procedure |
|---|---|
| A dependency update raised by Dependabot, with CI passing | [Dependabot](https://github.com/wellcomecollection/developer-handbook/blob/main/developer-handbook/dependabot.md) |
| Turning a toggle on for the public once its checklist is complete | [Toggles and feature flags](https://github.com/wellcomecollection/developer-handbook/blob/main/developer-handbook/front-end/toggles-feature-flags.md), "Before turning a toggle ON" |
| Updating a WAF IP list, either through the WAF IP set updaters or by adding an address to a block list | [WAF IP set updaters](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/cache/ip-updaters/README.md), and "Bot or scraper traffic slows or breaks the site" in the [website runbook](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/docs/runbook.md#bot-or-scraper-traffic-slows-or-breaks-the-site) |
| Changing an ECS service's task count or an Elastic Cloud deployment's size within agreed bounds | The bounds are recorded in the service's runbook. _To be written: the bounds for each service._ |
| Publishing a Prismic content model change in the documented order | [Updating an existing custom type](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/prismic-model/README.md#updating-an-existing-custom-type) in the prismic-model README |

A public toggle change and a block list update are made without a pull request. _To be agreed: where they are recorded._

Entries are added or removed by a pull request to this page. The lead engineer reviews the catalogue every quarter.

### Emergency change

An emergency change is one that can't wait for the normal route. Only the lead engineer, or a senior engineer the lead engineer has delegated authority to, makes one. They record it in #wc-digital-platform at the time it is made, in one message per change that links the pull request or the Terraform apply.

### Merging without review

Merging a pull request without an approving review is not standard practice. The lead engineer may do it when it is required, for an emergency change or when no reviewer is available and the change can't wait. Each time, the lead engineer records it: the pull request body says why the change could not wait for review, and a message in #wc-digital-platform links the pull request. Other admins don't merge without a review.

### Terraform

Any developer who has completed induction may run `terraform apply` against production. The Terraform code goes through the normal route, and is applied to production only from `main` after its pull request has merged. Applying anything else to production is an emergency change. CloudTrail in each account is the record of who applied a change and when. Its coverage of every account is being confirmed with the D&T Cloud team under [platform#6793](https://github.com/wellcomecollection/platform/issues/6793).

Terraform applies don't create GitHub Deployments, so they aren't counted in the change failure rate below.

### Change failure rate

We report change failure rate from the DORA metrics in Backplane (internal), our developer portal. Backplane counts production deploys recorded as GitHub Deployments, and shows a service whose deploys don't create one as not measured. It doesn't yet work out which deploys failed.

### Where practice differs today

- Some repositories deploy to production without a person checking staging first, and some have no staging environment.
- Some repositories don't create GitHub Deployments, so their change record is the pull request alone and their deploys aren't counted in the change failure rate.

## Related documentation

- [GitHub Groups & Permissions](github_groups_permissions.md)
