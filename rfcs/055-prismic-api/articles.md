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
        "alt": ""
    },
    "caption": "",
    "partOf": [
        {
            ... // reuse the partOf model for series
        }
    ]
}
```

```
GET /articles?query=foo&filters=bar&sort=baz&sortOrder=asc
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
    "nextPage": "/articles?query=foo&filters=bar&sort=baz&sortOrder=asc&page=2",
}
```

## Filters

- **publicationDate.from**
  DD-MM-YYYY
- **publicationDate.to**
  DD-MM-YYYY
- **contributor.agent.label**
  Includes author, artists, photographers
- **partOf**
  List of series (e.g. serials - which is a scheduled list of articles, or webcomic series)
- **format.label**
  [`Comic`, `Long read`, `Prose poem`, `Podcast`, `In pictures`, `Article`, `Photo story`, `Interview`, `Book extract`]

## Sort options

- relevance
- publicationDate

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- contributor.agent.label
- partOf
- format.label
