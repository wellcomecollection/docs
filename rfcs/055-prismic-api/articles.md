# Prismic API: articles endpoint

## Example response

```
GET /articles/{id}
{
    "type": "Article",
    "id": "",
    "format": {
        "id": "",
        "label": "",
        "type": "ArticleFormat"
    },
    "title": "",
    "publicationDate": "",
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

```
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

## Filters

- publicationDate.from
- publicationDate.to
- contributor.agent.label
- partOf
- format.label

## Sort options

- relevance
- publicationDate

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- contributor.agent.label
- partOf
- format.label
