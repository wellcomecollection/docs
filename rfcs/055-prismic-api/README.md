# RFC 055: Prismic API

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

#### Example response

```json
GET /articles/{id}
{
    "id": "",
    "format": "",
    "title": "",
    "body": "", // not exposed by default, should require an ?includes=body
    "standfirst": "",
    "published": "",
    "contributors": [
        {
            ... // reuse the Contributor model
        },
        ...
    ],
    "image": {
        "thumbnail": {
            ... // reuse the DigitalLocation model
        },
        "caption": ""
    }
}
```

```json
GET /articles?query=foo&filters=bar&sort=baz
{
    "type": "ResultList",
    "results": [
        {
            ... // as above
        },
        ...
    ],
    "pageSize": 100,
    "totalResults": 1000,
    "totalPages": 10,
    "nextPage": "/articles?query=foo&filters=bar&sort=baz?page=2",
}
```

#### Filters

- date
- contributor
- series
- contentType

#### Sort

- date
- relevance

### `/exhibitions`

#### Example response

```json
GET /exhibitions/{id}
{
    "id": "",
    "format": "",
    "title": "",
    "status": "",
    "instantiations": [
        {
            "start": "", // ISO 8601 date only (no time)
            "end": "", // ISO 8601 date only (no time)
            "place": "",
            "guide": {
                ... // reuse the DigitalLocation model
            }
        }
    ],
    "contributors": [ // behind ?includes=contributors
        {
            ... // reuse the Contributor model
        },
        ...
    ],
    "image": {
        "thumbnail": {
            ... // reuse the DigitalLocation model
        },
        "caption": ""
    },
    "seasons": [
        "",
        ...
    ],
}
```

```json
GET /exhibitions?query=foo&filters=bar&sort=baz
{
    "type": "ResultList",
    "results": [
        {
            ... // as above
        },
        ...
    ],
    "pageSize": 100,
    "totalResults": 1000,
    "totalPages": 10,
    "nextPage": "/exhibitions?query=foo&filters=bar&sort=baz?page=2",
}
```

#### Filter

- date
- status
- place
- contributor
- format (ie permanent, exhibition, installation)
- season

#### Sort

- date
- relevance

### `/events`

#### Example response

```json
GET /events/{id}
{
    "id": "",
    "format": "",
    "title": "",
    "status": "",
    "isOnline": false,
    "availableOnline": false,
    "audience": "",
    "instantiations": [
        {
            "start": "", // ISO 8601 datetime
            "end": "", // ISO 8601 datetime
            "place": ""
        }
    ],
    "contributors": [ // behind ?includes=contributors
        {
            ... // reuse the Contributor model
        },
        ...
    ],
    "image": {
        "thumbnail": {
            ... // reuse the DigitalLocation model
        },
        "caption": ""
    },
    "series": [
        "",
        ...
    ],
    "seasons": [
        "",
        ...
    ],
}
```

```json
GET /events?query=foo&filters=bar&sort=baz
{
    "type": "ResultList",
    "results": [
        {
            ... // as above
        },
        ...
    ],
    "pageSize": 100,
    "totalResults": 1000,
    "totalPages": 10,
    "nextPage": "/events?query=foo&filters=bar&sort=baz?page=2",
}
```

#### Filter

- date
- accessibility status (is it audio described, signed, etc)
- location
- format (eg discussion)
- series
- season
- audience (eg schools)
- contributor
- isOnline?
- availableOnline?

#### Sort

- date
- relevance

## Open questions

- How do we represent functional content?
- If we want to avoid maintaining multiple versions of the same code, should this work be done as an extension to the concepts API?
- Works exist at [api.wellcomecollection.org/catalogue/v2/works](api.wellcomecollection.org/catalogue/v2/works), concepts at [/catalogue/v2/concepts](api.wellcomecollection.org/catalogue/v2/concepts), images at [/catalogue/v2/images](api.wellcomecollection.org/catalogue/v2/images).
Stories etc aren't part of the catalogue - should the URL be different?
- what are the top level types? is it articles? stories? series?
- where do books go? they appear on the stories landing page, so should they appear in stories search results? or are they at a separate endpoint?
- what is a serial? what is a series?
- can we filter exhibitions for accessibility, ie whether a digital guide exists? we can for events, but unclear for exhibitions
- do we have any exhibition contributors who have contributed to more than one? is a filter for exhibition contributors really going to be useful?

## Next steps

- Answer most of those questions ☝️
- Write a glossary of terms
- Get building?
