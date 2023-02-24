# RFC 055: Prismic API

This RFC outlines a new set of API endpoints which will allow wellcomecollection.org users to search and filter content which is stored in Prismic.

## Background

We use Prismic CMS to edit and store exhibitions, events, stories, and other pieces of non-catalogue content on wellcomecollection.org.

The site currently allows users to [search for stories](https://wellcomecollection.org/search/stories) using [Prismic's GraphQL API](https://Prismic.io/docs/graphql). That MVP implementation has demonstrated that Prismic's search functionality isn't good enough to produce relevant results on its own. We would like to replace it with something more configurable, like the system we have for the catalogue.

We're building a pipeline to ingest Prismic content into elasticsearch (see separate RFC).  
We also need a corresponding API which will allow users to search for those Prismic documents in elasticsearch.

## Requirements, considerations, constraints

- We'll be considering articles, exhibitions, and events in this first pass. Books won't be included for now, but could be added at a later date.
- The API should only return enough information for users to figure out whether a result is relevant to them, and provide a link to the relevant page on wellcomecollection.org. The content of the pages themselves should still be fetched from Prismic directly.
- Though we're describing them as a separate project, the new endpoints should seamlessly fit into the rest of the wellcomecollection.org API suite from a user POV. All of the existing conventions should be followed.
- Despite prioritising search and defaulting to the Prismic API for display, We'll still include a way to fetch a single document by ID, eg `/articles/{id}`.
- The API's URL structure should also be consistent with what appears on the front end of the site. For example, if article on the site appears at `/articles/{id}`, the API equivalent should be at `/articles/{id}`. The same should be true for search results.
- The new API service should be written in typescript, following patterns set by the [concepts API](../050-concepts-api/README.md) for filtering, pagination, error handling, etc.
- We shouldn't create new IDs for exhibitions, events, stories, etc. There aren't any situations where we should need to merge content from multiple sources, so we should use the document IDs directly from Prismic.
- The elasticsearch index mapping should represent the contract between the pipeline and the API. The API shouldn't need to know anything about the structure of the data in Prismic.
- We won't include an endpoint for `/series`, nor will we include series nodes in the `/articles` endpoint. If an article is part of a series, we'll denormalise information from its parent onto the article itself to use for relevance and visual signposting in results.

## Proposed endpoints

### `/articles`

#### Example response

```http
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
    },
    "partOf": [
        {
            ... // reuse the partOf model for series
        }
    ]
}
```

```http
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
    "nextPage": "/articles?query=foo&filters=bar&sort=baz&page=2",
}
```

#### Filters

- date
- contributor
- series
- format

#### Sort

- date
- relevance

### `/exhibitions`

#### Example response

```http
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

```http
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
    "nextPage": "/exhibitions?query=foo&filters=bar&sort=baz&page=2",
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

```http
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
    "partOf": [
        {
            ... // reuse the partOf model for series and seasons
        }
    ]
}
```

```http
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
    "nextPage": "/events?query=foo&filters=bar&sort=baz&page=2",
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
Stories etc aren't part of the catalogue - should the URL be different? Does `/content` work?
- Should we include a `/series` endpoint as part of this work?

## Next steps

- Answer most of those questions ☝️
- Write a glossary of terms
- Get building?
