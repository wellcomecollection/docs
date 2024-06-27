# GitHub Actions with AWS access

Last updated: 27/06/24

---

## Context

We're going to be moving more things to GitHub actions so it's important we understand the 
security model at play, as Continuous Integration & Deployment (CI /CD) environments create 
the risk of leaking privileges from one environment to another.

### Buildkite

At the moment when we deploy things via Buildkite we give "buildkite runners" the machines that 
execute automated CI/CD permissions to assume a set of roles described in [wellcomecollection/aws-account-infrastructure](https://github.com/wellcomecollection/aws-account-infrastructure/tree/main/accounts). 

Specifically [roles like this](https://github.com/wellcomecollection/aws-account-infrastructure/blob/main/accounts/experience/iam_experience_ci.tf) 
that desribes what permissions in which account a runner can have.

The same group of people with developer credentials via Azure AD can modify this infrastructure
and have granted those permissions to the Buildkite runners which are running in our AWS accounts.

The instructions that Buildkite uses to run builds is in GitHub and the group of people who can 
propose changes to those instructions is wider than the group of developers described in Azure AD. 

- A person in the "product" team with write access in GitHub can propose changes to a Buildkite
  workflow in a pull request and those changes would be executed by the runner with the permissions
  granted by the developer group.

- Our projects are open source, so anyone with a GitHub account can propose changes with a pull
  request, there are a variety of situations within this and different options for preventing
  unapproved execution, but if these PRs are approved & merged their changes will be executed
  by the runner with the permissions granted by the developer group.

## CI Permissions

In our case outside collaborators (non-org members) require approval for GitHub actions workflows to 
run, and Buildkite is configured not to run builds from forks, these permissions are configured at 
the organisation and admin levels in GitHub and Buildkite respectively, **and should not be modified.**

At present only GitHub users who are members of the `wellcomecollection` organisation, and who have write 
permissions to repositories will have their changes executed in the CI environment. **We should continue to 
use this model.**

## Related documentation

The following links describe how to restrict access for GitHub actions runners, and who can create PRs
of different kinds relevant to this discussion.

- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
- https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

## Decision

- We will use OIDC Connect to provide access to AWS for GitHub runners
- We will create a GitHub OIDC Provider relationship in each AWS account, and associated roles for runners
- Roles will be made available to runners using GitHub repository secrets
- Roles for GitHub action runners will follow [PoLP](https://en.wikipedia.org/wiki/Principle_of_least_privilege) and be restricted by repo, branch and scope of permissions to be as narrow as possible
- Provider relationships and roles will be provisioned as IaC in the [wellcomecollection/aws-account-infrastructure](https://github.com/wellcomecollection/aws-account-infrastructure) repository
- For repositories with actions that have either write access to AWS, or read access to sensitive data only the developers GitHub group should have write access or higher
- The group of developers in GitHub should always be a subset of the group of Wellcome employees in the Wellcome developers group in Azure AD (aka Micrsoft Entra ID)







