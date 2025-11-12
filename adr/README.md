# Architecture Decision Records (ADR)

Documents here are intended to record and describe particular architectural decisions. 

---

An ADR records a a particular decision and contains the key information to understand how the mechanism it describes work.

**An ADR is not an RFC**. An RFC is speculative and provides a place to discuss multiple options with pros and cons, which may or may not be implemented. An ADR relates only to the current implementation and will be replaced as new decisions are made.

## Table of contents


| Document | Description |
|---|---|
| [Architecture Decision Records (ADR)](README.md) | A description of the purpose of ADRs and how they differ from RFCs. |
| [API faceting principles & expectations](api_faceting.md) | Guidelines for implementing faceting in APIs, including expectations for performance and usability. |
| [GitHub Actions with AWS access](gha_aws.md) | Best practices for using GitHub Actions with AWS, including authentication and permissions. |
| [GitHub Groups & Permissions](github_groups_permissions.md) | An overview of GitHub groups and permissions, including how to manage access to repositories. |
| [GitHub Security](github_security.md) | Guidelines for securing GitHub repositories, including best practices for managing secrets and access. |
| [Logging](logging.md) | Best practices for logging in applications, including log levels and structured logging. |
| [Secrets](secrets.md) | Guidelines for managing secrets in applications, including best practices for storing and accessing sensitive information. |
| [Uptime monitoring with LogicMonitor](logicmonitor.md) | Overview of our LogicMonitor-based website uptime monitoring and how to manage it. |
| [Base AMI updates](base_ami_updates.md) | A process for updating base AMIs in Wellcome Collection AWS accounts. |
| [Identity service for IIIF-Builder](iiif-builder-identity-service.md) | How IIIF-Builder (DDS) learns where and how digital objects are stored, given an identifier |
