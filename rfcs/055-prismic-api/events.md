# Prismic API: Events endpoint

## Example response

```
GET /events/{id}
{
    "type": "Event",
    "id": "",
    "format": {
        "id": "",
        "label": ""
        "type": "EventFormat"
    },
    "title": "",
    "status": "",
    "isOnline": boolean,
    "availableOnline": boolean,
    "interpretations": [
        {
            "label": "",
            "type": "EventInterpretation"
        },
        ...
    ],
    "audiences": [
        {
            "label": "",
            "type": "EventAudience"
        },
        ...
    ],
    "instantiations": [
        {
            "start": "", // ISO 8601 datetime
            "end": "", // ISO 8601 datetime
            "place": {
                "id": "",
                "label": "",
                "type": "Place"
            },

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

```
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

## Filter

- instantiations.start.from
- instantiations.start.to
- instantiations.end.from
- instantiations.end.to
- interpretation
- place
- format
- partOf
- audience
- contributor
- isOnline
- availableOnline

## Sort

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- status
- place
- contributor
- format
- audience
