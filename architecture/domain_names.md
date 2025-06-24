# Domain names

This document lists the domain names used by the Wellcome Collection, and their purpose and associated services.

## Table of Contents

- [Collection user facing domains](#collection-user-facing-domains)
- [Product/Engineering team facing domains](#productengineering-team-facing-domains)
- [Collection Staff facing domains](#collection-staff-facing-domains)
- [Internal routing domains](#internal-routing-domains)

The following domains manage DNS for wellcomecollection.org:
- [wellcometrust/wellcome-dns-infra](https://github.com/wellcometrust/wellcome-dns-infra): Top level DNS management including hosted zone delegation.
- [wellcomecollection/platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure/tree/main/cloudfront/wellcomecollection.org): DNS management for the wellcomecollection.org domain.

### Collection user facing domains

| Domain Name | Description | Served By | AWS Account | Example URL |
| :--- | :--- | :--- | :--- | :--- |
| `wellcomecollection.org` | The main public-facing website for Wellcome Collection. | `CloudFront` | `experience` | `https://wellcomecollection.org/` |
| `iiif.wellcomecollection.org` | Serves images and other material via the IIIF standard. | `CloudFront` | `platform` | `https://iiif.wellcomecollection.org/image/B0000001/info.json` |
| `api.wellcomecollection.org` | The main entry point for all public APIs. | `CloudFront` | `platform` | `https://api.wellcomecollection.org/catalogue/v2/works` |
| `v1-api.account.wellcomecollection.org` | API Gateway custom domain for the identity API. | `API Gateway` | `identity` | `https://v1-api.account.wellcomecollection.org/` |
| `data.wellcomecollection.org` | Provides access to static snapshots of catalogue data. | `CloudFront` | `catalogue` | `https://data.wellcomecollection.org/catalogue/v2/works.json.gz` |
| `developers.wellcomecollection.org` | Documentation and resources for developers. | `GitHub Pages` | `n/a` | `https://developers.wellcomecollection.org/` |
| `rss.wellcomecollection.org` | Provides RSS feeds for articles and other content. | `CloudFront` | `experience` | `https://rss.wellcomecollection.org/stories` |
| `account.wellcomecollection.org` | User account and login services, managed by Auth0. | `Auth0` | `n/a` | `https://account.wellcomecollection.org/` |
| `i.wellcomecollection.org` | Serves images used on the main website. | `CloudFront` | `experience` | `https://i.wellcomecollection.org/assets/icons/apple-touch-icon.png` |
| `toggles.wellcomecollection.org` | The service for managing feature flags. | `CloudFront` | `experience` | `https://toggles.wellcomecollection.org/toggles.json` |
| `wellcomelibrary.org` | Redirects for the legacy Wellcome Library website. | `CloudFront` | `platform` | `https://wellcomelibrary.org/` |
| `wellcomeimages.org` | Redirects for the legacy Wellcome Images website. | `CloudFront` | `experience` | `https://wellcomeimages.org/` |


### Product/Engineering team facing domains

| Domain Name | Description | Served By | AWS Account | Example URL |
| :--- | :--- | :--- | :--- | :--- |
| `logging.wellcomecollection.org` | Centralised logging for applications and services. | `CloudFront` | `platform` | `https://logging.wellcomecollection.org/` |
| `reporting.wellcomecollection.org` | Internal reporting dashboards and services. | `CloudFront` | `reporting` | `https://reporting.wellcomecollection.org/` |
| `monitoring.wellcome.digital` | Monitoring and alerting dashboards. | `CloudFront` | `platform` | `https://monitoring.wellcome.digital/` |
| `dash.wellcomecollection.org` | A dashboard for staff and developers. | `CloudFront` | `experience` | `https://dash.wellcomecollection.org/` |
| `cardigan.wellcomecollection.org` | The Storybook component library for the design system. | `CloudFront` | `experience` | `https://cardigan.wellcomecollection.org/` |

### Collection Staff facing domains

| Domain Name | Description | Served By | AWS Account | Example URL |
| :--- | :--- | :--- | :--- | :--- |
| `ingest-inspector.wellcomecollection.org` | A tool for inspecting data being ingested into the storage service. | `CloudFront` | `storage` | `https://ingest-inspector.wellcomecollection.org/` |
| `workflow.wellcomecollection.org` | The Goobi workflow management system for digitisation. | `CloudFront` | `workflow` | `https://workflow.wellcomecollection.org/goobi/` |
| `archivematica.wellcomecollection.org` | The Archivematica digital preservation system. | `CloudFront` | `workflow` | `https://archivematica.wellcomecollection.org/` |

### Internal routing domains

These domains are used for routing traffic between services within the AWS infrastructure.

| Domain Name | Description | Served By | AWS Account | Example URL |
| :--- | :--- | :--- | :--- | :--- |
| `content.wellcomecollection.org` | Routes to the main website content frontend. | `CloudFront` | `experience` | `https://content.wellcomecollection.org/` |
| `storage.api.wellcomecollection.org` | API Gateway custom domain for the storage service. | `API Gateway` | `storage` | `https://storage.api.wellcomecollection.org/` |
| `catalogue.api-prod.wellcomecollection.org` | API Gateway custom domain for the catalogue APIs. | `API Gateway` | `catalogue` | `https://catalogue.api-prod.wellcomecollection.org/` |
| `content.api-prod.wellcomecollection.org` | API Gateway custom domain for the content API. | `API Gateway` | `catalogue` | `https://content.api-prod.wellcomecollection.org/` |