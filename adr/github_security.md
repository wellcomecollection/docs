# GitHub Security

Last updated: 19/03/24

---

## Context

We can improve visibility of security vulnerabilities in our services introduced either by insecure coding patterns or open source dependencies. 

In order that we avoid the exploitation of vulnerabilities present in our services we should identify and mitigate vulnerabilities that may allow attackers to access sensitive data and run code on your application, as well as being aware of potential licensing issues. 

See the [Q1 2024 Platform Health OKR proposal](https://wellcomecloud.sharepoint.com/:w:/r/sites/wc2/DE/Platform/_layouts/15/doc2.aspx?sourcedoc=%7B42A407B7-61E8-45A1-BDC2-C0E65DED1F7A%7D&file=Platform%20Health%20OKR%20proposal.docx&action=default&mobileredirect=true).

## Decision

We should have visibility of [Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts), [CodeQL](https://codeql.github.com/) issues, [secrets in code](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning) and an automated mechanism to raise PRs to remediate vulnerabilities.

This will involve:

- Providing Dependabot with a graph of dependencies for all our Scala repositories
- Providing a usable mechanism to raise PRs against both Scala & Typescript repositories
- Providing a mechanism to incentivise merging automated PRs, consisting of:
  - ChatOps notification of open PRs in need of review & merge
  - Preventing proliferation of unmerged PRs by automated closing when stale

In addition we will enable at the [organisation level security settings](https://github.com/organizations/wellcomecollection/settings/security_analysis):

- Dependabot alerts for all repositories for medium, high & critical vulnerabilities idenitified in depenendency graphs for our services.
- Automated PR raising by Dependabot for all repositories for all critical vulnerabilities.
- Grouped security updates for all repositories to expedite testing and merging remediation PRs.
- Secret scanning with push protection on all out repositories for supported secrets.
