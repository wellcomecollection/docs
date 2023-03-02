# RFC 056: Prismic to Elasticsearch ETL pipeline

**Status:** Draft

**Last updated:** 23/2/2023

## Context
In order to make our editorial content - including stories, comics, exhibitions and events - more discoverable, we want to be able to search it via an API as described in [RFC 055](https://github.com/wellcomecollection/docs/tree/main/rfcs/055-prismic-api).

While Prismic does provide some search functionality of its own (which we have been using for initial versions of unified search), we want more control and fewer limitations. To achieve this we want to use Elasticsearch, as we do for our other search services. As such, we need to get data from Prismic into Elasticsearch: this RFC will propose the mechanism by which we achieve that.

#### Desiderata
- Changes (including additions and edits but possibly not deletions - see [questions](#questions-and-potential-issues)) in Prismic are reflected promptly in the Elasticsearch index
- Full reindexes are easy, quick and cheap to perform
- Changes to the data mapping (and the index mapping) can be made easily by any developer

#### Prior art
Both the catalogue pipeline and the concepts pipeline extract data from external sources, transform it, and load it into elasticsearch. They have similar architectures:

![Existing pipeline architecture](https://user-images.githubusercontent.com/4429247/220949681-b0c765d0-46a2-446a-a236-91553edc7263.png)

The adapter/ingestor stages are separate from the transformer/aggregator stages to separate the (often complex!) concern of getting data out of external APIs and that of selecting which parts of the data we want and transforming them. 

Most of the adapters receive updates by polling the source APIs at regular intervals for documents updated  in the intervening time period. Where deletions are indicated only by the absence of the data from subsequent requests to the source, we run additional "deletion checker" services which run over all currently stored records and delete them if they're missing from the source.

## Proposal

The Prismic corpus is smaller than our other corpora, and this ETL pipeline is very linear and self-contained. However, Prismic data is fairly heavily [normalised](https://en.wikipedia.org/wiki/Database_normalization) and so we need to build a solution that can (a) denormalise data from linked documents onto our "primary" documents and (b) reflect changes from these linked documents ("secondary" documents) on all of the primary documents on which they are present. 

A basic example of this would be that the `article` type has a `contributors` field, which links to `role` and `person` types:
```json
{
  ...
  "contributors": {
    "role": {
      "id": "<foreign key>",
      "type": "editorial-contributor-roles",
      ...
    },
    "person": {
      "id": "<foreign key>",
      "type": "people",
      ...
    }
  }
}
```

Fortunately, Prismic provide an API, [`graphQuery`](https://prismic.io/docs/graphquery-rest-api) which can do this denormalisation for us, using a GraphQL-like syntax. This straightforwardly solves the first problem of denormalising linked data, but not the second problem of reflecting changes in it.

The proposed solution to this is to store the IDs of the secondary documents alongside the other information we index in Elasticsearch for primary documents:
```json
{
  "display": {
    // Opaque JSON to be displayed by the API
  },
  "query": {
    // Fields for querying, filtering etc
    ...
    // List of identifiers (foreign keys) of linked documents
    "ids": [
      "1",
      "2",
      "3"
    ]
  }
}
```
Then we can build a pipeline that works as follows:

1. A 'window generator' Lambda triggered on schedule, which generates a payload representing a time period/window that is sent to (2).
2. A 'Prismic ETL' Lambda which consumes time periods (potentially half-bounded or unbounded, for complete reindexes) and then:
   1. Queries Prismic for all documents (including denormalised data on primary documents) updated within the time window.
   2. For all secondary documents, query the ES index for already-indexed primary documents that contain them.
   3. Queries Prismic for all the documents (including denormalised data) from (ii) that are not part of the list returned by (i).
   4. Transforms the resultant primary documents into JSON objects as described above.
   5. Indexes these into an Elasticsearch cluster using the Elasticsearch JS client's bulk helpers. 

For complete reindexes, it would be straightforward to trigger the Prismic ETL lambda from a local script, with a payload that covers all documents. In this case, it would also be an easy optimisation to disable steps (ii) and (iii), as all documents would be being fetched regardless.

#### Technical implementation points
- The intention is that the Prismic ETL Lambda will be written in TypeScript for maintainability, but one disadvantage of this is that we lose some of the patterns/tools that Scala gives us for reactive streaming data pipelines. Suggest we try [RxJS](https://rxjs.dev/) for this purpose.


## Questions and potential issues
- What do we do about deletions? Do we know if they happen? We could write something similar to the [CALM deletion checker](https://github.com/wellcomecollection/docs/tree/main/rfcs/032-calm-deletions) if necessary. 
  _**Initial answer**: having checked with the editorial team, deletions very rarely happen with our content. I suggest we hold off on solving this for our initial efforts, especially given our intention to make full reindexes easy._
- What about the [Prismic webhook](https://prismic.io/docs/webhooks) rather than polling to detect updates?
  _**Initial answer**: while this has some clear advantages (immediacy of updates being one), I decided against it for the following reasons:_
  - *Reliability issues: if a single update is missed because of bugs in our services or problems on Prismic's side, we have no way of knowing that we missed it.*
  - *Not useful for complete reindexes: with a similar implementation effort (due to the necessity of storing relationships between primary and secondary documents), the webhook solution does nothing to solve the problem of complete reindexes. We would have to build a service or script to scroll over every document and pass every identifier to the webhook service, which would be both inefficient and time-consuming to build.* 
