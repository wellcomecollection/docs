# GitHub Groups & Permissions

Developers can be assigned to the following groups in GitHub:
- [@wellcomecollection/developers](https://github.com/orgs/wellcomecollection/teams/developers): The default group for engineering roles.
- [@wellcomecollection/buildkite-reviewers](https://github.com/orgs/wellcomecollection/teams/buildkite-reviewers): Group for folk reviewing code that will run in CI.

These groups are to aid in notification for review only and cover the 2 major languages in the platform.
- [@wellcomecollection/js-ts-reviewers](https://github.com/orgs/wellcomecollection/teams/js-ts-reviewers): Folk who can review JavaScript and TypeScript things. The [wellcomecollection.org repo](https://github.com/wellcomecollection/wellcomecollection.org) requires a review from this group before you can merge.
- [@wellcomecollection/scala-reviewers](https://github.com/orgs/wellcomecollection/teams/scala-reviewers): This group is only to notifiy folk who want to review Scala code in our services.

We have some groups for developers who we work with from external companies:
- [@wellcomecollection/digirati-external](https://github.com/orgs/wellcomecollection/teams/digirati-external): We work the [Digirati](https://digirati.com/) to provide our iiif-image & iiif-presentation APIs.
- [@wellcomecollection/intranda-external](https://github.com/orgs/wellcomecollection/teams/intranda-external): [Intranda](https://www.intranda.com/) maintain the Goobi service, part of our digital-workflow services.

And a group for folk providing oversight from the Trust:
- [@wellcomecollection/wellcome-trust-platform-technology](https://github.com/orgs/wellcomecollection/teams/wellcome-trust-platform-technology): This group contains members of the Wellcome Trust platform technology teams who have oversight of Collection services.

## CODEOWNERS

We use the [GitHub CODEOWNERS](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-code-owners) file in our repositories to ensure proper reviews on some parts of the platform.

### Buildkite pipelines

The [@wellcomecollection/buildkite-reviewers](https://github.com/orgs/wellcomecollection/teams/buildkite-reviewers) group **MUST** be added as a code owner for any Buildkite pipelines when new repositories are added or existing ones updated.

It's necessary to enforce this relationship so that only code that has been properly reviewed can be run in our [Buildkite CI environment](https://buildkite.com/wellcomecollection). CI can assume roles across accounts and changes need to be reviewed properly to maintain permission boundaries.
