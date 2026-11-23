# Service ownership and lifecycle decisions

Last updated: 23/11/26

---

This records where service ownership is held, who is accountable for a service, and who decides what across its life. It answers assessment row AWS-21 from the Digital & Technology (D&T) service management assessment of October 2026. Tracked in [platform#6791](https://github.com/wellcomecollection/platform/issues/6791) under [platform#6790](https://github.com/wellcomecollection/platform/issues/6790).

## Ownership register

Backplane (internal), our developer portal, is the ownership register. Each repository declares its systems and components in `manifest.yml`, with the owning team in `spec.owner` and the runbook as a link. Backplane shows these, and D&T can open it. The service pages in [architecture/services](../architecture/services/README.md) name the Backplane entity rather than copying the owner or runbook.

The lead engineer of the owning team is accountable for a service day to day.

Services are not recorded as ServiceNow configuration items. This follows the D&T CMMI work package on a product-led application lifecycle (INIT-16), which builds on the product operating model and asks that each application has clear accountable ownership from Transform through Build and Run to Retire. Backplane holds that ownership next to the code, so it changes in the same pull request as the service. If D&T needs our services listed in ServiceNow, the list should be generated from Backplane rather than kept by hand, so that the two cannot drift.

## Lifecycle decisions

R is responsible, A accountable, C consulted and I informed.

| Decision | Owning team | Lead engineer | Delivery manager | Head of Digital Experience and Engagement | D&T |
|---|---|---|---|---|---|
| Architecture of a service, recorded as an ADR | R | A | I | I | C for anything touching D&T infrastructure |
| Production change ([change model](change_model.md)) | R | A | I | Accountable for the risk | |
| Incident command ([major incident playbook](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/incident-comms-and-escalation.md)) | R | R as incident lead or cover | A as comms lead | I for a major incident | I for a major incident |
| Accepting a known risk or a gap in a control | C | R | I | A | I |
| Access to AWS accounts and services | R for granting within the team | A | | I | C, as owners of account governance |
| Cost and budget | C | R | I | A | I |
| Retiring a service | R | R | C | A | I |

## Quarterly review

Every quarter the lead engineers check that each service has a Backplane entity with the right owner and runbook, that new services have a page, and that retired ones have moved to Legacy. They do this alongside the review of the standard change catalogue in the [change model](change_model.md), and record it as an issue on the platform board.

## Related documentation

- [Service levels](service_levels.md)
- [Change model](change_model.md)
