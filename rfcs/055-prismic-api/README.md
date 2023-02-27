# RFC 055: Prismic API

This RFC outlines a new set of API endpoints which will allow wellcomecollection.org users to search and filter content which is stored in Prismic.

## Background

We use [Prismic](https://prismic.io/) to edit and store information about our exhibitions, events, stories, and other pieces of non-catalogue content on wellcomecollection.org.

Recently, we've allowed users to [search for stories on wellcomecollection.org](https://wellcomecollection.org/search/stories) using [Prismic's GraphQL API](https://Prismic.io/docs/graphql).

That MVP implementation has demonstrated that Prismic's search functionality isn't good enough to produce relevant results on its own.  
See slack threads [about Prismic's GraphQL search](https://wellcome.slack.com/archives/C02ANCYL90E/p1666103130854219) and [attempts to augment Prismic's search results with third party libraries](https://wellcome.slack.com/archives/C3TQSF63C/p1667495781964079).

Primsic matches documents to a user's search terms using a very loose, fuzzy query on all text-like fields, but, unlike elasticsearch, does not assign each document a score corresponding to its relevance. Instead of sorting by relevance, users are limited to sorting the retrieved documents by date or by title, which often makes the results appear irrelevant (eg weak matches appearing at the top of the list due to recency). Primsic's GraphQL API is also unsuitable for filtering content by arbitrary fields, which further limits our users' ability to find the content they're looking for.

We'd like to replace our queries to the Prismic API with something more configurable, like the system we have for the catalogue.

We're building a pipeline which will ingest content from Prismic into a set of elasticsearch indices (see [RFC 056: Prismic to Elasticsearch ETL pipeline](https://github.com/wellcomecollection/docs/blob/rfc-056-prismic-etl/rfcs/056-prismic-etl-pipeline/README.md)). To allow users to search and filter  that content from Prismic, we also need a new set of API endpoints which will query those elasticsearch indices.

This API will live at `https://api.wellcomecollection.org/content/v0/`, with endpoints for `/articles`, `/exhibitions`, and `/events`.

We won't consider the way that documents are scored as part of this RFC. Relevance requirements should be developed iteratively and independently from the development of the API.

## Purposes

The `/content` API should allow users to:

- request a single exhibition, event, or article by ID
- query `exhibitions`, `events`, and `articles`, retrieving relevant results based on their search terms
- filter and aggregate lists of exhibitions, events, and articles by a set of predefined filters and aggregations

## Further requirements

- The new endpoints should fit seamlessly into the rest of the wellcomecollection.org API suite from a user's POV, following as many of the existing conventions as possible.
- The API should only return enough information for users to determine whether a result is relevant, and provide a link to the relevant page on wellcomecollection.org.
- The content of the pages themselves should still be fetched from Prismic directly.
- The API's URL structure should be consistent with what appears on wellcomecollection.org's front-end. For example, if article on the site appears at `/articles/{id}`, the API equivalent should be at `content/v0/articles/{id}`.

## Notes on implementation

- The new API service should be written in typescript, following patterns set by the [concepts API](../050-concepts-api/README.md) for filtering, pagination, error handling, etc.
- Though the content API will share code with the concepts API, it should be built as a separate service.
- The elasticsearch index mapping should represent the contract between the pipeline and the API. The API shouldn't need to know anything about the structure of the data in Prismic, and any substantial data augmentation should be done by the pipeline.
- We shouldn't mint new IDs for exhibitions, events, stories, etc. Articles, exhibitions, and events are only stored in Prismic, and won't need to be merged with other sources. `/content` objects should therefore use the document IDs directly from Prismic. This is also consistent with the way that these objects are referenced in wellcomecollection.org's URLs (eg [/articles/Y_M_xhQAACcAqmjW](https://wellcomecollection.org/articles/Y_M_xhQAACcAqmjW), [/exhibitions/Y0QhIxEAAA__0sMb](https://wellcomecollection.org/exhibitions/Y0QhIxEAAA__0sMb)).

## Proposed endpoints

### Articles

`https://api.wellcomecollection.org/content/v0/articles`

Read more about the structure of the [articles endpoint](articles.md)

### Exhibitions

`https://api.wellcomecollection.org/content/v0/exhibitions`

Read more about the structure of the [exhibitions endpoint](exhibitions.md)

### Events

`https://api.wellcomecollection.org/content/v0/events`

Read more about the structure of the [events endpoint](events.md)

## Open questions

- Should we have a common model for exhibition and event `instantiations`?
- Can we populate some real examples of each response object?
- Are we thinking about the right aggregations?
