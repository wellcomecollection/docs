# RFC 054: Prismic API

This RFC outlines a new set of API endpoints which will allow wellcomecollection.org users to search and filter content which is stored in Prismic.

## Background

We use Prismic as the CMS for exhibitions, events, stories, and other pieces of non-catalogue content on wellcomecollection.org.

The MVP version of the site's prismic search functionality uses [Prismic's GraphQL endpoint](https://prismic.io/docs/graphql) to enable stories search. That MVP has demonstrated that prismic's search functionality isn't able to produce sufficiently relevant results on its own. We would like to replace it with something more configurable, akin to the system we have for the catalogue content.

We're building a pipeline to ingest prismic content into elasticsearch (see separate RFC).

We'd like to build a new corresponding API which will allow users to search for those prismic documents in elasticsearch.

## Requirements, considerations, constraints

- The API should only return enough information for users to figure out whether a result is relevant to them, and provide a link to the relevant page on wellcomecollection.org. The content of the pages themselves should still be fetched from prismic directly.
- Though we're describing them as a separate project, the new endpoints should seamlessly fit into the rest of the wellcomecollection.org API suite from a user POV. All of the existing conventions should be followed.
- The API url structure should also be consistent with what appears on the front end of the site. For example, an article on the site appears at `/articles/{id}`, so the API equivalent should be `/articles/{id}`. The same should be true for search results.
- The new API service should be written in typescript, following patterns set by the [concepts API](../050-concepts-api/README.md) for filtering, pagination, error handling, etc.
- We shouldn't create new IDs for exhibitions, events, stories, etc. There aren't any situations where we should need to merge content from multiple sources, so we should use the document IDs directly from prismic.
- The elasticsearch index mapping should represent the contract between the pipeline and the API. The API shouldn't need to know anything about the structure of the data in prismic.

## Proposed endpoints

### `/articles`

Filter for type eg stories, webcomics

### `/exhibitions`

Filters for date, location, status, etc

### `/events`

Filters for date, location, status, etc

## Open questions

- How do we represent functional content?
- Should we include the full prismic API response at eg `/articles/{id}`?
- If we want to avoid maintaining multiple versions of the same code, should this work be done as an extension to the concepts API?
- Works exist at [api.wellcomecollection.org/catalogue/v2/works](api.wellcomecollection.org/catalogue/v2/works), concepts at [/catalogue/v2/concepts](api.wellcomecollection.org/catalogue/v2/concepts), images at [/catalogue/v2/images](api.wellcomecollection.org/catalogue/v2/images).  
Stories etc aren't part of the catalogue - should the URL be different?

## Next steps

Get building?
