# Services

Our services can be grouped into several categories based on their functionality and purpose. Below is a list of the main services we maintain, along with their primary functions:

## Front-end Services (wellcomecollection.org)

Services that are directly related to the Wellcome Collection website and its user-facing features.

See the [main page](./wellcomecollection_org/README.md), or jump to a section:

- [content_frontend / identity_frontend](./wellcomecollection_org/#content_frontend-identity_frontend) - The front-end applications for the main website and identity pages.
- [account.wellcomecollection.org](./wellcomecollection_org/#accountwellcomecollectionorg) - The user account and login pages.
- [dash.wellcomecollection.org](./wellcomecollection_org/#dashwellcomecollectionorg) - A dashboard for staff and developers.
- [cardigan.wellcomecollection.org](./wellcomecollection_org/#cardiganwellcomecollectionorg) - The Storybook component library for the design system.
- [toggles.wellcomecollection.org](./wellcomecollection_org/#toggleswellcomecollectionorg) - The feature flag management service.
- [rss_feed](./wellcomecollection_org/#rss_feed) - The service that generates RSS feeds for website content.

## Wellcome Collection API Services

The public and internal APIs that expose our data and services.

See the [main page](./apis/README.md), or jump to a section:

- [search_api](./apis/README.md#search_api) - The API for searching across all of our collections.
- [content_api](./apis/README.md#content_api) - The API for retrieving editorial content.
- [concepts_api](./apis/README.md#concepts_api) - The API for retrieving concepts and subjects.
- [data_api](./apis/README.md#data_api) - The API for retrieving bulk data snapshots.
- [items_api](./apis/README.md#items_api) - The API for retrieving information about individual items.
- [identity_api](./apis/README.md#identity_api) - The API for managing user identity and authentication.
- [requesting_api](./apis/README.md#requesting_api) - The API for handling requests for physical items.
- [iiif.wellcomecollection.org](./apis/README.md#iiifwellcomecollectionorg) - The IIIF Image and Presentation API endpoints.

## Catalogue pipeline Services

Services responsible for ingesting and processing data from various sources into the main catalogue.

See the [main page](./catalogue_pipeline/README.md), or jump to a section:

- [catalogue_graph](./catalogue_pipeline/README.md#catalogue_graph) - Manages the relationships between catalogue items.
- [catalogue_pipeline](./catalogue_pipeline/README.md#catalogue_pipeline) - The core pipeline for processing catalogue data.
- [calm_adapter](./catalogue_pipeline/README.md#calm_adapter) - Adapter for ingesting data from the Calm archive management system.
- [sierra_adapter](./catalogue_pipeline/README.md#sierra_adapter) - Adapter for ingesting data from the Sierra library management system.
- [mets_adapter](./catalogue_pipeline/README.md#mets_adapter) - Adapter for ingesting METS XML data.
- [tei_adapter](./catalogue_pipeline/README.md#tei_adapter) - Adapter for ingesting TEI XML data.
- [ebsco_adapter](./catalogue_pipeline/README.md#ebsco_adapter) - Adapter for ingesting data from EBSCO.
- [reindexer](./catalogue_pipeline/README.md#reindexer) - The service for re-indexing catalogue data.

## Digital Workflow Services

Services that manage the digitisation workflow, from ingest to storage and preservation.

See the [main page](./workflow/README.md), or jump to a section:

- [storage_service](./workflow/README.md#storage_service) - The service for storing and retrieving digital objects.
- [ingest_inspector](./workflow/README.md#ingest_inspector) - A tool for inspecting data being ingested into the storage service.
- [archivematica](./workflow/README.md#archivematica) - The Archivematica digital preservation system.
- [workflow (Goobi)](./workflow/README.md#workflow-goobi) - The Goobi workflow management system for digitisation.
- [dlcs_iiif](./workflow/README.md#dlcs_iiif) - The Digital Library Cloud Service for serving IIIF images.

## Developer Services

The Developer Services group includes various adapters and tools that facilitate the integration and management of our systems.

See the [main page](./developer/README.md), or jump to a section:

- [logging.wellcomecollection.org](./developer/README.md#loggingwellcomecollectionorg) - Centralised logging for applications and services.
- [reporting.wellcomecollection.org](./developer/README.md#reportingwellcomecollectionorg) - Internal reporting dashboards and services.
- [monitoring.wellcome.digital](./developer/README.md#monitoringwellcomedigital) - Monitoring and alerting dashboards.
- [buildkite_stack](./developer/README.md#buildkite_stack) - The infrastructure for our CI/CD pipelines.


## Legacy Services

Services that are no longer actively developed but are still maintained for specific purposes.

See the [main page](./legacy/README.md), or jump to a section:

- [moh (Medical Officer of Health reports)](./legacy/README.md#moh-medical-officer-of-health-reports) - A standalone service for the Medical Officer of Health reports.
- [wellcomeimages_redirects](./legacy/README.md#wellcomeimages_redirects) - Redirects for the legacy Wellcome Images website.
- [wellcomelibrary_redirects](./legacy/README.md#wellcomelibrary_redirects) - Redirects for the legacy Wellcome Library website.