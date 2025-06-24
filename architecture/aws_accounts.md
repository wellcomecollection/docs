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

- [`catalogue_pipeline`](./services/catalogue_pipeline/README.md#catalogue_pipeline): Manages the ingestion and processing of catalogue data to prepare it for the APIs. Contains many subsystems and component services involved in the data processing pipeline.
- [`calm_adapter`](./services/catalogue_pipeline/README.md#calm_adapter): Adapts data from the Calm system for use in the catalogue.
- [`sierra_adapter`](./services/catalogue_pipeline/README.md#sierra_adapter): Adapts data from the Sierra system for use in the catalogue.
- [`mets_adapter`](./services/catalogue_pipeline/README.md#mets_adapter): Adapts data from the METS system for use in the catalogue.
- [`tei_adapter`](./services/catalogue_pipeline/README.md#tei_adapter): Adapts data from the TEI system for use in the catalogue.
- [`ebsco_adapter`](./services/catalogue_pipeline/README.md#ebsco_adapter): Adapts data from the EBSCO system for use in the catalogue.
- [`reindexer`](./services/catalogue_pipeline/README.md#reindexer): Manages the reindexing of catalogue data when we make changes to data model in the catalogue pipeline.
- [`buildkite_stack`](./services/developer/README.md#buildkite_stack): Contains the Buildkite stack for the Wellcome Collection, which is used for CI/CD pipelines.
- [`wellcomelibrary_redirects`](./services/legacy/README.md#wellcomelibrary_redirects): Manages redirects for the legacy Wellcome Library website.

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

- [`data_api`](./services/apis/README.md#data_api): Allows access to static snapshots of the Wellcome Collection catalogue data.
- [`search_api`](./services/apis/README.md#search_api): Provides search functionality across the catalogue, including works, and images.
- [`content_api`](./services/apis/README.md#content_api): Provides access to the Wellcome Collection content API, which includes editorial content from Prismic.
- [`concepts_api`](./services/apis/README.md#concepts_api): Provides access to the Wellcome Collection concepts API.
- [`items_api`](./services/apis/README.md#items_api): Provides access to the Wellcome Collection items API.

### Cloudfront Distributions

- `data.wellcomecollection.org`: Serves the data API.

### Associated Domains

- `catalogue.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the catalogue APIs.
- `content.api-prod.wellcomecollection.org`: API Gateway custom domain, routes to the content API for the Wellcome Collection.

## `experience`

**Number**: 130871440101  
**Description**: Hosts the infrastructure for the main Wellcome Collection website.

### Services 

- [`content_frontend`](./services/wellcomecollection_org/README.md#content_frontend): The main website frontend, built with Next.js including editorial content and catalogue search.
- [`identity_frontend`](./services/wellcomecollection_org/README.md#identity_frontend): The frontend for user authentication and authorisation, built with Next.js.
- [`rss_feed`](./services/wellcomecollection_org/README.md#rss_feed): Provides RSS feeds for the Wellcome Collection.
- [`toggles`](./services/wellcomecollection_org/README.md#toggleswellcomecollectionorg): Manages toggles and a/b testing for the Wellcome Collection website.
- [`wellcomeimages_redirects`](./services/legacy/README.md#wellcomeimages_redirects): Redirects for the legacy Wellcome Images website.

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

- [`identity_api`](./services/apis/README.md#identity_api): Provides the identity API for user authentication and authorisation.
- [`requesting_api`](./services/apis/README.md#requesting_api): Provides the requesting API for managing user requests to view items.

### Associated Domains

- `v1-api.account.wellcomecollection.org`: API Gateway custom domain, routes to the identity API for user authentication and authorisation.
- `account.wellcomecollection.org`: Auth0 custom domain, routes to Auth0 tenant for login and user management.

## `storage`

**Number**: 975596993436  
**Description**: Hosts the Wellcome Collection digital archival storage services, including S3 buckets for long term storage of digital assets and data. 

### Services

- [`storage_service`](./services/workflow/README.md#storage_service): Manages the ingestion, storage and retrieval of digital archival assets. Contains many subsystems and component services involved in the storage of digital assets.
- [`ingest_inspector`](./services/workflow/README.md#ingest_inspector): Provides a web interface for inspecting the data being ingested into the catalogue.

### Cloudfront Distributions

- `ingest-inspector.wellcomecollection.org`: Routes to the Ingest Inspector service.

### Associated Domains

- `storage.api.wellcomecollection.org`: API Gateway custom domain, routes to the storage service for managing digital archival assets.

## workflow

**Number**: 299497370133  
**Description**: Hosts the services for managing the digital production workflows at Wellcome Collection. This includes the management of digital assets, and adding of metadata before they are stored in our archival storage.

### Services

- [`archivematica`](./services/workflow/README.md#archivematica): A digital preservation & workflow system that manages the ingest, storage, and access of digital assets. Specifically dealing with "born-digital" assets. This service is managed by [Artefactual Systems](https://www.artefactual.com/), running on our AWS infrastructure. It has a number of subsystems and component services involved in the digital preservation workflow.
- [`workflow`](./services/workflow/README.md#workflow-goobi): An instance of rdigitisation preservation & workflow management system [Goobi](https://www.intranda.com/en/digiverso/goobi/goobi-overview/) that manages artefacts of digitisation workflows, including the management of metadata and digital assets. A 3rd party service provided and managed by Intranda, running on our AWS infrastructure. It has a number of subsystems and component services involved in the digitisation workflow.

### Associated Domains

- `workflow.wellcomecollection.org`: Routes to the Goobi workflow service for managing digital production workflows.
- `archivematica.wellcomecollection.org`: Routes to the Archivematica service for managing digital preservation workflows.

## `digitisation`

**Number**: 404315009621  
**Description**: Contains object storage for digitisation workflows. This is intended to manage the storage of digital assets before they enter the digital production workflows, and before they are stored in our archival storage. Access to object storage (S3) is provided to the digital production teams for managing upload of digital assets.

## `digirati`

**Number**: 653428163053  
**Description**: Account for the Digirati-managed services, including the IIIF image services.  

### Services

- [`dlcs_iiif`](./services/workflow/README.md#dlcs_iiif): A collection of subsystems and component services that provide [IIIF](https://iiif.io/) image services for the Wellcome Collection, including the services routed to by the IIIF APIs. 
- [`moh`](./services/legacy/README.md#moh-medical-officer-of-health-reports): Medical Officer of Health reports (MoH) webapp, a legacy service providing access to [Medical Officer of Health reports.](https://wellcomelibrary.org/moh/about-the-reports/about-the-medical-officer-of-health-reports/).


## Legacy accounts

For reference only, these accounts are no longer in use and should be considered deprecated.

- **systems_strategy**: 269807742353  
- **microsites**: 782179017633
- **data**: 964279923020
- **reporting**: 269807742353