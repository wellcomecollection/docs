# Prismic API: exhibitions endpoint

## Example response

```
GET /exhibitions/{id}
{
    "type": "Exhibition",
    "id": "",
    "format": {
        "id": "",
        "label": ""
        "type": "ExhibitionFormat"
    },
    "title": "",
    "status": "",
    "instantiations": [
        {
            "start": "", // ISO 8601 date only (no time)
            "end": "", // ISO 8601 date only (no time)
            "place": {
                "id": "",
                "label": "",
                "type": "Place"
            },
            "interpretations": [
                {
                    "label": "",
                    "type": "ExhibitionInterpretation"
                },
                ...
            ]
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

```
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

## Filters

- instantiations.start.from
- instantiations.start.to
- instantiations.end.from
- instantiations.end.to
- status.label
- place.label
- contributor.agent.label
- format.label
- season

## Sort options

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- status
- place
- contributor
