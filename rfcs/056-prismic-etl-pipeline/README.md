# RFC 056: Prismic to Elasticsearch ETL pipeline

**Status:** Draft

**Last updated:** 23/2/2023

## Context
In order to make our editorial content - including stories, comics, exhibitions and events - more discoverable, we want to be able to search it via an API as described in [RFC 055](https://github.com/wellcomecollection/docs/tree/main/rfcs/055-prismic-api).

While Prismic does provide some search functionality of its own (which we have been using for initial versions of unified search), we want more control and fewer limitations. To achieve this we want to use Elasticsearch, as we do for our other search services. As such, we need to get data from Prismic into Elasticsearch: this RFC will propose the mechanism by which we achieve that.

#### Desiderata
- Changes (including additions and edits but possibly not deletions - see BEEPB OPOSDF) in Prismic are reflected promptly in the Elasticsearch index
- Full reindexes are easy, quick and cheap to perform
- Changes to the data mapping (and the index mapping) can be made easily by any developer

#### Prior art
Both the catalogue pipeline and the concepts pipeline extract data from external sources, transform it, and load it into elasticsearch. They have similar architectures:

![Existing pipeline architecture](https://user-images.githubusercontent.com/4429247/220949681-b0c765d0-46a2-446a-a236-91553edc7263.png)

The adapter/ingestor stages are separate from the transformer/aggregator stages to separate the (often complex!) concern of getting data out of external APIs and that of selecting which parts of the data we want and transforming them. 

Most of the adapters receive updates by polling the source APIs at regular intervals for documents updated  in the intervening time period. Where deletions are indicated only by the absence of the data from subsequent requests to the source, we run additional "deletion checker" services which run over all currently stored records and delete them if they're missing from the source.

## Proposal

The Prismic corpus is smaller than our other corpora, and this ETL pipeline is very linear and self-contained. This points us towards a simple architecture, which helps with (a) speed/ease of reindexing and (b) maintainability across the team.

![Proposed architecture](https://user-images.githubusercontent.com/4429247/220966188-097cac58-56f8-4c6d-afd8-48a17e50720c.png)

1. A 'window generator' Lambda triggered on schedule, which generates a payload representing a time period/window that is sent to (2).
2. A 'Prismic ETL' Lambda which consumes time periods (potentially half-bounded or unbounded, for complete reindexes) and then:
   i. Queries using the `@prismicio/client` for documents with a [`last_publication_date`](https://prismic.io/docs/rest-api-technical-reference#q) within the specified window.
   ii. Transforms these documents to JSON objects with `display` and `query` fields corresponding to the entities/queries described in [RFC 055](https://github.com/wellcomecollection/docs/tree/main/rfcs/055-prismic-api).
   iii. Indexes these into an Elasticsearch cluster using the Elasticsearch JS client's bulk helpers.
   
For complete reindexes, it would be straightforward to trigger the Prismic ETL lambda from a local script, with a payload that covers all documents.

#### Technical implementation points
- The intention is that the Prismic ETL Lambda will be written in TypeScript for maintainability, but one disadvantage of this is that we lose some of the patterns/tools that Scala gives us for reactive streaming data pipelines. Suggest we try [RxJS](https://rxjs.dev/) for this purpose.


## Questions and potential issues
- What do we do about deletions? Do we know if they happen? We could write something similar to the [CALM deletion checker](https://github.com/wellcomecollection/docs/tree/main/rfcs/032-calm-deletions) if necessary.