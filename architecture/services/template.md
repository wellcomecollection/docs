# Service Name

## Description

*A brief, one-sentence description of what this service does.*

## Ownership and support

*Fill in all four fields. Link to Backplane rather than copying what it holds: owners come from `spec.owner` in the repository's `manifest.yml`, team contacts from the team page, and supplier contacts from the System or Component. Name roles, not people.*

- **Owner:** *The owning team from `spec.owner` in `manifest.yml` and the role accountable for the service, linking the Backplane entity, for example "[catalogue-api](https://backplane.wellcome.digital/catalog/system/default/catalogue-api) (internal), Digital Platform team, lead engineer". If the repository has no `manifest.yml` yet, name the team and role and add "no Backplane entity yet".*
- **Runbook:** *Link the service's `docs/runbook.md`, the same URL as the `Runbook` link in `manifest.yml`. If there is no runbook, write "none yet".*
- **Support hours:** Office hours. Out of hours is best effort. See the [service-level statement](https://github.com/wellcomecollection/docs/blob/main/adr/service_levels.md).
- **Escalation:** Follow the [major incident playbook](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/incident-comms-and-escalation.md). *If a supplier runs part of the service, add "Supplier escalation is on the Backplane entity page (internal)."*

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

