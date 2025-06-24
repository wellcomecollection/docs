# AWS Accounts

This document describes the structure and purpose of the AWS accounts used by Wellcome Collection. We partition our AWS resources into different accounts to manage access, security, and billing effectively. 

## Table of Contents

- [`platform`](#platform)
- [`experience`](#experience)
- [`catalogue`](#catalogue)
- [`identity`](#identity)
- [`storage`](#storage)
- [`workflow`](#workflow)
- [`digitisation`](#digitisation)
- [`digirati`](#digirati)
- [Legacy accounts](#legacy-accounts)

See https://github.com/wellcomecollection/aws-account-infrastructure for the Infrastructure as Code (IaC) that manages these accounts.

## `platform`

**Number**: 760097843905  
**Description**: The platform account is the central hub for managing shared infrastructure and services across Wellcome Collection AWS accounts. It contains the core services that support the Wellcome Collection's digital infrastructure, including CI/CD pipelines, logging and the first place API requests are routed to.

### Services 

- [`catalogue_pipeline`](./services/catalogue_pipeline/catalogue_pipeline.md): Manages the ingestion and processing of catalogue data to prepare it for the APIs. Contains many subsystems and component services involved in the data processing pipeline.
- [`calm_adapter`](./services/catalogue_pipeline/calm_adapter.md): Adapts data from the Calm system for use in the catalogue.
- [`sierra_adapter`](./services/catalogue_pipeline/sierra_adapter.md): Adapts data from the Sierra system for use in the catalogue.
- [`mets_adapter`](./services/catalogue_pipeline/mets_adapter.md): Adapts data from the METS system for use in the catalogue.
- [`tei_adapter`](./services/catalogue_pipeline/tei_adapter.md): Adapts data from the TEI system for use in the catalogue.
- [`ebsco_adapter`](./services/catalogue_pipeline/ebsco_adapter.md): Adapts data from the EBSCO system for use in the catalogue.
- [`reindexer`](./services/catalogue_pipeline/reindexer.md): Manages the reindexing of catalogue data when we make changes to data model in the catalogue pipeline.
- [`buildkite_stack`](./services/developer/buildkite_stack.md): Contains the Buildkite stack for the Wellcome Collection, which is used for CI/CD pipelines.
- [`wellcomelibrary_redirects`](./services/legacy/wellcomelibrary_redirects.md): Manages redirects for the legacy Wellcome Library website.

### Cloudfront Distributions

- `iiif.wellcomecollection.org`: Serves the IIIF image and presentation APIs.
- `logging.wellcomecollection.org`: Routes to the logging services for the Wellcome Collection.
- `reporting.wellcomecollection.org`: Routes to staff & developer facing reporting services for the Wellcome Collection.
- `*.wellcomelibrary.org`: Serves the Wellcome Library redirects.
- `api.wellcomecollection.org`: Routes requests to all Wellcome Collection APIs, including catalogue search, concepts, content, storage, text (ALTO), items and requesting APIs.

## `catalogue`

**Number**: 756629837203  
**Description**: Contains the infrastructure for the Wellcome Collection public facing APIs.

### Services 

- [`data_api`](./services/apis/data_api.md): Allows access to static snapshots of the Wellcome Collection catalogue data.
- [`search_api`](./services/apis/search_api.md): Provides search functionality across the catalogue, including works, and images.
- [`content_api`](./services/apis/content_api.md): Provides access to the Wellcome Collection content API, which includes editorial content from Prismic.
- [`concepts_api`](./services/apis/concepts_api.md): Provides access to the Wellcome Collection concepts API.
- [`items_api`](./services/apis/items_api.md): Provides access to the Wellcome Collection items API.

### Cloudfront Distributions

- `data.wellcomecollection.org`: Serves the data API.

### Associated Domains

- `catalogue.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the catalogue APIs.
- `content.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the content API for the Wellcome Collection.

## `experience`

**Number**: 130871440101  
**Description**: Hosts the infrastructure for the main Wellcome Collection website.

### Services 

- [`content_frontend`](./services/frontend/content_frontend.md): The main website frontend, built with Next.js including editorial content and catalogue search.
- [`identity_frontend`](./services/frontend/identity_frontend.md): The frontend for user authentication and authorisation, built with Next.js.
- [`rss_feed`](./services/frontend/rss_feed.md): Provides RSS feeds for the Wellcome Collection.
- [`toggles.wellcomecollection.org`](./services/frontend/toggles.wellcomecollection.org.md): Manages toggles and a/b testing for the Wellcome Collection website.
- [`wellcomeimages_redirects`](./services/legacy/wellcomeimages_redirects.md): Redirects for the legacy Wellcome Images website.

### Cloudfront Distributions

- `wellcomecollection.org`: Serves the main Wellcome Collection website, including:
  - `identity.wellcomecollection.org`: Routes to `identity_frontend` for user authentication and authorisation.
  - `content.wellcomecollection.org`: Routes to `content_frontend` for the main website content.
- `rss.wellcomecollection.org`: Serves RSS feeds for the Wellcome Collection.
- `dash.wellcomecollection.org`: Serves the Wellcome Collection dashboard for staff and developers.
- `toggles.wellcomecollection.org`: Serves the toggles service for feature flags.
- `preview.wellcomecollection.org`: Serves the preview environment for the Wellcome Collection website.
- `static.wellcomecollection.org`: Serves static assets for the Wellcome Collection website, for editorial staff.
- `i.wellcomecollection.org`: Serves images for the Wellcome Collection website.
- `cardigan.wellcomecollection.org`: Serves the Wellcome Collection Storybook design system.
- `wellcomeimages.org`: Serves the Wellcome Images redirects.

## `identity`

**Number**: 770700576653  
**Description**: Contains the requesting service and identity APIs for the Wellcome Collection. 

### Services 

- [`identity_api`](./services/apis/identity_api.md): Provides the identity API for user authentication and authorisation.
- [`requesting_api`](./services/apis/requesting_api.md): Provides the requesting API for the Wellcome Collection.
- [`account.wellcomecollection.org`](./services/frontend/account.wellcomecollection.org.md): The user account and login pages.

### Associated Domains

- `identity.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the identity API for the Wellcome Collection.

## `storage`

**Number**: 299497370133
**Description**: Contains the storage service and other long-term storage for the Wellcome Collection.

### Services

- [`storage_service`](./services/workflow/storage_service.md): The service for storing and retrieving digital objects.
- [`ingest_inspector`](./services/workflow/ingest_inspector.md): A tool for inspecting data being ingested into the storage service.

### Associated Domains

- `storage.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the storage service for the Wellcome Collection.

## `workflow`

**Number**: 365125299635
**Description**: Contains the workflow management systems for the Wellcome Collection.

### Services

- [`archivematica`](./services/workflow/archivematica.md): The Archivematica digital preservation system.
- [`workflow (Goobi)`](./services/workflow/goobi.md): The Goobi workflow management system for digitisation.

## `digitisation`

**Number**: 964279954909
**Description**: Contains the infrastructure for the digitisation workflow.

### Services

- [`dlcs_iiif`](./services/workflow/dlcs_iiif.md): The Digital Library Cloud Service for serving IIIF images.

## `digirati`

**Number**: 048926554549
**Description**: Contains the infrastructure for the Digirati-managed services.

### Services

- [`iiif.wellcomecollection.org`](./services/apis/iiif.wellcomecollection.org.md): The IIIF Image and Presentation API endpoints.

## Legacy accounts

### `born-digital-accessions`

**Number**: 094622098392
**Description**: Contains the infrastructure for the born-digital accessions service. This is a legacy account and is no longer used.

### `catalogue-api-prismic`

**Number**: 418439632722
**Description**: Contains the infrastructure for the Prismic content API. This is a legacy account and is no longer used.

### `wc-platform-infra`

**Number**: 312583357253
**Description**: Contains the infrastructure for the Wellcome Collection platform. This is a legacy account and is no longer used.