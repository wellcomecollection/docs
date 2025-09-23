# Identity Service for IIIF Builder

Last updated: 12/09/25

---

## Context

[RFC 078: Identifiers in iiif-builder](https://github.com/wellcomecollection/docs/tree/main/rfcs/078-identifiers-in-iiif-builder) describes a reorganisation of the DDS code to make use of an Identity Service to learn various attributes of a digital object, given its identifier, rather than baked-in knowledge and parsing of identifier strings:

> While we don't yet know how later implementations of this interface will obtain their information when they can no longer parse it out of the identifier string, we have removed this concern from the rest of the iiif-builder codebase and need only worry about a new implementation of `IIdentityService` for future functionality.

This ADR describes an initial implementation of `IIdentityService`

## Decision

IIIF-Builder will maintain a database table to back its identity service.

When DDS receives a [message](https://github.com/wellcomecollection/iiif-builder/blob/main/src/Wellcome.Dds/Wellcome.Dds.Common/WorkflowMessage.cs) from Goobi or Archivematica it will create or update a database row for the [Identity](https://github.com/wellcomecollection/iiif-builder/blob/5e980f358791999ae2632b75515c10f03e99ff4f/src/Wellcome.Dds/Wellcome.Dds.Common/DdsIdentity.cs) that records the information mentioned in the RFC - storage location, generator (Goobi/Archivematica) and source (Sierra, CALM, ???).

Source systems never send volume or issue level identifiers (see RFC), so the implementation still needs to do some parsing of the identifier string, but crucially will not be determining storage or source-system information from that parsing.

The DB table design will allow for _alternative identifiers_ - that a record can be resolved from identifiers in different forms.

Caveat - the `origin` property of WorkflowMessage identifies what system sent the message, which may not be the system the object originated in (`origin` can be "dashboard" or a script to batch processing items). However, Archivematica will never send a Goobi origin or vice versa, so if it's a _known_ generator of digital objects (currently just those two) then we can rely on it.

Implication - DDS / IIIFBuilder becomes a provisional source of truth for this information. This was deemed acceptable.