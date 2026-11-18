# Service Name

## Description

*A brief, one-sentence description of what this service does.*

## Ownership and support

*Name the service's Backplane entity as `kind:name`, without a link. Owner, runbook and supplier contacts live in the repository's `manifest.yml` and show in Backplane, so don't copy them here. Support hours follow the [service levels ADR](https://github.com/wellcomecollection/docs/blob/main/adr/service_levels.md) and escalation follows the [major incident playbook](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/incident-comms-and-escalation.md). Write anything else here only when the service is an exception, for example run by a supplier or owned outside the team.*

- **Owner and runbook:** *`system:ENTITY` in Backplane (internal)*

## Architecture

*A more detailed explanation of the service's architecture. What does it do? How does it work? What are the key components?*

*You can include diagrams here if you have them, for example:*

```puml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

Container(service, "Service Name", "Technology", "Description")

@enduml
```

## Repositories

*A list of the GitHub repositories that contain the code for this service.*

- [wellcomecollection/service-repo-1](https://github.com/wellcomecollection/service-repo-1)
- [wellcomecollection/service-repo-2](https://github.com/wellcomecollection/service-repo-2)

## Accounts

*A list of the AWS accounts where this service is deployed.*

- [platform](../aws_accounts.md#platform)
- [experience](../aws_accounts.md#experience)

