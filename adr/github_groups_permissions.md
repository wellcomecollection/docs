# GitHub Groups & Permissions

Developers can be assigned to the following groups in GitHub:
- [@wellcomecollection/developers](https://github.com/orgs/wellcomecollection/teams/developers): The default group for engineering roles.

These groups are to aid in notification for review only and cover the 2 major languages in the platform:
- [@wellcomecollection/js-ts-reviewers](https://github.com/orgs/wellcomecollection/teams/js-ts-reviewers): Folk who can review JavaScript and TypeScript things. The [wellcomecollection.org repo](https://github.com/wellcomecollection/wellcomecollection.org) requires a review from this group before you can merge.
- [@wellcomecollection/scala-reviewers](https://github.com/orgs/wellcomecollection/teams/scala-reviewers): This group is only to notifiy folk who want to review Scala code in our services.

There are also teams and sub-teams for product/project/UX team members:
- [@wellcomecollection/product-project-ux](https://github.com/orgs/wellcomecollection/teams/product-project-ux): Product ownership, project management & UX team
  - [@wellcomecollection/data](https://github.com/orgs/wellcomecollection/teams/data): Data science & analytics
  - [@wellcomecollection/design](https://github.com/orgs/wellcomecollection/teams/data): All things design and UX

We have a group for developers from an external company who have Wellcome accounts:
- [@wellcomecollection/intranda-external](https://github.com/orgs/wellcomecollection/teams/intranda-external): [Intranda](https://www.intranda.com/) maintain the Goobi service, part of our digital-workflow services.

Developers from other partners are outside collaborators rather than organisation members, with access granted repository by repository (see [Access policy](#access-policy)).

And a group for folk providing oversight from the Trust:
- [@wellcomecollection/wellcome-trust-platform-technology](https://github.com/orgs/wellcomecollection/teams/wellcome-trust-platform-technology): This group contains members of the Wellcome Trust platform technology teams who have oversight of Collection services.

## Access policy

The organisation enforces SAML single sign-on through Wellcome's Entra ID, so every member signs in to GitHub through their Wellcome account.
Someone without a linked Wellcome identity is removed from the organisation.
They can rejoin by signing in at <https://github.com/orgs/wellcomecollection/sso> with their Wellcome account, and if they do so within three months of being removed, their previous teams are restored.

Members of the `ent:data-engineering` and `ent:machine-learning` enterprise teams are added to the organisation by the Wellcome Trust enterprise account, not by us, and stay members whether or not they have signed in through SSO.

Partner developers who don't have Wellcome accounts are outside collaborators, which SSO does not apply to.
They can't join teams, so each one is granted access on the repositories they work on, and none has access to a private repository:
- [Artefactual](https://www.artefactual.com/), who support Archivematica: maintain on `archivematica-infrastructure`.
- [Digirati](https://digirati.com/), who run our IIIF services: write or maintain on `iiif-builder`, `iiif-builder-infrastructure` and `londons-pulse`, and read on a few related repositories.

Members can't create repositories. Ask an organisation owner to create one.

We don't use machine users.
Automation acts on GitHub through organisation-owned GitHub Apps, described in [platform-infrastructure/github](https://github.com/wellcomecollection/platform-infrastructure/tree/main/github), and Buildkite checks out code with a read-only deploy key per repository, described in [buildkite-infrastructure](https://github.com/wellcomecollection/buildkite-infrastructure#how-builds-check-out-code).

## CODEOWNERS

We use the [GitHub CODEOWNERS](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-code-owners) file in our repositories to ensure proper reviews on some parts of the platform.

### Buildkite pipelines

The [@wellcomecollection/buildkite-reviewers](https://github.com/orgs/wellcomecollection/teams/buildkite-reviewers) group **MUST** be added as a code owner for any Buildkite pipelines when new repositories are added or existing ones updated.

You can use this template repository when starting a new project that needs CI: https://github.com/wellcomecollection/buildkite-template

It's necessary to enforce this relationship so that only code that has been properly reviewed can be run in our [Buildkite CI environment](https://buildkite.com/wellcomecollection). CI can assume roles across accounts and changes need to be reviewed properly to maintain permission boundaries.
