# Services

Our services can be grouped into several categories based on their functionality and purpose. Below is a list of the main services we maintain, along with their primary functions:

See also the [system context diagram](./system_context.md) for a high-level overview of how these services interact with each other and external systems.

## Frontend Services

Services that are directly related to the Wellcome Collection website and its user-facing features.

- [content_frontend](./services/frontend/content_frontend.md)
- [identity_frontend](./services/frontend/identity_frontend.md)
- [account.wellcomecollection.org](./services/frontend/account.wellcomecollection.org.md)
- [dash.wellcomecollection.org](./services/frontend/dash.wellcomecollection.org.md)
- [cardigan.wellcomecollection.org](./services/frontend/cardigan.wellcomecollection.org.md)
- [rss_feed](./services/frontend/rss_feed.md)
- [toggles.wellcomecollection.org](./services/frontend/toggles.wellcomecollection.org.md)

## Catalogue pipeline Services

Services responsible for ingesting and processing data from various sources into the main catalogue.

- [catalogue_graph](./services/catalogue_pipeline/catalogue_graph.md)
- [catalogue_pipeline](./services/catalogue_pipeline/catalogue_pipeline.md)
- [calm_adapter](./services/catalogue_pipeline/calm_adapter.md)
- [sierra_adapter](./services/catalogue_pipeline/sierra_adapter.md)
- [mets_adapter](./services/catalogue_pipeline/mets_adapter.md)
- [tei_adapter](./services/catalogue_pipeline/tei_adapter.md)
- [ebsco_adapter](./services/catalogue_pipeline/ebsco_adapter.md)
- [reindexer](./services/catalogue_pipeline/reindexer.md)

## Workflow Services

Services that manage the digitisation workflow, from ingest to storage and preservation.

- [storage_service](./services/workflow/storage_service.md)
- [ingest_inspector](./services/workflow/ingest_inspector.md)
- [archivematica](./services/workflow/archivematica.md)
- [workflow (Goobi)](./services/workflow/goobi.md)
- [dlcs_iiif](./services/workflow/dlcs_iiif.md)

## Wellcome Collection API Services

The public and internal APIs that expose our data and services.

- [search_api](./services/apis/search_api.md)
- [content_api](./services/apis/content_api.md)
- [concepts_api](./services/apis/concepts_api.md)
- [data_api](./services/apis/data_api.md)
- [items_api](./services/apis/items_api.md)
- [identity_api](./services/apis/identity_api.md)
- [requesting_api](./services/apis/requesting_api.md)
- [iiif.wellcomecollection.org](./services/apis/iiif.wellcomecollection.org.md)

## Developer Services

The Developer Services group includes various adapters and tools that facilitate the integration and management of our systems.

- [logging.wellcomecollection.org](./services/developer/logging.wellcomecollection.org.md)
- [reporting.wellcomecollection.org](./services/developer/reporting.wellcomecollection.org.md)
- [monitoring.wellcome.digital](./services/developer/monitoring.wellcome.digital.md)
- [buildkite_stack](./services/developer/buildkite_stack.md)

## Legacy Services

Services that are no longer actively developed but are still maintained for specific purposes.

- [moh (Medical Officer of Health reports)](./services/legacy/moh.md)
- [wellcomeimages_redirects](./services/legacy/wellcomeimages_redirects.md)
- [wellcomelibrary_redirects](./services/legacy/wellcomelibrary_redirects.md)