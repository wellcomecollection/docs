# Architecture Documentation

This document provides a high-level overview of the technical architecture of the Wellcome Collection's digital platform. It is intended to be a living document that evolves with our systems.

## Sections

- [AWS Accounts](./aws_accounts.md): Describes the structure and purpose of our AWS accounts, including the services hosted within each account.
- [Domain Names](./domain_names.md): A comprehensive list of domain names used by Wellcome Collection, detailing their purpose and the services they are associated with.
- [Services](./services/README.md): A detailed index of the services that constitute our digital platform, categorized by their function.
- [Partners and Third-Party Services](./partners.md): An overview of the external partners, and third-party services that we integrate with.


## Architectural Decision Records (ADRs)

We use ADRs to document significant architectural decisions. You can find our ADRs in the [`/adr`](../adr) directory. A key ADR related to this documentation is:

- [ADR: Using C4 Model at Container Level for Service Documentation](../adr/c4_model_for_services.md): This ADR outlines our approach to documenting services using the C4 model.

## Maintenance

This documentation is a living document. It is the responsibility of all engineers to ensure that it is kept up-to-date. When creating a new service or updating an existing one, the relevant documentation in this section must be updated as part of that work.