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
        "alt": ""
    },
    "caption": "",
    "seasons": [
        "",
        ...
    ],
}
```

```
GET /exhibitions?query=foo&filters=bar&sort=baz&sortOrder=asc
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
    "nextPage": "/exhibitions?query=foo&filters=bar&sort=baz&sortOrder=asc&page=2",
}
```

## Filters

- **instantiations.start.from**
  DD-MM-YYYY
- **instantiations.start.to**
  DD-MM-YYYY
- **instantiations.end.from**
  DD-MM-YYYY
- **instantiations.end.to**
  DD-MM-YYYY
- **place.label**
  List of physical locations, would also include "Online".
- **contributor.agent.label**
  e.g. Filmmaker, Curator
- **format.label**
  [`Permanent Exhibition`, `Season`, `Installation`]

## Sort options

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- place
- contributor
