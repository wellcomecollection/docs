# Services

Our services can be grouped into several categories based on their functionality and purpose. Below is a list of the main services we maintain, along with their primary functions:

Use the [service template](./template.md) to add a new service.

See also the [system context diagram](../system_context.md) for a high-level overview of how these services interact with each other and external systems.

## Front-end Services (wellcomecollection.org)

Services that are directly related to the Wellcome Collection website and its user-facing features.

- [content_frontend](./frontend/content_frontend.md) - The front-end applications for the main website and identity pages.
- [identity_frontend](./frontend/identity_frontend.md) - The front-end applications for the main website and identity pages.
- [account.wellcomecollection.org](./frontend/account.wellcomecollection.org.md) - The user account and login pages.
- [dash.wellcomecollection.org](./frontend/dash.wellcomecollection.org.md) - A dashboard for staff and developers.
- [cardigan.wellcomecollection.org](./frontend/cardigan.wellcomecollection.org.md) - The Storybook component library for the design system.
- [toggles.wellcomecollection.org](./frontend/toggles.wellcomecollection.org.md) - The feature flag management service.
- [rss_feed](./frontend/rss_feed.md) - The service that generates RSS feeds for website content.

## Wellcome Collection API Services

The public and internal APIs that expose our data and services.

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

- [catalogue_graph](./catalogue_pipeline/catalogue_graph.md) - Manages the relationships between catalogue items.
- [catalogue_pipeline](./catalogue_pipeline/catalogue_pipeline.md) - The core pipeline for processing catalogue data.
- [calm_adapter](./catalogue_pipeline/calm_adapter.md) - Adapter for ingesting data from the Calm archive management system.
- [sierra_adapter](./catalogue_pipeline/sierra_adapter.md) - Adapter for ingesting data from the Sierra library management system.
- [mets_adapter](./catalogue_pipeline/mets_adapter.md) - Adapter for ingesting METS XML data.
- [tei_adapter](./catalogue_pipeline/tei_adapter.md) - Adapter for ingesting TEI XML data.
- [ebsco_adapter](./catalogue_pipeline/ebsco_adapter.md) - Adapter for ingesting data from EBSCO.
- [reindexer](./catalogue_pipeline/reindexer.md) - The service for re-indexing catalogue data.

## Digital Workflow Services

Services that manage the digitisation workflow, from ingest to storage and preservation.

- [storage_service](./workflow/storage_service.md) - The service for storing and retrieving digital objects.
- [ingest_inspector](./workflow/ingest_inspector.md) - A tool for inspecting data being ingested into the storage service.
- [archivematica](./workflow/archivematica.md) - The Archivematica digital preservation system.
- [workflow (Goobi)](./workflow/goobi.md) - The Goobi workflow management system for digitisation.
- [dlcs_iiif](./workflow/dlcs_iiif.md) - The Digital Library Cloud Service for serving IIIF images.

## Developer Services

The Developer Services group includes various adapters and tools that facilitate the integration and management of our systems.

- [logging.wellcomecollection.org](./developer/logging.wellcomecollection.org.md) - Centralised logging for applications and services.
- [reporting.wellcomecollection.org](./developer/reporting.wellcomecollection.org.md) - Internal reporting dashboards and services.
- [monitoring.wellcome.digital](./developer/monitoring.wellcome.digital.md) - Monitoring and alerting dashboards.
- [buildkite_stack](./developer/buildkite_stack.md) - The infrastructure for our CI/CD pipelines.


## Legacy Services

Services that are no longer actively developed but are still maintained for specific purposes.

- [moh (Medical Officer of Health reports)](./legacy/moh.md) - A standalone service for the Medical Officer of Health reports.
- [wellcomeimages_redirects](./legacy/wellcomeimages_redirects.md) - Redirects for the legacy Wellcome Images website.
- [wellcomelibrary_redirects](./legacy/wellcomelibrary_redirects.md) - Redirects for the legacy Wellcome Library website.