# Services

Our services can be grouped into several categories based on their functionality and purpose. Below is a list of the main services we maintain, along with their primary functions:

## Front-end Services (wellcomecollection.org)

Services that are directly related to the Wellcome Collection website and its user-facing features.

See the [main page](./frontend/README.md), or jump to a section:

- [content_frontend](./frontend/content_frontend.md) - The front-end applications for the main website and identity pages.
- [identity_frontend](./frontend/identity_frontend.md) - The front-end applications for the main website and identity pages.
- [account.wellcomecollection.org](./frontend/account.wellcomecollection.org.md) - The user account and login pages.
- [dash.wellcomecollection.org](./frontend/dash.wellcomecollection.org.md) - A dashboard for staff and developers.
- [cardigan.wellcomecollection.org](./frontend/cardigan.wellcomecollection.org.md) - The Storybook component library for the design system.
- [toggles.wellcomecollection.org](./frontend/toggles.wellcomecollection.org.md) - The feature flag management service.
- [rss_feed](./frontend/rss_feed.md) - The service that generates RSS feeds for website content.

## Wellcome Collection API Services

The public and internal APIs that expose our data and services.

See the [main page](./apis/README.md), or jump to a section:

- [search_api](./apis/search_api.md) - The API for searching across all of our collections.
- [content_api](./apis/content_api.md) - The API for retrieving editorial content.
- [concepts_api](./apis/concepts_api.md) - The API for retrieving concepts and subjects.
- [data_api](./apis/data_api.md) - The API for retrieving bulk data snapshots.
- [items_api](./apis/items_api.md) - The API for retrieving information about individual items.
- [identity_api](./apis/identity_api.md) - The API for managing user identity and authentication.
- [requesting_api](./apis/requesting_api.md) - The API for handling requests for physical items.
- [iiif.wellcomecollection.org](./apis/iiif.wellcomecollection.org.md) - The IIIF Image and Presentation API endpoints.

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