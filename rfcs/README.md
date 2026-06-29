# Request for comments (RFC)

An RFC is a place to discuss possible changes to the Wellcome Collection platform.

## Table of contents

- [What is an RFC?](#what-is-an-rfc)
- [How do I format an RFC?](#how-do-i-format-an-rfc)
- [RFC Listing](#rfc-listing)

## What is an RFC?

Please create an RFC if you have an idea about how to make a big change to the way we do things currently and need a place to share that with your colleagues.

The process of creating an RFC, discussing that RFC in a pull request, amending and merging is important to provide a forum for all to contribute to the platform.

When an RFC is merged it provides a guide to implementing that change when it is useful to do so, or provides context to an [Architecture decision record (ADR) document](../adr/).

## How do I format an RFC?

An RFC is a markdown file in the `rfcs` directory. It should be named with a number and a short description, e.g. `070-concepts-api-changes.md`.
The filename should be prefixed with the next available number in the sequence, and the title of the RFC should match the filename.

The RFC **must** include the following sections:

- **Title:** A short, descriptive title for the RFC, in the format `RFC {number}: {title}`.
- **Last modified:** The date and time the RFC was last modified, in ISO 8601 UTC format with explicit offset, e.g. `2026-06-01T12:34:56+00:00`.
- **Purpose:** A brief description of what the RFC is about. This is used as the summary in the RFC listing table.

`## Context` or `## Background` sections are optional supporting sections if you need additional framing.

The RFC **should** include the following sections:

- **Proposal:** A detailed description of the proposed solution, including any relevant technical details, diagrams, or examples.
- **Alternatives considered:** A discussion of any alternative solutions that were considered, and why they were not chosen.
- **Impact:** A description of the impact of the proposed solution, including any potential risks or challenges.
- **Next steps:** A list of next steps for implementing the proposed solution, including any dependencies or prerequisites.

### Validation

We validate RFC structure automatically for files under `rfcs/*/README.md`:

- In PRs, GitHub Actions runs `.scripts/validate_rfc.py` on changed RFC README files.
- Locally, you can run `python3 .scripts/validate_rfc.py` to validate all RFC README files.
- For pre-commit enforcement, install [pre-commit](https://pre-commit.com/) and run:

```bash
# macOS (Homebrew)
brew install pre-commit

# or with pipx
pipx install pre-commit

pre-commit install

# optional first run across existing files
pre-commit run --all-files
```

This enables all RFC automation hooks from `.pre-commit-config.yaml`.

The RFC listing table in this file is also automated:

- In PRs, GitHub Actions checks that the table is in sync with `.scripts/create_table_summary.py`.
- Locally, pre-commit runs these hooks (in order) when RFC files change:
  - `.scripts/validate_rfc.py`
  - `.scripts/create_table_summary.py --write-readme`

`Last modified` is non-automatic. Update it manually when making a meaningful RFC change, then run validation.

## RFC Listing

_This is generated from the RFCs in this directory using `.scripts/create_table_summary.py`._

| RFC ID | Summary | Next Line | Last Modified |
|--------|---------|-----------|---------------|
| [091-digitisation-ingest-identifiers](091-digitisation-ingest-identifiers/README.md) | RFC 091: Digitisation ingest identifiers during the Sierra to Folio migration | Wellcome Collection is migrating its library management system from Sierra to Folio. The b-number (the Sierra system number) is embedded in storage locations, METS records, IIIF manifest URIs, and the join key that merges digitised content onto the public catalogue work. This RFC sets out why the b-number cannot simply be swapped for a Folio id, and proposes minting catalogue-style identifiers at ingest via a secured endpoint on the Identifiers API (RFC 089), with separate cross-migration and post-migration ingest paths. | 29 Jun 2026 |
| [088-folio-identity-requesting-migration](088-folio-identity-requesting-migration/README.md) | RFC 088: Migrating identity, requesting and items APIs from Sierra to FOLIO | This RFC describes how we move the identity, requesting and item-availability APIs that power `wellcomecollection.org` from our current Library Management System (LMS), **Sierra**, to its replacement, **FOLIO**. It sets out the proposed architecture (a parallel, FOLIO-backed **v2** identity API fronted by Auth0), the embedded API contract, the migration plan (a per-request website toggle plus lazy patron migration, culminating in a single coordinated cutover), and the questions still open before cutover. | 22 Jun 2026 |
| [087-kiosk-mode](087-kiosk-mode/README.md) | RFC 087: wellcomecollection.org in kiosk mode | This RFC serves to outline how we propose to offer in-venue experiences using our current website, while optimising it for a different experience than usual. | 13 May 2026 |
| [086-item-viewer-refactor](086-item-viewer-refactor/README.md) | RFC 086: IIIF Viewer Context Refactoring | This folder contains a comprehensive plan to refactor the IIIF Viewer context to eliminate code duplication and centralise derived state calculations. | 14 Apr 2026 |
| [084-shopify-integration-strategies](084-shopify-integration-strategies/README.md) | RFC 084: Shopify Integration Approaches for Wellcome Collection | This research outlines five approaches for integrating Shopify with the Wellcome Collection website, ranging from simple embedded solutions to fully headless implementations. | 16 Feb 2026 |
| [083-stable_identifiers](083-stable_identifiers/README.md) | RFC 083: Stable identifiers following mass record migration | This RFC discusses what will happen to public catalogue identifiers following the mass migration of records from CALM/Sierra to Axiell Collection / Folio and how we can update the catalogue pipeline to accommodate this change. | 10 Feb 2026 |
| [082-curated-collections-prismic](082-curated-collections-prismic/README.md) | RFC 082: Curated Collections × Prismic | As we increasingly connect Collections to Content (Prismic), we are having a lot of conversations that can get muddled together. We thought it best to separate concerns. There are a few things to address, from the selection process to the actual solution implementation, and we wanted to start documenting them. | 26 Jan 2026 |
| [080-pipeline-failures](080-pipeline-failures/README.md) | RFC 080: Handling failures in Python Step Functions | Pipeline steps may fail for certain inputs. Those failures are caught, logged, and retried using a templated recursive state machine defined for each step. The overall pipeline is thereby kept clean of error handling and can simply describe the happy-path flow of data. | 01 Dec 2025 |
| [079-new-online](079-new-online/README.md) | RFC 079: Showcase recently digitised works on the Collections landing page | This RFC proposes adding a digitisation `createdDate` to catalogue Works and exposing it via the catalogue-api so we can surface “New Online” works, including a dedicated page and an editorialised selection on the Collections landing page. It outlines how the date is extracted from METS, indexed, and made available for filtering and sorting. | 15 Oct 2025 |
| [078-name-reconciliation-service](078-name-reconciliation-service/README.md) | RFC 078: Name Reconciliation Service (NARESE) | This RFC proposes NARESE, a batch-oriented Name Reconciliation Service that uses embedding-based vector similarity search combined with constrained Large Language Model reasoning to identify and cluster variant textual forms of person and agent names in our Works metadata. The service addresses fragmentation caused by different spellings, initials, and date formats (e.g., "John Smith", "J. Smith", "Smith, John (1870-1932)") by producing machine-generated reconciliation clusters with traceable provenance and confidence tiers, prioritizing precision over recall to maintain data quality trust while improving search relevance, faceting, and downstream enrichment capabilities. | 08 Sep 2025 |
| [081-identifiers-in-iiif-builder](081-identifiers-in-iiif-builder/README.md) | RFC 081: Identifiers in iiif-builder: beyond the B number | IIIF-Builder (aka DDS) understands various identifier forms (BNumbers, CALM Reference Numbers and Work IDs), and makes processing decisions based on the form of the identifier. For example, if asked to process a b number, it knows the item _must_ have been processed by Goobi, and it _must_ be in the `digitised` storage service space. These _musts_ will soon no longer be true, and soon there will not even be b numbers. | 15 Aug 2025 |
| [077-enriching-addressables-with-works](077-enriching-addressables-with-works/README.md) | RFC 077: Content API: Enriching addressable content types with Works data | We'd like to enrich the content pages of our website, i.e. those whose data is retrieved from Prismic, with previews of Works that are linked to within them. This RFC proposes augmenting the [Addressable content types](https://github.com/wellcomecollection/docs/tree/main/rfcs/062-content-api-all-search#addressable-content-types) with Works data and creating a new endpoint for retrieving individual Addressable items, so that we can create the desired UI with a single API call. | 07 Jul 2025 |
| [076-catalogue-api-knowledge-graph](076-catalogue-api-knowledge-graph/README.md) | RFC 076: Integrating the catalogue graph into the works pipeline | This RFC proposes integrating the catalogue graph deeper into the catalogue pipeline to enable enrichment of the production works index with additional metadata and hierarchical relationships. The changes would replace the relation embedder subsystem with graph-based operations and create a new Python-based works ingestor, allowing for enhanced work pages and improved consistency between theme pages and search results. | 21 Jun 2025 |
| [075-updated_adapters](075-updated_adapters/README.md) | RFC 075: Using Apache Iceberg tables in Catalogue Pipeline adapters | Discussing a replacement architecture for the catalogue pipeline adapters, moving away from the Versioned Hybrid Store (VHS) using Apache Iceberg as the underlying storage format. | 02 Jun 2025 |
| [070-concepts-api-changes](070-concepts-api-changes/README.md) | RFC 070: Concepts API changes | This RFC describes changes to the concepts API, which will be used to support new theme pages on the Wellcome Collection website. | 13 Mar 2025 |
| [071-python_builds](071-python_builds/README.md) | RFC 071: Python Building and Deployment | Building and deploying Python projects | 13 Mar 2025 |
| [068-exhibitions-content-api](068-exhibitions-content-api/README.md) | RFC 068: Exhibitions in Content API | Exhibitions are to be added to Events search, becoming Events & Exhibitions search. We'll therefore be working on indexing Exhibitions in a more intentional manner. That indexing and subsquent API endpoint will power the Events & Exhibitions search as well as, eventually, the existing listing pages. | 18 Feb 2025 |
| [069-catalogue_graph_ingestor](069-catalogue_graph_ingestor/README.md) | RFC 069: Catalogue Graph Ingestor | Following on from the [Catalogue Graph pipeline](https://github.com/wellcomecollection/docs/tree/main/rfcs/066-graph_pipeline), this RFC outlines the requirements for the Catalogue Graph Ingestor to replace the existing Concepts Pipeline. | 18 Feb 2025 |
| [067-prismic-api-ids](067-prismic-api-ids/README.md) | RFC 067: Prismic API ID casing | This RFC proposes a consistent casing for Prismic API IDs across custom types, fields, and slices, to align with Prismic defaults and improve maintainability. | 13 Jan 2025 |
| [066-graph_pipeline](066-graph_pipeline/README.md) | RFC 066: Catalogue Graph pipeline | This RFC outlines considerations for the development of the catalogue-graph pipeline. The first iteration of the graph will be focused on concepts and their enrichment with data from external ontologies, as discussed below. | 08 Jan 2025 |
| [064-graph-data-model](064-graph-data-model/README.md) | RFC 064: Graph data model | An update to the previous [RFC #62](../062-knowledge-graph/README.md) on the knowledge graph, focusing on a new graph data model for concept enrichment and linking to external ontologies. | 05 Dec 2024 |
| [065-library-data-link-explorer](065-library-data-link-explorer/README.md) | RFC 065: Library Data Link Explorer | This RFC outlines the plan for the Library Data Link Explorer web application. This tool will enable Collections Information colleagues the ability to view and debug work relationships independently, potentially replacing the workflow of requesting a developer-run script to produce a matcher graph .dot file. | 27 Nov 2024 |
| [062-content-api-all-search](062-content-api-all-search/README.md) | RFC 062: Content API: All search and indexing of addressable content types | Searching for content on wellcomecollection.org is currently split into separate, statically-ordered grids for Stories, Works, Images and Events. This RFC proposes a new "All" search endpoint that will return all Addressable content types in a single, ordered list, improving efficiency and relevance. | 18 Nov 2024 |
| [063-catalogue_pipeline_lambdas](063-catalogue_pipeline_lambdas/README.md) | RFC 063: Catalogue Pipeline services from ECS to Lambda | Discuss the potential benefits and challenges of moving the catalogue pipeline services from AWS Elastic Container Service (ECS) to AWS Lambda. | 25 Oct 2024 |
| [062-knowledge-graph](062-knowledge-graph/README.md) | RFC 062: Wellcome Collection Graph overview and next steps | Enriching concepts in the Wellcome Collection with a knowledge graph to enhance discovery and exploration of the collection online. | 11 Oct 2024 |
| [061-content-api-next-steps](061-content-api-next-steps/README.md) | RFC 061: Content API next steps | This RFC documents the next steps for the Content API, specifically focusing on the addition of Prismic Events to the API. It outlines the background information, challenges encountered, decisions made, and the proposal for how the API will be structured moving forward. | 03 Jul 2024 |
| [074-offsite-item-requesting](074-offsite-item-requesting/README.md) | RFC 074: Offsite requesting | This RFC outlines the plan for enabling online requesting of items that are held offsite, with a phased approach to accommodate both onsite and offsite viewing. | 23 Apr 2024 |
| [060-healthcheck-principles](060-healthcheck-principles/README.md) | RFC 060: Service health-check principles | This RFC explores how we should implement health-checks in our services, specifically around services that have HTTP interactions / are serviced by load-balancers that implement health-checking. | 07 Feb 2024 |
| [059-splitting-pipeline-terraform](059-splitting-pipeline-terraform/README.md) | RFC 059: Splitting the catalogue pipeline Terraform | This RFC proposes a change to how we manage the Terraform for instances of the catalogue pipeline. | 03 Jul 2023 |
| [058-relevance-testing](058-relevance-testing/README.md) | RFC 058: Relevance testing | This RFC describes how and why we might write a new version of _rank_, our relevance testing tool. | 20 Jun 2023 |
| [073-prismic-api](073-prismic-api/README.md) | RFC 073: Content API | This RFC outlines a new set of API endpoints which will allow wellcomecollection.org users to search and filter content which is stored in Prismic. | 08 Mar 2023 |
| [055-genres-as-concepts](055-genres-as-concepts/README.md) | RFC 055: Genres as Concepts | This RFC proposes to treat Genres as Concepts, in the same manner as Subjects. | 06 Mar 2023 |
| [056-prismic-etl-pipeline](056-prismic-etl-pipeline/README.md) | RFC 056: Prismic to Elasticsearch ETL pipeline | This RFC proposes a mechanism for extracting data from Prismic, transforming it, and loading it into Elasticsearch to make our editorial content more discoverable via an API. | 02 Mar 2023 |
| [054-authority-vs-canonical-concept-ids](054-authority-vs-canonical-concept-ids/README.md) | RFC 054: Authoritative ids with multiple Canonical ids. | This RFC proposes a change to the way Concepts are stored in the catalogue-concepts index | 10 Feb 2023 |
| [017-url_design](017-url_design/README.md) | RFC 017: URL Design | This RFC proposes a set of principles for designing URLs on wellcomecollection.org, ensuring they are persistent, user-friendly, and globally unique. | 09 Dec 2022 |
| [053-lambda-logging](053-lambda-logging/README.md) | RFC 053: Logging in Lambdas | This RFC proposes a solution for logging in AWS Lambdas, aiming to provide a consistent and efficient way to capture and stream logs from Lambda functions to an Elasticsearch cluster. | 30 Nov 2022 |
| [051-concepts-adapters](051-concepts-adapters/README.md) | RFC 051: Ingesting Library of Congress concepts | This RFC outlines the design for the first phase of the concepts pipeline, specifically focusing on ingesting concepts from the Library of Congress (LoC) and preparing them for use in the Wellcome Collection catalogue. | 08 Jul 2022 |
| [052-concepts-pipeline](052-concepts-pipeline/README.md) | RFC 052: The Concepts Pipeline - phase one | This RFC describes the first phase of the Concepts Pipeline, which will be used to ingest and aggregate concepts. | 07 Jul 2022 |
| [050-concepts-api](050-concepts-api/README.md) | RFC 050: Design considerations for the concepts API | This RFC collects some initial thinking on how we might represent concepts in the catalogue API. It's a starting point for discussions; not a final design. | 31 May 2022 |
| [049-catalogue-api-aggregations-modelling](049-catalogue-api-aggregations-modelling/README.md) | RFC 049: Changing how aggregations are retrieved by the Catalogue API | This RFC proposes a change to how aggregations are handled in the Catalogue API, allowing us to remove the internal/display model coupling that currently exists. | 13 May 2022 |
| [048-concepts-rfcs](048-concepts-rfcs/README.md) | RFC 048: Concepts work plan | This RFC outlines the work plan for introducing concepts to the Wellcome digital platform, including the design of a concepts API, knowledge graph population, and integration with works. | 10 May 2022 |
| [047-catalogue-api-index-structure](047-catalogue-api-index-structure/README.md) | RFC 047: Changing the structure of the Catalogue API index | This RFC proposes a change to the structure of the Catalogue API index, which is used to store and retrieve documents for the Catalogue API. | 29 Apr 2022 |
| [046-born-digital-iiif](046-born-digital-iiif/README.md) | RFC 046: Born Digital in IIIF | This RFC is a proposal for how Wellcome can represent born digital archival material using IIIF. | 21 Apr 2022 |
| [072-transitive-sierra-hierarchies](072-transitive-sierra-hierarchies/README.md) | RFC 072: Transitive Sierra hierarchies | This RFC proposes a new stage in the Works pipeline to allow for transitive Sierra hierarchies. | 20 Apr 2022 |
| [045-sierra-work-relationships](045-sierra-work-relationships/README.md) | RFC 045: Work relationships in Sierra, part 2 | This RFC is a continuation of the work started in [RFC-044: Sierra Series](044-sierra-series). | 21 Feb 2022 |
| [044-patron-deletions](044-patron-deletions/README.md) | RFC 044: Tracking Patron Deletions | This RFC describes a proposal for tracking patron deletions in the Sierra API and removing corresponding records from Auth0. | 09 Feb 2022 |
| [043-recording-deletions](043-recording-deletions/README.md) | RFC 043: Removing deleted records from (re)indexes | This RFC proposes a change to the way we handle deleted source records in the Catalogue API index. | 26 Jul 2021 |
| [040-tei_adapter](040-tei_adapter/README.md) | RFC 040: TEI Adapter | This RFC proposes an adapter to harvest TEI files from GitHub and store them in a VersionedStore. | 24 Jun 2021 |
| [042-requesting-model](042-requesting-model/README.md) | RFC 042: Requesting model | This RFC describes how we will model the data for physical items in the catalogue API, so that users can find out how to access them. | 20 May 2021 |
| [041-miro-data-changes](041-miro-data-changes/README.md) | RFC 041: Tracking changes to the Miro data | This RFC describes a proposal for tracking changes to the Miro data, which is used to populate the Catalogue API. | 19 May 2021 |
| [039-requesting-api-design](039-requesting-api-design/README.md) | RFC 039: Requesting API design | This RFC describes the design of a new API for requesting items in the catalogue. | 26 Apr 2021 |
| [038-matcher-versioning](038-matcher-versioning/README.md) | RFC 038: Matcher versioning | This RFC describes a proposal for how to version works in the matcher/merger pipeline, to avoid issues with works becoming "stuck" in the pipeline. | 19 Apr 2021 |
| [037-api-faceting-principles](037-api-faceting-principles/README.md) | RFC 037: API faceting principles & expectations | This RFC describes the principles and expectations for how we expect the Catalogue API to behave in terms of faceting, filtering, and aggregating data. It aims to provide a clear and consistent framework for building a faceted search interface that can effectively handle multiple dimensions of data. | 24 Mar 2021 |
| [036-holdings-records](036-holdings-records/README.md) | RFC 036: Modelling holdings records | This RFC describes how we will model holdings records in the Catalogue API. | 03 Mar 2021 |
| [035-marc-856](035-marc-856/README.md) | RFC 035: Modelling MARC 856 "web linking entry" | This RFC describes how we will model MARC 856 "web linking entry" in the Catalogue API. | 24 Feb 2021 |
| [032-calm-deletions](032-calm-deletions/README.md) | RFC 032: Calm deletion watcher | This RFC describes a proposal for a Calm deletion watcher, which will allow us to detect deleted Calm records and update the VHS accordingly. | 09 Feb 2021 |
| [034-location_location_location](034-location_location_location/README.md) | RFC 034: Modelling Locations in the Catalogue API | This RFC describes how we will model locations in the Catalogue API, and how we will return them in the API. | 08 Feb 2021 |
| [033-api-internal-model-versioning](033-api-internal-model-versioning/README.md) | RFC 033: Api internal model versioning | This RFC describes a proposal for how to version the internal model used by the catalogue API, to allow for independent deployment of the API and the catalogue pipeline. | 01 Feb 2021 |
| [031-relation_batcher](031-relation_batcher/README.md) | RFC 031: Relation Batcher | This RFC describes a proposal for how to batch works in the relation embedder, to improve performance and reduce duplicate work. | 10 Nov 2020 |
| [030-pipeline_merging](030-pipeline_merging/README.md) | RFC 030: Pipeline merging | This RFC describes a proposal for how to merge works in the catalogue pipeline, to avoid issues with works becoming "stuck" in the pipeline. | 09 Oct 2020 |
| [029-work_state_modelling](029-work_state_modelling/README.md) | RFC 029: Work state modelling | This RFC proposes a new way of modelling works in the catalogue pipeline and API, separating the type of work from its state in the pipeline. This aims to improve composability, clarity, and ease of adding new types or states. | 07 Sep 2020 |
| [028-pipeline-intermediate-storage](028-pipeline-intermediate-storage/README.md) | RFC 028: Pipeline Intermediate Storage | This RFC describes a proposal for how to store intermediate works in the catalogue pipeline, to allow for more efficient and cost-effective processing of works. | 07 Sep 2020 |
| [027-relation-embedder](027-relation-embedder/README.md) | RFC 027: Relation Embedder | This RFC describes a proposal for how to denormalise relations between works in the catalogue pipeline, to improve the API response times and allow for richer queries. | 07 Sep 2020 |
| [025-tagging-our-resources](025-tagging-our-resources/README.md) | RFC 025: Tagging our Terraform resources | This RFC describes a proposal for how to tag our Terraform-managed resources, so we can find the corresponding Terraform configuration in the console. | 03 Aug 2020 |
| [021-data_science_in_the_pipeline](021-data_science_in_the_pipeline/README.md) | RFC 021: Data science in the pipeline | This RFC outlines a proposal for integrating data science services into the Wellcome Collection catalogue pipeline. The goal is to augment works and images with data inferred from them using data science techniques, such as feature vectors and colour palettes for images. | 29 Jul 2020 |
| [026-relevance_reporting_service](026-relevance_reporting_service/README.md) | RFC 026: Relevance reporting service | This RFC describes a proposal for a service that will allow us to test and report on the efficacy of our elastic-queries by comparing a set of search-terms and their respective expected results and ordering. | 20 Jul 2020 |
| [022-logging](022-logging/README.md) | RFC 022: Logging | This RFC describes a proposal for how we log from our services, and how we collect and search those logs. | 29 Jun 2020 |
| [002-archival_storage](002-archival_storage/README.md) | RFC 002: Archival Storage Service | This RFC proposes a service for storing archival and access copies of digital assets, ensuring long-term preservation and compliance with industry standards. | 01 Jun 2020 |
| [023-images-endpoint](023-images-endpoint/README.md) | RFC 023: Images endpoint | This RFC proposes an initial images endpoint for the catalogue API, allowing for searching and fetching images from the visual collections. | 06 May 2020 |
| [024-library_management](024-library_management/README.md) | RFC 024: Library management | This RFC describes a proposal for how we manage our libraries, so we can ensure they work together and are easy to discover. | 01 May 2020 |
| [013-release_deployment_tracking](013-release_deployment_tracking/README.md) | RFC 013: Release & Deployment tracking | This RFC proposes a new approach to tracking releases and deployments of services in the Wellcome Collection platform, moving away from the current reliance on Terraform for deployment. The approach described has been superseded by improvements in native AWS ECS deployment capabilities, but the tagging and tracking concepts remain relevant. | 08 Apr 2020 |
| [019-platform_reliability](019-platform_reliability/README.md) | RFC 019: Platform Reliability | This RFC proposes a set of actions to improve the reliability of the Wellcome Collection platform, based on a review of current issues and discussions with the team. | 20 Mar 2020 |
| [020-locations_requesting](020-locations_requesting/README.md) | RFC 020: Locations and requesting | This RFC describes a proposal for how to model item locations in the Catalogue API, and how to build a new Stacks API that allows users to request physical items. | 06 Mar 2020 |
| [016-holdings_service](016-holdings_service/README.md) | RFC 016: Holdings service | This RFC proposes a now deprecated approach to building a holdings service, which has been superseded by the [020-locations_requesting](../020-locations-requesting/README.md) RFC. | 03 Mar 2020 |
| [018-pipeline_tracing](018-pipeline_tracing/README.md) | RFC 018: Pipeline Tracing | This RFC outlines a proposal for adding distributed tracing to the Wellcome Collection catalogue pipeline. The goal is to improve debugging and monitoring of the pipeline by tracking the flow of data through it, from the adapters right through to ingest. | 29 Jan 2020 |
| [011-network_architecture](011-network_architecture/README.md) | RFC 011: Network Architecture | This RFC proposes a network architecture for Wellcome Collection services, ensuring effective security, maintenance, and scalability as the number of services grows. | 16 Oct 2019 |
| [008-api_filtering](008-api_filtering/README.md) | RFC 008: API Filtering | This RFC proposes a consistent approach to filtering and sorting resources in our APIs, ensuring a uniform developer experience. | 24 Sep 2019 |
| [015-how_we_work](015-how_we_work/README.md) | RFC 015: How we work | This RFC outlines a set of principles for how we work together as a team, including our approach to collaboration, communication, and decision-making. | 09 Sep 2019 |
| [014-born_digital_workflow](014-born_digital_workflow/README.md) | RFC 014: Born digital workflow | This RFC proposes an initial workflow for managing born-digital archives using Archivematica, which will be integrated with our new storage service. | 13 Jun 2019 |
| [012-api_architecture](012-api_architecture/README.md) | RFC 012: API Architecture | This RFC proposes a solution for serving Wellcome Collection APIs from a single domain, `api.wellcomecollection.org`, using AWS API Gateway and CloudFront. | 25 Jan 2019 |
| [006-reindexer_architecture](006-reindexer_architecture/README.md) | RFC 006: Reindexer architecture | This RFC proposes a new architecture for the reindexer, which is responsible for updating records in DynamoDB to trigger events for downstream applications. | 09 Jan 2019 |
| [010-data_model](010-data_model/README.md) | RFC 010: Data model | This RFC outlines the process and models used to create ontologies for Wellcome Collection's digital platform, focusing on a unified graph of linked data. | 09 Jan 2019 |
| [009-aws_account_layout](009-aws_account_layout/README.md) | RFC 009: AWS account setup | This RFC proposes a solution for breaking up the monolithic "wellcomedigitalplatform" AWS account into smaller, more manageable accounts, improving security and access control. | 09 Jan 2019 |
| [001-merger_matcher](001-merger_matcher/README.md) | RFC 001: Matcher architecture | This RFC proposes an architecture for the matcher and merger components of the reindexer, which are responsible for identifying and merging related works in the catalogue. | 02 Nov 2018 |
| [003-asset_access](003-asset_access/README.md) | RFC 003: Asset Access | This RFC proposes a solution for restricting access to digital assets based on their access provisions and the authentication status of the viewer, while allowing these assets to be served via a CDN. | 02 Nov 2018 |
| [004-mets_adapter](004-mets_adapter/README.md) | RFC 004: METS Adapter | This RFC proposes a solution for ingesting METS files from the digitisation workflow software Goobi, converting them to JSON, and integrating them into the Wellcome Collection digital catalogue. | 02 Nov 2018 |
| [005-reporting_pipeline](005-reporting_pipeline/README.md) | RFC 005: Reporting Pipeline | This RFC proposes a reporting pipeline for the Wellcome Collection data, allowing for analytics and reporting on data from various sources. | 02 Nov 2018 |
| [007-goobi_upload](007-goobi_upload/README.md) | RFC 007: Goobi Upload | This RFC proposes a new mechanism for uploading assets to Goobi workflows, replacing existing mechanisms with a more efficient and automated solution. | 02 Nov 2018 |
